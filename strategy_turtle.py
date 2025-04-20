# strategy_turtle.py

def turtle_signal(price_eth, price_btc):
    """
    터틀 트레이딩 신호 생성 함수.
    - 가격이 일정 고점/저점을 돌파할 때 진입
    """
    high_55_day = get_55_day_high(price_eth)  # 예시: 55일 고점
    low_55_day = get_55_day_low(price_eth)    # 예시: 55일 저점

    if price_eth > high_55_day:
        return "LONG"
    elif price_eth < low_55_day:
        return "SHORT"
    else:
        return "NONE"
    
def get_55_day_high(price_eth):
    # 예시: 55일 고점
    return 3500

def get_55_day_low(price_eth):
    # 예시: 55일 저점
    return 2400
