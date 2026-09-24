import pygame
import ui
import city
import constants
import domestic
import turn
import military
import officer

# ==============================
# pygame 초기화
# ==============================

pygame.init()

# ==============================
# 화면 설정
# ==============================

BASE_WIDTH = 1024
BASE_HEIGHT = 768

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# 실제 윈도우
window = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    pygame.RESIZABLE,
)

# 게임은 항상 이 크기에 그린다.
screen = pygame.Surface(
    (BASE_WIDTH, BASE_HEIGHT)
)

pygame.display.set_caption("삼국지")

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    "malgungothic",
    20,
)


# ==============================
# 게임 데이터
# ==============================

year = constants.START_YEAR
month = constants.START_MONTH

current_city = city.default_city
selected_city = city.cities.index(current_city)
PLAYER_FACTION = "촉"

# ==============================
# 메인 메뉴
# ==============================

menu_items = [
    "도시",
    "내정",
    "군사",
    "외교",
    "정보",
    "턴 종료",
]

selected_menu = 0


# ==============================
# 내정 메뉴
# ==============================

domestic_items = [
    "농업 개발",
    "상업 개발",
    "치안 강화",
    "돌아가기",
]

selected_domestic = 0


# ==============================
# 군사 메뉴
# ==============================

military_items = [
    "모병",
    "훈련",
    "출진",
    "병력 이동",
    "돌아가기",
    
]

selected_military = 0


# ==============================
# 모병 수량
# ==============================

recruit_count = 100
recruit_count_input = ""

# ==============================
# 출진
# ==============================

sortie_targets = []
selected_sortie_target = 0

sortie_target_city = None
sortie_troops = 100
sortie_troops_input = ""

# ==============================
# 통치자 선택
# ==============================

governor_candidates = []
selected_governor = 0
conquered_city = None

# ==============================
# 병력 이동
# ==============================

transport_targets = []
selected_transport_target = 0

transport_target_city = None
move_troops = 0
move_troops_input = ""


# ==============================
# 화면 상태
# ==============================

current_menu = "main"
popup_message = None


# ==============================
# 메인 루프
# ==============================

running = True

while running:

    # ==============================
    # 1. 입력 처리
    # ==============================

    for event in pygame.event.get():

        # ==============================
        # 창 닫기
        # ==============================

        if event.type == pygame.QUIT:
            running = False


        # ==============================
        # 키 입력
        # ==============================

        if event.type == pygame.KEYDOWN:

            # ==============================
            # 결과 팝업
            # ==============================

            if popup_message is not None:

                if (
                    event.key == pygame.K_RETURN
                    or event.key == pygame.K_ESCAPE
                ):
                    popup_message = None

                # 팝업이 떠 있는 동안
                # 다른 입력은 처리하지 않는다.
                continue


            # ==============================
            # 메인 메뉴
            # ==============================

            if current_menu == "main":

                # 왼쪽
                if event.key == pygame.K_LEFT:
                    selected_menu -= 1
                    selected_menu %= len(menu_items)

                # 오른쪽
                elif event.key == pygame.K_RIGHT:
                    selected_menu += 1
                    selected_menu %= len(menu_items)

                # 결정
                elif event.key == pygame.K_RETURN:

                    selected_item = menu_items[selected_menu]

                    # ======================
                    # 도시
                    # ======================

                    if selected_item == "도시":

                        current_menu = "city_select"
                        selected_city = city.cities.index(
                            current_city
                        )

                    # ======================
                    # 내정
                    # ======================

                    elif selected_item == "내정":

                        current_faction = officer.get_city_faction(current_city)

                        if current_faction != PLAYER_FACTION:
                            popup_message = (
                                "내정 불가\n"
                                "다른 세력의 도시 입니다."
                            )
                        else:
                            current_menu = "domestic"
                            selected_domestic = 0

                    # ======================
                    # 군사
                    # ======================

                    elif selected_item == "군사":

                        current_faction = officer.get_city_faction(current_city)

                        if current_faction != PLAYER_FACTION:
                            popup_message = (
                                "군사 명령 불가\n"
                                "다른 세력의 도시입니다."
                            )
                        else:
                            current_menu = "military"
                            selected_military = 0

                    # ======================
                    # 외교
                    # ======================

                    elif selected_item == "외교":

                        popup_message = (
                            "외교\n"
                            "아직 GUI 연결 전입니다."
                        )

                    # ======================
                    # 정보
                    # ======================

                    elif selected_item == "정보":

                        popup_message = (
                            "정보\n"
                            "아직 GUI 연결 전입니다."
                        )

                    # ======================
                    # 턴 종료
                    # ======================

                    elif selected_item == "턴 종료":

                        total_food = 0
                        total_tax = 0
                        total_population = 0

                        for city_data in city.cities:
                            city_faction = officer.get_city_faction(city_data)

                            # 플레이어 소유 도시만 처리
                            if city_faction == PLAYER_FACTION:
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

                        # 날짜는 딱 한 번만 변경
                        year, month = turn.end_turn(year, month)

                        popup_message = (
                            f"{year}년 {month}월\n"
                            f"전체 식량 생산 "
                            f"+{total_food:,}\n"
                            f"전체 세금 수입 "
                            f"+{total_tax:,}\n"
                            f"전체 인구 변화 "
                            f"{total_population:+,}"
                        )

            # ==============================
            # 통치자 선택
            # ==============================

            elif current_menu == "governor_select":

                if event.key == pygame.K_UP:
                    selected_governor -= 1
                    selected_governor %= len(governor_candidates)

                elif event.key == pygame.K_DOWN:
                    selected_governor += 1
                    selected_governor %= len(governor_candidates)

                elif event.key == pygame.K_RETURN:
                    new_governor = governor_candidates[selected_governor]
                    conquered_city["governor"] = (new_governor["name"])

                    popup_message = (
                        "통치자 임명 완료\n"
                        f"{conquered_city['name']} : "
                        f"{new_governor['name']}"
                    )
                    current_menu = "main"

            # ==============================
            # 도시 선택
            # ==============================

            elif current_menu == "city_select":

                # 이전 도시
                if event.key == pygame.K_LEFT:

                    selected_city -= 1
                    selected_city %= len(city.cities)

                    current_city = city.cities[
                        selected_city
                    ]

                # 다음 도시
                elif event.key == pygame.K_RIGHT:

                    selected_city += 1
                    selected_city %= len(city.cities)

                    current_city = city.cities[
                        selected_city
                    ]

                # 선택 완료
                elif event.key == pygame.K_RETURN:

                    current_menu = "main"

                # 돌아가기
                elif event.key == pygame.K_ESCAPE:

                    current_menu = "main"


            # ==============================
            # 내정 메뉴
            # ==============================

            elif current_menu == "domestic":

                # 위
                if event.key == pygame.K_UP:
                    selected_domestic -= 1
                    selected_domestic %= len(domestic_items)

                # 아래
                elif event.key == pygame.K_DOWN:
                    selected_domestic += 1
                    selected_domestic %= len(domestic_items)

                # ESC
                elif event.key == pygame.K_ESCAPE:
                    current_menu = "main"

                # Enter
                elif event.key == pygame.K_RETURN:

                    selected_item = domestic_items[
                        selected_domestic
                    ]

                    # ======================
                    # 농업 개발
                    # ======================

                    if selected_item == "농업 개발":

                        current_city["ap"], cost, gain = (
                            domestic.dev_agri(
                                current_city,
                                current_city["ap"],
                            )
                        )

                        if gain > 0:

                            popup_message = (
                                "농업 개발 완료\n"
                                f"금 -{cost:,}\n"
                                f"농업 +{gain}"
                            )

                        else:

                            popup_message = (
                                "농업 개발 실패\n"
                                "실행할 수 없습니다."
                            )

                    # ======================
                    # 상업 개발
                    # ======================

                    elif selected_item == "상업 개발":

                        current_city["ap"], cost, gain = (
                            domestic.dev_commerce(
                                current_city,
                                current_city["ap"],
                            )
                        )

                        if gain > 0:

                            popup_message = (
                                "상업 개발 완료\n"
                                f"금 -{cost:,}\n"
                                f"상업 +{gain}"
                            )

                        else:

                            popup_message = (
                                "상업 개발 실패\n"
                                "실행할 수 없습니다."
                            )

                    # ======================
                    # 치안 강화
                    # ======================

                    elif selected_item == "치안 강화":

                        current_city["ap"], cost, gain = (
                            domestic.improve_order(
                                current_city,
                                current_city["ap"],
                            )
                        )

                        if gain > 0:

                            popup_message = (
                                "치안 강화 완료\n"
                                f"금 -{cost:,}\n"
                                f"치안 +{gain}"
                            )

                        else:

                            popup_message = (
                                "치안 강화 실패\n"
                                "실행할 수 없습니다."
                            )

                    # ======================
                    # 돌아가기
                    # ======================

                    elif selected_item == "돌아가기":

                        current_menu = "main"


            # ==============================
            # 군사 메뉴
            # ==============================

            elif current_menu == "military":

                # 위
                if event.key == pygame.K_UP:
                    selected_military -= 1
                    selected_military %= len(military_items)

                # 아래
                elif event.key == pygame.K_DOWN:
                    selected_military += 1
                    selected_military %= len(military_items)

                # ESC
                elif event.key == pygame.K_ESCAPE:
                    current_menu = "main"

                # Enter
                elif event.key == pygame.K_RETURN:

                    selected_item = military_items[
                        selected_military
                    ]

                    # ======================
                    # 모병
                    # ======================

                    if selected_item == "모병":

                        if current_city[
                            "recruited_this_turn"
                        ]:

                            popup_message = (
                                "모병 실패\n"
                                "이번 턴에는 이미 모병했습니다."
                            )

                        else:

                            recruit_count = 0
                            recruit_count_input = ""
                            current_menu = "recruit"

                    # ======================
                    # 훈련
                    # ======================

                    elif selected_item == "훈련":

                        if current_city[
                            "trained_this_turn"
                        ]:

                            popup_message = (
                                "훈련 실패\n"
                                "이번 턴에는 이미 훈련했습니다."
                            )

                        else:

                            cost, gain = military.train_army(
                                current_city
                            )

                            if gain > 0:

                                current_city[
                                    "trained_this_turn"
                                ] = True

                                popup_message = (
                                    "훈련 완료\n"
                                    f"금 -{cost:,}\n"
                                    f"훈련도 +{gain}"
                                )

                            else:

                                popup_message = (
                                    "훈련 실패\n"
                                    "훈련할 수 없습니다."
                                )

                    # ======================
                    # 출진
                    # ======================

                    elif selected_item == "출진":
                        if current_city["sortied_this_turn"]:
                            popup_message = (
                                "출진 불가\n"
                                "이번 턴에 이미 출정 했습니다."
                            )

                        else:
                            neighbors = city.get_neighbor_cities(current_city)
                            sortie_targets = []

                            for target_city in neighbors:
                                target_faction = (officer.get_city_faction(target_city))

                                # 같은 세력 도시는 공격 대상 제외
                                if target_faction != PLAYER_FACTION:
                                    sortie_targets.append(target_city)

                            if not sortie_targets:
                                popup_message = (
                                    "출진 불가\n"
                                    "공격 가능한 인접 도시가 없습니다"
                                )
                            else:
                                selected_sortie_target = 0
                                current_menu = "sortie_target"

                    # ======================
                    # 병력 이동
                    # ======================

                    elif selected_item == "병력 이동":
                        if current_city["moved_this_turn"]:
                            popup_message = (
                                "병력 이동 불가\n"
                                "이번 턴에는 이미 병력을 이동 했습니다."
                            )
                        else:
                            neighbors = city.get_neighbor_cities(current_city)

                            transport_targets = []
                            for target_city in neighbors:
                                target_faction = (officer.get_city_faction(target_city))

                                # 같은 세력 도시만 이동 가능
                                if target_faction == PLAYER_FACTION:
                                    transport_targets.append(target_city)

                            if not transport_targets:
                                popup_message = (
                                    "병력 이동 불가\n"
                                    "인접한 아군 도시가 없습니다."
                                )
                            else:
                                selected_transport_target = 0
                                current_menu = "transport_target"

                    # ======================
                    # 돌아가기
                    # ======================

                    elif selected_item == "돌아가기":

                        current_menu = "main"


            # ==============================
            # 모병 수량 선택
            # ==============================

            elif current_menu == "recruit":
                # 숫자 직접 입력
                if pygame.K_0 <= event.key <= pygame.K_9:
                    recruit_count_input += event.unicode
                    if recruit_count_input:
                        recruit_count = int(recruit_count_input)
                # 한 자리 삭제
                elif event.key == pygame.K_BACKSPACE:
                    recruit_count_input = (recruit_count_input[:-1])

                    if recruit_count_input:
                        recruit_count = int(recruit_count_input)
                    else:
                        recruit_count = 0

                # 100명 감소
                if event.key == pygame.K_LEFT:

                    recruit_count -= 100

                    if recruit_count < 100:
                        recruit_count = 100

                # 100명 증가
                elif event.key == pygame.K_RIGHT:

                    recruit_count += 100

                # 취소
                elif event.key == pygame.K_ESCAPE:

                    current_menu = "military"

                # 모병 실행
                elif event.key == pygame.K_RETURN:

                    cost, recruited = military.recruit(
                        current_city,
                        recruit_count,
                    )

                    if recruited > 0:

                        current_city[
                            "recruited_this_turn"
                        ] = True

                        popup_message = (
                            "모병 완료\n"
                            f"병력 +{recruited:,}\n"
                            f"식량 -{cost:,}"
                        )

                        current_menu = "military"

                    else:

                        popup_message = (
                            "모병 실패\n"
                            "모병할 수 없습니다."
                        )

            # ==============================
            # 출진 대상 선택
            # ==============================
            elif current_menu == "sortie_target":

                # 위
                if event.key == pygame.K_UP:

                    selected_sortie_target -= 1
                    selected_sortie_target %= len(sortie_targets)

                # 아래
                elif event.key == pygame.K_DOWN:

                    selected_sortie_target += 1
                    selected_sortie_target %= len(
                    sortie_targets
                )

                # 취소
                elif event.key == pygame.K_ESCAPE:

                    current_menu = "military"

                # 대상 결정
                elif event.key == pygame.K_RETURN:

                    sortie_target_city = sortie_targets[selected_sortie_target]

                    if current_city["troops"] < 100:
                        popup_message = (
                            "출진 불가\n"
                            "출진할 병력이 부족합니다."
                        )

                        current_menu = "military"

                    else:
                        sortie_troops = 100
                        current_menu = "sortie_troops"

            # ==============================
            # 출진 병력 선택
            # ==============================

            elif current_menu == "sortie_troops":
                # 숫자 직접 입력
                if pygame.K_0 <= event.key <= pygame.K_9:
                    number = event.unicode
                    sortie_troops_input += number
                    if sortie_troops_input:
                        sortie_troops = int(sortie_troops_input)

                    # 현재 도시 병력보다 많으면 제한
                    if sortie_troops > current_city["troops"]:
                        sortie_troops = current_city["troops"]
                        sortie_troops_input = str(sortie_troops)

                # 한 자리 삭제
                elif event.key == pygame.K_BACKSPACE:
                    sortie_troops_input = (sortie_troops_input[:-1])
                    if sortie_troops_input:
                        sortie_troops = int(sortie_troops_input)
                    else:
                        sortie_troops = 0

                # 100명 감소
                if event.key == pygame.K_LEFT:
                    sortie_troops -= 100
                    if sortie_troops < 100:
                        sortie_troops = 100

                # 100명 증가
                elif event.key == pygame.K_RIGHT:
                    sortie_troops += 100
                    if sortie_troops > current_city["troops"]:
                        sortie_troops = current_city["troops"]

                 # 취소
                elif event.key == pygame.K_ESCAPE:
                    current_menu = "sortie_target"

                # 결정
                elif event.key == pygame.K_RETURN:
                    if sortie_troops < 100:
                        popup_message = (
                            "출진 불가\n"
                            "최소 100명 이상 입력하십시오."
                        )

                    # 100명 단위 검사
                    elif sortie_troops % 100 != 0:
                        popup_message = (
                            "출진 불가\n"
                            "병력은 100명 단위로 입력하십시오."
                        )
                    else:
                        result = military.battle(
                            sortie_target_city,
                            sortie_troops
                        )

                        # 출진 병력은 일단 출진 도시에서 빠짐.
                        current_city["troops"] -= sortie_troops
                    
                        # 승리
                        if result["result"] == "win":

                            # 살아 남은 병력이 공격 도시 주둔
                            sortie_target_city["troops"] = (result["remaining_troops"])

                            # 점령 처리
                            governor_candidates = (officer.get_available_governors(city.cities, PLAYER_FACTION))

                            conquered_city = sortie_target_city
                            conquered_city["ap"] = 0
                            selected_governor = 0

                            current_city["sortied_this_turn"] = True

                            popup_message = (
                                "전투 승리!\n"
                                f"{sortie_target_city['name']} 점령!"
                            )
                            current_menu = "governor_select"
                        
                        # 패배
                        else:
                            # 살아남은 병력은 출발 도시로 복귀
                            current_city["troops"] += result["remaining_troops"]
                            current_city["sortied_this_turn"] = True

                            popup_message = (
                                "전투 패배\n"
                                f"공격군 피해 : "
                                f"{result['attacker_loss']:,}명\n"
                                f"방어군 피해 : "
                                f"{result['defender_loss']:,}명"
                            )
                            current_menu = "military"

            # ==============================
            # 이송 병력 선택
            # ==============================
            elif current_menu == "transport_target":

                # 위
                if event.key == pygame.K_UP:
                    selected_transport_target -= 1
                    selected_transport_target %= len(
                    transport_targets
                )

                # 아래
                elif event.key == pygame.K_DOWN:
                    selected_transport_target += 1
                    selected_transport_target %= len(
                    transport_targets
                )

                # 취소
                elif event.key == pygame.K_ESCAPE:
                    current_menu = "military"

                # 대상 결정
                elif event.key == pygame.K_RETURN:
                    transport_target_city = (transport_targets[selected_transport_target])

                    if current_city["troops"] < 100:
                        popup_message = (
                            "병력 이동 불가\n"
                            "이동할 병력이 부족합니다."
                        )   
                        current_menu = "military"
                    else:
                        move_troops = 0
                        move_troops_input = ""
                        current_menu = "transport_troops"
            # ==============================
            # 이송 병력 수 선택
            # ==============================

            elif current_menu == "transport_troops":

                # 숫자 직접 입력
                if pygame.K_0 <= event.key <= pygame.K_9:
                    move_troops_input += event.unicode
                    if move_troops_input:
                        move_troops = int(
                        move_troops_input
                    )

                    # 현재 병력보다 많이 입력하면 제한
                    if move_troops > current_city["troops"]:
                        move_troops = current_city["troops"]
                        move_troops_input = str(
                            move_troops
                        )

                # 한 자리 삭제
                elif event.key == pygame.K_BACKSPACE:
                    move_troops_input = (move_troops_input[:-1])
                    if move_troops_input:
                        move_troops = int(
                        move_troops_input
                        )

                    else:
                        move_troops = 0

                # 100명 감소
                elif event.key == pygame.K_LEFT:
                    move_troops -= 100

                    if move_troops < 100:
                        move_troops = 100   
                    move_troops_input = str(move_troops)

                # 100명 증가
                elif event.key == pygame.K_RIGHT:
                    move_troops += 100

                    if move_troops > current_city["troops"]:
                        move_troops = current_city["troops"]

                    move_troops_input = str(move_troops)

                # 취소
                elif event.key == pygame.K_ESCAPE:
                    current_menu = "transport_target"

                # 병력 이동 실행
                elif event.key == pygame.K_RETURN:
                    if move_troops < 100:
                        popup_message = (
                            "병력 이동 불가\n"
                            "최소 100명부터 가능합니다."
                        )

                    elif move_troops % 100 != 0:
                        popup_message = (
                            "병력 이동 불가\n"
                            "병력은 100명 단위로 입력하십시오."
                        )

                    else:
                        success = military.transport_troops(
                            current_city,
                            transport_target_city,
                            move_troops,
                        )

                        if success:
                            current_city["moved_this_turn"] = True

                            popup_message = (
                                "병력 이동 완료\n"
                                f"{current_city['name']} → "
                                f"{transport_target_city['name']}\n"
                                f"{move_troops:,}명 이동"
                            )

                            current_menu = "military"

                        else:
                            popup_message = (
                                "병력 이동 실패\n"
                                "병력을 이동할 수 없습니다."
                            )



    # ==============================
    # 2. 화면 그리기
    # ==============================

    ui.draw_background(
        screen
    )


    # ==============================
    # 상단 정보
    # ==============================

    ui.draw_header(
        screen,
        font,
        year,
        month,
        current_city["ap"],
    )

    # ==============================
    # 도시 지도
    # ==============================

    ui.draw_map(
        screen,
        font,
        city.cities,
        current_city,
    )

    # ==============================
    # 선택 도시 간략 정보
    # ==============================

    faction = officer.get_city_faction(current_city)

    ui.draw_selected_city_info(
        screen,
        font,
        current_city,
        faction,
    )

    # ==============================
    # 메인 명령 메뉴
    # ==============================

    if popup_message is None:

        ui.draw_main_menu(
            screen,
            font,
            menu_items,
            selected_menu,
        )


    # ==============================
    # 내정 메뉴
    # ==============================

    if (
        current_menu == "domestic"
        and popup_message is None
    ):

        ui.draw_domestic_menu(
            screen,
            font,
            domestic_items,
            selected_domestic,
        )


    # ==============================
    # 군사 메뉴
    # ==============================

    if (
        current_menu == "military"
        and popup_message is None
    ):

        ui.draw_military_menu(
            screen,
            font,
            military_items,
            selected_military,
        )

    # ==============================
    # 출진 대상 선택
    # ==============================

    if (current_menu =="sortie_target" and popup_message is None):
         ui.draw_sortie_target_menu(
            screen,
            font,
            sortie_targets,
            selected_sortie_target,
        )

    # ==============================
    # 출진 병력 선택
    # ==============================

    if (current_menu == "sortie_troops" and popup_message is None):
        ui.draw_sortie_troops_menu(
            screen,
            font,
            current_city,
            sortie_target_city,
            sortie_troops,
        )

    # ==============================
    # 이송 위치 지정
    # ==============================
    
    if (
    current_menu == "transport_target"
    and popup_message is None
    ):
        ui.draw_transport_target_menu(
            screen,
            font,
            transport_targets,
            selected_transport_target,
        )

    # ==============================
    # 이송 병력 수량
    # ==============================

    if (
    current_menu == "transport_troops"
    and popup_message is None
    ):
        ui.draw_transport_troops_menu(
            screen,
            font,
            current_city,
            transport_target_city,
            move_troops,
        )

    # ==============================
    # 모병 수량 선택
    # ==============================

    if (
        current_menu == "recruit"
        and popup_message is None
    ):

        ui.draw_recruit_menu(
            screen,
            font,
            current_city,
            recruit_count,
        )


    # ==============================
    # 결과 팝업
    # ==============================

    if popup_message is not None:

        ui.draw_popup(
            screen,
            font,
            popup_message,
        )

    # ==============================
    # 통치자 선택
    # ==============================

    if (
        current_menu == "governor_select"
        and popup_message is None
    ):

        ui.draw_governor_select_menu(
            screen,
            font,
            conquered_city,
            governor_candidates,
            selected_governor,
        )

    # ==============================
    # 실제 창 크기에 맞춰 확대/축소
    # ==============================
    window_width, window_height = (window.get_size())

    scale = min(window_width/BASE_WIDTH, window_height/BASE_HEIGHT)
    scaled_width = max(1, int(BASE_WIDTH * scale))
    scaled_height = max(1, int(BASE_HEIGHT * scale))
    scaled_screen = pygame.transform.smoothscale(screen, (scaled_width, scaled_height),)

    # 남는 영역
    window.fill((0, 0, 0))

    offset_x = (window_width - scaled_width) // 2
    offset_y = (window_height - scaled_height) // 2
    window.blit(scaled_screen, (offset_x, offset_y),)

    # ==============================
    # 3. 화면 갱신
    # ==============================
    
    pygame.display.flip()


    # ==============================
    # 4. FPS 제한
    # ==============================

    clock.tick(60)


# ==============================
# pygame 종료
# ==============================

pygame.quit()
