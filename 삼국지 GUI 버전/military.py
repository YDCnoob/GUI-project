
from constants import (RECRUIT_COST, TRAIN_COST_PER_100, TRAIN_GAIN, MAX_TRAINING,)

def recruit(city, recruit_count=None):
    print("==============================")
    print("징병")
    print("==============================")
    print(f"현재 병력: {city['troops']}")
    print(f"현재 식량: {city['food']}")
    print(f"병사 100명당 식량 " f"{RECRUIT_COST}이 필요합니다.")

    # 실제 게임에서는 직접 입력
    if recruit_count is None:
        recruit_count = int(input("징병할 병력 수: "))

    if recruit_count <= 0:
        print("잘못된 병력 수입니다.")
        return 0, 0

    if recruit_count % 100 != 0:
        print("징병은 100명 단위로 가능합니다.")
        return 0, 0

    food_cost = recruit_count // 100 * RECRUIT_COST

    if city["food"] < food_cost:
        print("식량이 부족합니다.")
        return 0, 0

    city["food"] -= food_cost
    city["troops"] += recruit_count

    print(f"병력 +{recruit_count}")
    print(f"식량 -{food_cost}")
    print(f"현재 병력: {city['troops']}")
    print(f"현재 식량: {city['food']}")

    return food_cost, recruit_count

def get_training_cost(city):
    return (
        TRAIN_COST_PER_100
        * city["troops"]
        // 100
    )

def train_army(city):
    if city["troops"] <= 0:
        print("훈련할 병력이 없습니다.")
        return 0, 0

    if city["training"] >= MAX_TRAINING:
        print("훈련도가 이미 최대입니다.")
        return 0, 0

    training_cost = get_training_cost(city)

    if city["gold"] < training_cost:
        print("금이 부족합니다.")
        return 0, 0

    city["gold"] -= training_cost

    old_training = city["training"]

    city["training"] += TRAIN_GAIN

    if city["training"] > MAX_TRAINING:
        city["training"] = MAX_TRAINING

    training_gain = (
        city["training"]
        - old_training
    )

    print(f"금 -{training_cost}")
    print(f"훈련도 +{training_gain}")

    return training_cost, training_gain

def battle(defender_city, attacking_troops):

    defending_troops = defender_city["troops"]

    if attacking_troops > defending_troops:

        attacker_loss = int(attacking_troops * 0.2)

        remaining_troops = (
            attacking_troops - attacker_loss
        )

        defender_city["troops"] = 0

        return {
            "result": "win",
            "attacker_loss": attacker_loss,
            "defender_loss": defending_troops,
            "remaining_troops": remaining_troops,
        }

    else:

        attacker_loss = int(attacking_troops * 0.5)
        defender_loss = int(defending_troops * 0.2)

        remaining_troops = (
            attacking_troops - attacker_loss
        )

        defender_city["troops"] -= defender_loss

        return {
            "result": "lose",
            "attacker_loss": attacker_loss,
            "defender_loss": defender_loss,
            "remaining_troops": remaining_troops,
        }

def transport_troops(departure, arrival, move_troops):
    if move_troops < 100:
        return False

    if move_troops > departure["troops"]:
        return False

    departure["troops"] -= move_troops
    arrival["troops"] += move_troops

    return True