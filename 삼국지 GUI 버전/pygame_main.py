import pygame
import ui
from core import city
from core import constants
from core import officer

import main

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

                        year, month, popup_message = (
                            main.turn_handler.handle_end_turn(
                                city.cities,
                                PLAYER_FACTION,
                                year,
                                month,
                            )
                        )

            # ==============================
            # 통치자 선택
            # ==============================

            elif current_menu == "governor_select":
                (
                    current_menu,
                    selected_governor,
                    popup_message,
                ) = main.city_select.handle_governor_select(
                    event,
                    governor_candidates,
                    selected_governor,
                    conquered_city,
                )

            # ==============================
            # 도시 선택
            # ==============================

            elif current_menu == "city_select":

                (
                    current_menu,
                    current_city,
                    selected_city,
                ) = main.city_select.handle_city_select(
                    event,
                    city.cities,
                    current_city,
                    selected_city,
                )

            # ==============================
            # 내정 선택
            # ==============================
            
            elif current_menu == "domestic":
                (
                    current_menu,
                    selected_domestic,
                    popup_message
                ) = main.domestic_menu.handle_domestic_menu(
                    event,
                    current_city,
                    domestic_items,
                    selected_domestic
                )

            # ==============================
            # 군사 메뉴
            # ==============================

            elif current_menu == "military":
                (
                    current_menu,
                    selected_military,
                    popup_message,
                    recruit_count,
                    recruit_count_input,
                    sortie_targets,
                    selected_sortie_target,
                    transport_targets,
                    selected_transport_target,
                ) = main.military_menu.handle_military_menu(
                    event=event,
                    current_city=current_city,
                    military_items=military_items,
                    selected_military=selected_military,
                    player_faction=PLAYER_FACTION,
                    recruit_count=recruit_count,
                    recruit_count_input=recruit_count_input,
                    sortie_targets=sortie_targets,
                    selected_sortie_target=selected_sortie_target,
                    transport_targets=transport_targets,
                    selected_transport_target=selected_transport_target,
                )

            # ==============================
            # 모병 수량 선택
            # ==============================

            elif current_menu == "recruit":
                (
                    current_menu,
                    recruit_count,
                    recruit_count_input,
                    popup_message,
                ) = main.military_menu.handle_recruit_menu(
                    event=event,
                    current_city=current_city,
                    recruit_count=recruit_count,
                    recruit_count_input=recruit_count_input,
                )

            # ==============================
            # 출진 대상 선택
            # ==============================

            elif current_menu == "sortie_target":
                (
                    current_menu,
                    selected_sortie_target,
                    sortie_target_city,
                    sortie_troops,
                    popup_message,
                ) = main.military_menu.handle_sortie_target(
                    event=event,
                    current_city=current_city,
                    sortie_targets=sortie_targets,
                    selected_sortie_target=selected_sortie_target,
                    sortie_target_city=sortie_target_city,
                    sortie_troops=sortie_troops,
                )

            # ==============================
            # 출진 병력 선택
            # ==============================

            elif current_menu == "sortie_troops":
                (
                    current_menu,
                    sortie_troops,
                    sortie_troops_input,
                    popup_message,
                    governor_candidates,
                    conquered_city,
                    selected_governor,
                ) = main.military_menu.handle_sortie_troops(
                    event=event,
                    current_city=current_city,
                    sortie_target_city=sortie_target_city,
                    sortie_troops=sortie_troops,
                    sortie_troops_input=sortie_troops_input,
                    cities=city.cities,
                    player_faction=PLAYER_FACTION,
                    governor_candidates=governor_candidates,
                    conquered_city=conquered_city,
                    selected_governor=selected_governor,
                )

            # ==============================
            # 이송 병력 선택
            # ==============================

            elif current_menu == "transport_target":
                (
                    current_menu,
                    selected_transport_target,
                    transport_target_city,
                    move_troops,
                    move_troops_input,
                    popup_message,
                ) = main.military_menu.handle_transport_target(
                    event=event,
                    current_city=current_city,
                    transport_targets=transport_targets,
                    selected_transport_target=selected_transport_target,
                    transport_target_city=transport_target_city,
                    move_troops=move_troops,
                    move_troops_input=move_troops_input,
                )

            # ==============================
            # 이송 병력 수 선택
            # ==============================

            elif current_menu == "transport_troops":
                (
                    current_menu,
                    move_troops,
                    move_troops_input,
                    popup_message,
                ) = main.military_menu.handle_transport_troops(
                    event=event,
                    current_city=current_city,
                    transport_target_city=transport_target_city,
                    move_troops=move_troops,
                    move_troops_input=move_troops_input,
                )

    # ==============================
    # 2. 화면 그리기
    # ==============================

    ui.draw_background(screen)

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
