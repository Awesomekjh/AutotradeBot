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

            # Execute trade based on z-score signal
            if zscore_signal(zscore) == "LONG" and not position_open:
                print("Long position triggered.")
                # Execute long trade logic here
                position_open = True
                # Place long order on exchange
                send_alert("Long position opened")

            elif zscore_signal(zscore) == "SHORT" and not position_open:
                print("Short position triggered.")
                # Execute short trade logic here
                position_open = True
                # Place short order on exchange
                send_alert("Short position opened")

            # Sleep before the next iteration (time delay between trading signals)
            time.sleep(60)  # adjust sleep time as needed

        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(60)  # Sleep and retry in case of error

# Run the strategy
if __name__ == "__main__":
    main()
