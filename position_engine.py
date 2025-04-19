# position_engine.py

def calculate_position_size(balance, risk_level="low"):
    if risk_level == "low":
        return balance * 0.03  # 3%
    elif risk_level == "medium":
        return balance * 0.05
    elif risk_level == "high":
        return balance * 0.1
    return balance * 0.03  # default

def dca_size(base_size, zscore):
    if abs(zscore) >= 3:
        return base_size * 2.0
    elif abs(zscore) >= 2.5:
        return base_size * 1.5
    return base_size
