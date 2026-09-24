
from constants import BASE_GROWTH_RATE

def dev_agri(city, ap):
    if ap <= 0:
        print("행동력이 부족합니다.")
        return ap, 0, 0

    if city["gold"] < 1000:
        print("국고가 부족합니다.")
        return ap, 0, 0

    print("농업 개발을 실행합니다.")

    city["gold"] -= 1000
    city["agriculture"] += 5

    ap -= 1

    print("국고 -1000")
    print("농업 +5")
    print(f"현재 농업: {city['agriculture']}")
    print(f"남은 행동력: {ap}")

    return ap, 1000, 5

def dev_commerce(city, ap): # 도시 상업 수치 개발
    if ap <= 0:
        print("행동력이 부족합니다.")
        return ap, 0, 0

    if city["gold"] < 1000:
        print("국고가 부족합니다.")
        return ap, 0, 0

    print("상업 개발을 실행합니다.")

    city["gold"] -= 1000
    city["commerce"] += 5

    ap -= 1

    print("국고 -1000")
    print("상업 +5")
    print(f"현재 상업: {city['commerce']}")
    print(f"남은 행동력: {ap}")

    return ap, 1000, 5

def get_monthly_food(city):
    return max(city["population"] // 5, 1)

def get_food_months(city):
    monthly_food = get_monthly_food(city)
    food_months = city["food"] / monthly_food

    return food_months

def get_food_production(city):
    return city["agriculture"] * 30

def produce_food(city):
    food_production = get_food_production(city)

    city["food"] += food_production

    print(f"식량 생산: +{food_production}")

    return food_production

def consume_food(city):
    consume = city["population"] // 5
    purchase_cost = 0

    if city["food"] < consume:
        print("식량이 부족합니다.")

        shortage = consume - city["food"]
        # 필요한 구매 횟수
        required_purchase_count = (shortage + 2999) // 3000

        # 현재 돈으로 가능한 구매 횟수
        affordable_purchase_count = max(city["gold"] // 1000, 0)
        # 실제 구매 횟수
        purchase_count = min(required_purchase_count, affordable_purchase_count)

        if purchase_count > 0:
            purchased_food = purchase_count * 3000
            purchase_cost = purchase_count * 1000

            city["gold"] -= purchase_cost
            city["food"] += purchased_food

            print(f"외부에서 식량 {purchased_food} 구매")
            print(f"구매 비용: {purchase_cost}")
        else:
            print("식량을 구매할 국고가 없습니다.")

    # 실제 소비 가능한 양
    actual_consume = min(city["food"], consume)

    city["food"] -= actual_consume

    # 실제로 식량을 다 먹지 못했을 때만 치안 감소
    if actual_consume < consume:
        old_order = city["public_order"]

        city["public_order"] -= 3

        if city["public_order"] < 0:
            city["public_order"] = 0

        order_loss = old_order - city["public_order"]

        if order_loss > 0:
            print(f"식량 부족으로 인한 공공질서 -{order_loss} 감소.")
        else:
            print("공공질서는 이미 0입니다.")

    print(f"현재 공공질서: {city['public_order']}")
    print(f"필요 식량: {consume}")
    print(f"실제 소비량: {actual_consume}")

    return purchase_cost

def tax(city): # 세금
    base_tax = city["population"] // 100 * 7

    if city["public_order"] >= 80:
        tax_rate = 1.2
    elif city["public_order"] >= 60:
        tax_rate = 1.0
    elif city["public_order"] >= 40:
        tax_rate = 0.8
    elif city["public_order"] >= 20:
        tax_rate = 0.6
    else:
        tax_rate = 0.4

    # 상업 보정
    commerce_modifier = 1 + (city["commerce"] / 100 * 0.001)

    taxpay = int(base_tax * tax_rate * commerce_modifier)
    
    city["gold"] += taxpay

    print(f"기본 세금: {base_tax}")
    print(f"징수 효율: {tax_rate * 100:.0f}%")
    print(f"세금 수입: {taxpay}")

    return taxpay

def population_growth(city): # 인구 변화
    growth_rate = BASE_GROWTH_RATE

    # 현재 보유 식량이 몇개월분인지 계산
    food_months = get_food_months(city)

    # 식량 보정
    if food_months >= 12:
        food_modifier = 0.001
    elif food_months >= 6:
        food_modifier = 0.0005
    elif food_months >= 3:
        food_modifier = -0.001
    elif food_months >= 1:
        food_modifier = -0.0015
    else:
        food_modifier = -0.003

    # 공공질서 보정
    if city["public_order"] >= 90:
        order_modifier = 0.001
    elif city["public_order"] >= 80:
        order_modifier = 0.0005
    elif city["public_order"] >= 60:
        order_modifier = 0
    elif city["public_order"] >= 40:
        order_modifier = -0.001
    elif city["public_order"] >= 20:
        order_modifier = -0.002
    else:
        order_modifier = -0.003

    # 최종 성장률
    growth_rate += food_modifier
    growth_rate += order_modifier

    # 실제 인구 변화량
    growth = int(city["population"] * growth_rate)
    city["population"] += growth

    print(f"식량 비축량: {food_months:.1f}개월")
    print(f"식량 보정: {food_modifier:+.2%}")
    print(f"공공질서 보정: {order_modifier:+.2%}")
    print(f"최종 성장률: {growth_rate:+.2%}")
    print(f"인구 변화: {growth:+}")

    return {
        "growth": growth,
        "growth_rate": growth_rate,
        "food_months": food_months,
        "food_modifier": food_modifier,
        "order_modifier": order_modifier
    }

def improve_order(city, ap): # 공공 질서 변화
    if ap <= 0:
        print("행동력이 부족합니다.")
        return ap, 0, 0
    
    if city["gold"] < 1000:
        print("국고가 부족합니다.")
        return ap, 0, 0
    
    if city["public_order"] >= 100:
        print("치안이 최대치입니다.")
        return ap, 0, 0
    
    old_order = city["public_order"]

    city["gold"] -= 1000
    city["public_order"] += 5

    if city["public_order"] > 100:
        city["public_order"] = 100

    ap -= 1

    order_gain = city["public_order"] - old_order

    print(f"치안 강화: +{order_gain}")
    print(f"현재 치안: {city['public_order']}")

    return ap, 1000, order_gain

def decrease_order(city):
    old_order = city["public_order"]

    city["public_order"] -= 1

    if city["public_order"] < 0:
        city["public_order"] = 0

    order_change = city["public_order"] - old_order

    print(f"공공질서 자연 감소: {order_change}")

    return order_change