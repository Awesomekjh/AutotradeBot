# risk_guard.py

portfolio_status = {
    "daily_loss": 0.0,
    "weekly_loss": 0.0,
    "cumulative_loss": 0.0,
    "strategy_locked": False
}

def check_global_risk():
    if portfolio_status["daily_loss"] <= -0.03:
        portfolio_status["strategy_locked"] = True
    if portfolio_status["weekly_loss"] <= -0.05:
        portfolio_status["strategy_locked"] = True
    if portfolio_status["cumulative_loss"] <= -0.10:
        portfolio_status["strategy_locked"] = True
    return portfolio_status["strategy_locked"]

def update_loss(loss_pct):
    portfolio_status["daily_loss"] += loss_pct
    portfolio_status["weekly_loss"] += loss_pct
    portfolio_status["cumulative_loss"] += loss_pct
