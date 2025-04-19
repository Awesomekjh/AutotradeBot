# strategy_index_weighting.py

def determine_weighting(rsi_eth, rsi_btc, base_weight=1.0):
    if rsi_eth > rsi_btc:
        return {"ETH": base_weight * 1.5, "BTC": base_weight * 0.5}
    elif rsi_btc > rsi_eth:
        return {"ETH": base_weight * 0.5, "BTC": base_weight * 1.5}
    else:
        return {"ETH": base_weight, "BTC": base_weight}
