from strategy_triplescreen import triple_screen_signal
from strategy_turtle import turtle_signal
import ccxt
import time
import json
from strategy_zscore import zscore_signal
from strategy_inverse import inverse_signal
from strategy_coveredcall import coveredcall_adjustment
from strategy_index_weighting import determine_weighting
from etf_layer import etf_decision
from risk_guard import check_global_risk
from position_engine import calculate_position_size, dca_size
from telegram_alert import send_alert
from data_collector import get_price
import pandas as pd

# Load configuration from config.json
with open("config.json", "r") as f:
    config = json.load(f)

# Initialize exchange
exchange = ccxt.binance({
    'apiKey': config['api_key'],
    'secret': config['secret_key'],
})

# Initialize strategy state
position_open = False
last_price_eth = None
last_price_btc = None

# Strategy main loop
def main():
    global position_open, last_price_eth, last_price_btc
    print("AHA-X Strategy Starting...")

    while True:
        try:
            # Get the current prices of ETH and BTC
            price_eth = get_price(exchange, config["symbol_long"])
            price_btc = get_price(exchange, config["symbol_short"])

            if price_eth is None or price_btc is None:
                continue

            # Calculate z-score
            zscore = calculate_zscore([price_eth], [price_btc])

            # Get the RSI values (for demonstration purposes, you can replace with actual API calls)
            rsi_eth = exchange.fetch_rsi(config["symbol_long"])
            rsi_btc = exchange.fetch_rsi(config["symbol_short"])

            # Check if risk limits are exceeded
            if check_global_risk():
                print("[RISK] Risk threshold exceeded. Stopping strategy.")
                send_alert("Risk limit exceeded, strategy halted.")
                break

            # Get the ETF decision based on current market conditions
            etf_decision_result = etf_decision(zscore, price_eth, price_btc, rsi_eth, rsi_btc)

            # Hedge strategy: Covered call or inverse short
            hedge_signal = etf_decision_result['hedge']
            if hedge_signal:
                send_alert(f"Hedge signal: {hedge_signal}")
                print(f"Hedge signal: {hedge_signal}")
                # Execute hedge strategy logic here (buy or sell hedge)

            # Inverse strategy: Short ETH or Short BTC
            inverse_signal_result = etf_decision_result['inverse']
            if inverse_signal_result:
                send_alert(f"Inverse signal: {inverse_signal_result}")
                print(f"Inverse signal: {inverse_signal_result}")
                # Execute inverse strategy logic here (short BTC or ETH)

            # Momentum weighting adjustment
            weights = etf_decision_result['weights']
            print(f"Adjusting weights: {weights}")
            # Adjust position sizes based on calculated weights

            # Calculate position size based on risk level
            position_size = calculate_position_size(exchange.balance, config["risk_level"])

            # DCA adjustment
            position_size = dca_size(position_size, zscore)

            # 삼중 스크린 필터링 (삼중 스크린이 VALID일 경우에만 z-score 신호를 처리)
            if triple_screen_signal(price_eth, price_btc) == "VALID":
                # Execute trade based on z-score signal
                if zscore_signal(zscore) == "LONG" and not position_open:
                    print("Long position triggered.")
                    position_open = True
                    send_alert("Long position opened")
                    # Place long order on exchange

                elif zscore_signal(zscore) == "SHORT" and not position_open:
                    print("Short position triggered.")
                    position_open = True
                    send_alert("Short position opened")
                    # Place short order on exchange
            else:
                print("삼중 스크린 필터에 의해 진입 보류")

            # 터틀 트레이딩 신호 처리
            turtle_signal_result = turtle_signal(price_eth, price_btc)
            if turtle_signal_result == "LONG" and not position_open:
                print("Turtle long position triggered.")
                position_open = True
                send_alert("Turtle long position opened")
                # Place long order on exchange

            elif turtle_signal_result == "SHORT" and not position_open:
                print("Turtle short position triggered.")
                position_open = True
                send_alert("Turtle short position opened")
                # Place short order on exchange

            # DCA 및 터틀 진입 우선순위 처리
            if zscore_signal(zscore) == "LONG" and dca_entry_condition_met():
                if turtle_signal(price_eth, price_btc) == "LONG":
                    print("터틀 트레이딩 신호 우선, DCA 진입 연기")
                    enter_long_position()
                else:
                    enter_position()  # DCA 진입

            # 익절 후 터틀 진입 제한
            if position_profit > profit_threshold:
                close_position()  # 포지션 종료 (익절)
                if turtle_signal(price_eth, price_btc) == "LONG":
                    print("익절 후 터틀 진입")
                    enter_long_position()
                else:
                    print("익절 후 터틀 진입을 대기")

            # 리스크 관리
            if check_global_risk():
                print("[RISK] Risk threshold exceeded. Stopping strategy.")
                exit_all_positions()  # 모든 포지션 종료
                send_alert("Risk limit exceeded, strategy halted.")
                break  # 전략 종료

            # Sleep before the next iteration
            time.sleep(60)  # adjust sleep time as needed

        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(60)  # Sleep and retry in case of error

# Run the strategy
if __name__ == "__main__":
    main()
