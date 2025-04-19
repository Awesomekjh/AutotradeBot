# data_collector.py
def get_price(exchange, symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"[ERROR] 가격 수집 실패 ({symbol}): {e}")
        return None
