# strategy_coveredcall.py

def coveredcall_adjustment(entry_price, current_price, threshold=0.06):
    change = (current_price - entry_price) / entry_price
    if change >= threshold:
        return "HEDGE_SHORT"
    elif change <= -threshold:
        return "HEDGE_LONG"
    return None
