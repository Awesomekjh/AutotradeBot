# strategy_triplescreen.py

def triple_screen_signal(price_eth, price_btc):
    """
    삼중 스크린 전략 신호 생성 함수.
    1. 장기 추세: 일간 차트
    2. 중기 조정: 4시간 차트
    3. 단기 타이밍: 1시간 차트
    """
    # 예시: 각 시간대별 신호를 계산한 후 결과를 반환
    long_term_trend = check_long_term_trend(price_eth)
    mid_term_correction = check_mid_term_correction(price_eth)
    short_term_timing = check_short_term_timing(price_eth)

    # "VALID"인 경우만 롱/숏 신호를 허용
    if long_term_trend == "UP" and mid_term_correction == "BUY" and short_term_timing == "BUY":
        return "VALID"
    else:
        return "INVALID"
    
def check_long_term_trend(price_eth):
    # 간단한 예시로, RSI나 이동평균을 사용할 수 있음
    return "UP" if price_eth > 3000 else "DOWN"

def check_mid_term_correction(price_eth):
    return "BUY" if price_eth > 2500 else "SELL"

def check_short_term_timing(price_eth):
    return "BUY" if price_eth > 2700 else "SELL"
