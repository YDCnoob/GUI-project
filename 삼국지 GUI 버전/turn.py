
from domestic import (
    produce_food,
    consume_food,
    decrease_order,
    tax,
    population_growth,
)

def end_turn(year, month):
    print("턴을 종료합니다.")

    month += 1

    if month > 12:
        year += 1
        month = 1

    print(f"현재 날짜: {year}년 {month}월")

    return year, month


def process_city_turn(city):

    food_production = produce_food(city)
    purchase_cost = consume_food(city)
    decrease_order(city)
    tax_income = tax(city)
    population_result = population_growth(city)

    return {
        "food_production": food_production,
        "purchase_cost": purchase_cost,
        "tax_income": tax_income,
        "population_gain": population_result["growth"],
    }

