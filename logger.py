# logger.py

import csv
from datetime import datetime

def log_trade(symbol, side, amount, price, filename="AHA_X_Strategy/trade_log.csv"):
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.utcnow(), symbol, side, amount, price])
    except Exception as e:
        print(f"[ERROR] 로그 저장 실패: {e}")
