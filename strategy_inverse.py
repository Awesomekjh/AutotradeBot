# strategy_inverse.py
def inverse_signal(zscore, rsi_eth, rsi_btc, threshold=-2.0):
    if zscore < threshold:
        if rsi_eth < rsi_btc and rsi_eth < 30:
            return "SHORT_ETH"
        elif rsi_btc < rsi_eth and rsi_btc < 30:
            return "SHORT_BTC"
    return None
