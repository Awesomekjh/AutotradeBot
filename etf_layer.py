# etf_layer.py

from strategy_coveredcall import coveredcall_adjustment
from strategy_inverse import inverse_signal
from strategy_index_weighting import determine_weighting

def etf_decision(zscore, entry_price, current_price, rsi_eth, rsi_btc):
    # 수익 상단 보호
    hedge_signal = coveredcall_adjustment(entry_price, current_price)

    # 하락장 대응 인버스 전략
    inverse = inverse_signal(zscore, rsi_eth, rsi_btc)

    # 모멘텀 기반 비중 조절
    weights = determine_weighting(rsi_eth, rsi_btc)

    return {
        "hedge": hedge_signal,
        "inverse": inverse,
        "weights": weights
    }
