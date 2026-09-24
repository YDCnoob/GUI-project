
import constants

cities = [
    {
        "name": "성도",
        "governor": "유선",

        "neighbors": [
            "한중",
            "강하",
        ],
        "map_x" : 0,
        "map_y" : 1,
        "population": 50000,
        "food": 80000,
        "gold": 50000,

        "public_order": 80,
        "agriculture": 150,
        "commerce": 130,

        "troops": 10000,
        "training": 120,
        "ap" : constants.MAX_AP,

        "recruited_this_turn": False,
        "trained_this_turn": False,
        "sortied_this_turn": False,
        "moved_this_turn": False,
    },

    {
        "name": "한중",
        "governor": None,

        "neighbors": [
            "성도",
            "번성",
        ],
        "map_x" : 1,
        "map_y" : 0,
        "population": 30000,
        "food": 60000,
        "gold": 35000,

        "public_order": 70,
        "agriculture": 120,
        "commerce": 90,

        "troops": 8000,
        "training": 110,
        "ap" : constants.MAX_AP,

        "recruited_this_turn": False,
        "trained_this_turn": False,
        "sortied_this_turn": False,
        "moved_this_turn": False,
    },

    {
        "name": "번성",
        "governor": None,

        "neighbors": [
            "한중",
            "강하",
        ],
        "map_x" : 2,
        "map_y" : 1,
        "population": 45000,
        "food": 70000,
        "gold": 45000,

        "public_order": 75,
        "agriculture": 110,
        "commerce": 150,

        "troops": 9000,
        "training": 115,
        "ap" : constants.MAX_AP,

        "recruited_this_turn": False,
        "trained_this_turn": False,
        "sortied_this_turn": False,
        "moved_this_turn": False,
    },

    {
        "name": "강하",
        "governor": None,

        "neighbors": [
            "성도",
            "번성",
        ],
        "map_x" : 1,
        "map_y" : 2,
        "population": 25000,
        "food": 55000,
        "gold": 25000,

        "public_order": 65,
        "agriculture": 130,
        "commerce": 80,

        "troops": 6000,
        "training": 100,
        "ap" : constants.MAX_AP,

        "recruited_this_turn": False,
        "trained_this_turn": False,
        "sortied_this_turn": False,
        "moved_this_turn": False,
    },
]

def city_info(city):
    print("==============================")
    print(f"도시: {city['name']}")
    print(f"통치자: {city['governor']}")
    print(f"인구: {city['population']}")
    print(f"식량: {city['food']}")
    print(f"금: {city['gold']}")
    print(f"치안: {city['public_order']}")
    print(f"농업: {city['agriculture']}")
    print(f"상업: {city['commerce']}")
    print(f"병력: {city['troops']}")
    print(f"훈련도: {city['training']}")
    print("==============================")


# 선택한 도시의 정보 출력
def show_cities():
    if not cities:
        print("등록된 도시가 없습니다.")
        return

    for index, city_data in enumerate(
        cities,
        start=1
    ):
        print(
            f"{index}. "
            f"{city_data['name']} / "
            f"통치자: {city_data['governor']}"
        )

# 도시 찾는 함수
def find_city(name):
    for city in cities:
        if city["name"] == name:
            return city

    return None

# 인접 도시 찾는 함수
def get_neighbor_cities(city):
    neighbors = []

    for neighbor_name in city["neighbors"]:
        neighbor = find_city(neighbor_name)

        if neighbor is not None:
            neighbors.append(neighbor)

    return neighbors

# default 값으로 정해진 통치자 및 도시

default_city = cities[0]