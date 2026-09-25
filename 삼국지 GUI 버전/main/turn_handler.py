from core import constants
from core import officer
from core import turn

def handle_end_turn(
    cities,
    player_faction,
    year,
    month,
):
    total_food = 0
    total_tax = 0
    total_population = 0

    for city_data in cities:
        city_faction = officer.get_city_faction(city_data)

        # 플레이어 소유 도시만 처리
        if city_faction == player_faction:
            result = turn.process_city_turn(city_data)

            total_food += result["food_production"]
            total_tax += result["tax_income"]
            total_population += result["population_gain"]

            # 전체 행동 초기화
            city_data["recruited_this_turn"] = False
            city_data["trained_this_turn"] = False
            city_data["sortied_this_turn"] = False
            city_data["moved_this_turn"] = False

            # 도시별 행동력 회복
            city_data["ap"] = constants.MAX_AP

    # 날짜 변경
    year, month = turn.end_turn(
        year,
        month,
    )

    popup_message = (
        f"{year}년 {month}월\n"
        f"전체 식량 생산 +{total_food:,}\n"
        f"전체 세금 수입 +{total_tax:,}\n"
        f"전체 인구 변화 {total_population:+,}"
    )

    return year, month, popup_message