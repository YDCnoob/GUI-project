import pygame


# ==============================
# 색상
# ==============================

BACKGROUND = (8, 16, 48)

PANEL_BG = (15, 29, 61)
PANEL_ALT_BG = (27, 24, 54)
POPUP_BG = (20, 19, 44)

BORDER = (205, 190, 140)
POPUP_BORDER = (255, 220, 110)

TEXT = (235, 230, 210)
HIGHLIGHT = (255, 220, 110)
MUTED = (160, 170, 180)

# ==============================
# UI 레이아웃
# ==============================

UI_MARGIN = 16

HEADER_HEIGHT = 56
CITY_INFO_HEIGHT = 80
MAIN_MENU_HEIGHT = 84


def get_centered_position(
    screen,
    width,
    height,
):

    x = (
        screen.get_width() - width
    ) // 2

    y = (
        screen.get_height() - height
    ) // 2

    return x, y

# ==============================
# 기본 그리기 함수
# ==============================

def draw_background(screen):
    screen.fill(BACKGROUND)


def draw_panel(
    screen,
    x,
    y,
    width,
    height,
    fill_color=PANEL_BG,
    border_color=BORDER,
    border_width=2,
):
    rect = pygame.Rect(
        x,
        y,
        width,
        height,
    )

    # 내부 배경
    pygame.draw.rect(
        screen,
        fill_color,
        rect,
    )

    # 테두리
    pygame.draw.rect(
        screen,
        border_color,
        rect,
        border_width,
    )


def draw_text(
    screen,
    font,
    text,
    x,
    y,
    color=TEXT,
):
    image = font.render(
        text,
        True,
        color,
    )

    screen.blit(
        image,
        (x, y),
    )


def draw_centered_text(
    screen,
    font,
    text,
    rect,
    color=TEXT,
):
    rect = pygame.Rect(rect)

    image = font.render(
        text,
        True,
        color,
    )

    image_rect = image.get_rect(
        center=rect.center
    )

    screen.blit(
        image,
        image_rect,
    )


# ==============================
# 상단 정보창
# ==============================

def draw_header(
    screen,
    font,
    year,
    month,
    ap,
):

    x = UI_MARGIN
    y = UI_MARGIN

    width = (screen.get_width() - UI_MARGIN * 2) 
    height = HEADER_HEIGHT
    
    draw_panel(
        screen,
        x,
        y,
        width,
        height,
    )

    # 게임 제목
    draw_text(
        screen,
        font,
        "三國志",
        x + 20,
        y + 17,
        HIGHLIGHT,
    )

    # 날짜
    draw_centered_text(
        screen,
        font,
        f"{year}년 {month}월",
        (x, y, width, height),
    )

    # 행동력
    draw_text(
        screen,
        font,
        f"행동력 : {ap}",
        x + width - 150,
        y + 17,
    )


# ==============================
# 도시 정보창
# ==============================

def draw_city_panel(
    screen,
    font,
    city,
):
    x = UI_MARGIN
    y = 100
    width = 620
    height = 420

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
    )

    # 제목
    draw_centered_text(
        screen,
        font,
        "도 시 정 보",
        (x, y + 15, width, 35),
        HIGHLIGHT,
    )

    # 도시 이름
    draw_text(
        screen,
        font,
        f"도시 : {city['name']}",
        x + 30,
        y + 65,
    )

    # 구분선
    pygame.draw.line(
        screen,
        BORDER,
        (x + 25, y + 105),
        (x + width - 25, y + 105),
        1,
    )

    # 왼쪽 열
    left_x = x + 40
    right_x = x + 330

    row1 = y + 140
    row2 = y + 190
    row3 = y + 240
    row4 = y + 290

    draw_text(
        screen,
        font,
        f"인구 : {city['population']:,}",
        left_x,
        row1,
    )

    draw_text(
        screen,
        font,
        f"금   : {city['gold']:,}",
        left_x,
        row2,
    )

    draw_text(
        screen,
        font,
        f"식량 : {city['food']:,}",
        left_x,
        row3,
    )

    draw_text(
        screen,
        font,
        f"치안 : {city['public_order']}",
        left_x,
        row4,
    )

    draw_text(
        screen,
        font,
        f"농업 : {city['agriculture']}",
        right_x,
        row1,
    )

    draw_text(
        screen,
        font,
        f"상업 : {city['commerce']}",
        right_x,
        row2,
    )

    draw_text(
        screen,
        font,
        f"병력 : {city['troops']:,}",
        right_x,
        row3,
    )

    draw_text(
        screen,
        font,
        f"훈련 : {city['training']}",
        right_x,
        row4,
    )


# ==============================
# 통치자 정보창
# ==============================

def draw_governor_panel(
    screen,
    font,
    governor,
    faction=None,
):

    width = 330
    height = 420

    x = (screen.get_width() - UI_MARGIN - width)
    y = 100

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
    )

    draw_centered_text(
        screen,
        font,
        "통 치 자",
        (x, y + 15, width, 35),
        HIGHLIGHT,
    )

    # 통치자가 없는 도시
    if governor is None:
        draw_centered_text(
            screen,
            font,
            "통치자 없음",
            (x, y + 150, width, 40),
            MUTED,
        )
        return

    draw_centered_text(
        screen,
        font,
        governor["name"],
        (x, y + 60, width, 40),
        HIGHLIGHT,
    )

    faction_text = faction if faction is not None else "없음"

    rows = [
        ("세력", faction_text),
        ("통솔", governor["leadership"]),
        ("무력", governor["war"]),
        ("지력", governor["intelligence"]),
        ("정치", governor["politics"]),
        ("매력", governor["charisma"]),
    ]

    text_y = y + 120

    for label, value in rows:
        draw_text(
            screen,
            font,
            f"{label} : {value}",
            x + 75,
            text_y,
        )
        text_y += 42


def draw_info_menu(
    screen,
    font,
    city,
    governor,
    faction,
):
    """현재 도시와 통치자의 상세 정보를 표시한다."""

    draw_city_panel(
        screen,
        font,
        city,
    )

    draw_governor_panel(
        screen,
        font,
        governor,
        faction,
    )

    draw_centered_text(
        screen,
        font,
        "Enter / ESC : 돌아가기",
        (
            UI_MARGIN,
            525,
            screen.get_width() - UI_MARGIN * 2,
            30,
        ),
        MUTED,
    )


# ==============================
# 메인 명령 메뉴
# ==============================

def draw_main_menu(
    screen,
    font,
    menu_items,
    selected_menu,
):

    x = UI_MARGIN

    width = (
        screen.get_width()
        - UI_MARGIN * 2
    )

    height = MAIN_MENU_HEIGHT

    y = (
        screen.get_height()
        - height
        - UI_MARGIN
    )

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
    )

    slot_width = (
        width - 20
    ) // len(menu_items)

    for index, item in enumerate(
        menu_items
    ):

        slot_x = (
            x
            + 10
            + index * slot_width
        )

        slot_rect = pygame.Rect(
            slot_x,
            y + 10,
            slot_width,
            height - 20,
        )

        if index == selected_menu:
            text = f"> {item}"
            color = HIGHLIGHT
        else:
            text = item
            color = TEXT

        draw_centered_text(
            screen,
            font,
            text,
            slot_rect,
            color,
        )

# ==============================
# 내정 메뉴
# ==============================

def draw_domestic_menu(
    screen,
    font,
    domestic_items,
    selected_domestic,
):

    width = 340
    height = 280
    x, y = get_centered_position(screen, width, height)

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=PANEL_ALT_BG,
    )

    draw_centered_text(
        screen,
        font,
        "내 정",
        (x, y + 10, width, 30),
        HIGHLIGHT,
    )

    menu_y = y + 55

    for index, item in enumerate(
        domestic_items
    ):

        if index == selected_domestic:
            prefix = "> "
            color = HIGHLIGHT
        else:
            prefix = "  "
            color = TEXT

        draw_text(
            screen,
            font,
            prefix + item,
            x + 55,
            menu_y,
            color,
        )

        menu_y += 30

    draw_centered_text(
        screen,
        font,
        "ESC : 돌아가기",
        (x, y + height - 50, width, 30),
        MUTED,
    )


# ==============================
# 결과 팝업
# ==============================

def draw_popup(
    screen,
    font,
    message,
):
    lines = message.split("\n")

    width = 440

    # 메시지 줄 수에 따라 높이 자동 조정
    height = max(
        160,
        80 + len(lines) * 28,
    )

    x = (
        screen.get_width()
        - width
    ) // 2

    y = (
        screen.get_height()
        - height
    ) // 2

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=POPUP_BG,
        border_color=POPUP_BORDER,
    )

    text_y = y + 30

    for index, line in enumerate(lines):

        if index == 0:
            color = HIGHLIGHT
        else:
            color = TEXT

        draw_centered_text(
            screen,
            font,
            line,
            (
                x + 15,
                text_y,
                width - 30,
                25,
            ),
            color,
        )

        text_y += 28

    # 확인 문구
    draw_centered_text(
        screen,
        font,
        "Enter / ESC : 확인",
        (
            x,
            y + height - 40,
            width,
            25,
        ),
        MUTED,
    )

# ==============================
# 군사 메뉴
# ==============================

def draw_military_menu(
    screen,
    font,
    military_items,
    selected_military,
):

    width = 360
    height = 330 
    x, y = get_centered_position(screen, width, height)

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=PANEL_ALT_BG,
    )

    draw_centered_text(
        screen,
        font,
        "군 사",
        (x, y + 10, width, 30),
        HIGHLIGHT,
    )

    menu_y = y + 60

    for index, item in enumerate(
        military_items
    ):
        if index == selected_military:
            prefix = "> "
            color = HIGHLIGHT
        else:
            prefix = "  "
            color = TEXT

        draw_text(
            screen,
            font,
            prefix + item,
            x + 70,
            menu_y,
            color,
        )

        menu_y += 32

    draw_centered_text(
        screen,
        font,
        "ESC : 돌아가기",
        (x, y + 235, width, 25),
        MUTED,
    )


# ==============================
# 모병 수량 선택
# ==============================

def draw_recruit_menu(
    screen,
    font,
    city,
    recruit_count,
):
    
    width = 400
    height = 300
    x, y = get_centered_position(screen, width, height)

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=PANEL_ALT_BG,
    )

    draw_centered_text(
        screen,
        font,
        "모 병",
        (x, y + 10, width, 30),
        HIGHLIGHT,
    )

    draw_text(
        screen,
        font,
        f"현재 병력 : {city['troops']:,}",
        x + 45,
        y + 55,
    )

    draw_text(
        screen,
        font,
        f"현재 식량 : {city['food']:,}",
        x + 45,
        y + 85,
    )

    draw_centered_text(
        screen,
        font,
        f"<  {recruit_count:,}명  >",
        (x, y + 120, width, 35),
        HIGHLIGHT,
    )

    draw_centered_text(
        screen,
        font,
        "← → : 인원 변경",
        (x, y + 160, width, 25),
        MUTED,
    )

    draw_centered_text(
        screen,
        font,
        "Enter : 모병   ESC : 취소",
        (x, y + 185, width, 25),
        MUTED,
    )

# ==============================
# 지도 설정
# ==============================

MAP_LEFT = 200
MAP_TOP = 170

MAP_X_GAP = 280
MAP_Y_GAP = 120


# ==============================
# 도시 논리 좌표 → 화면 좌표
# ==============================

def get_city_screen_position(city):

    screen_x = (
        MAP_LEFT
        + city["map_x"] * MAP_X_GAP
    )

    screen_y = (
        MAP_TOP
        + city["map_y"] * MAP_Y_GAP
    )

    return screen_x, screen_y

# ==============================
# 지도
# ==============================

def draw_map(
    screen,
    font,
    cities,
    current_city,
):

    x = UI_MARGIN
    y = 84

    width = (
        screen.get_width()
        - UI_MARGIN * 2
    )

    height = 470

    city_lookup = {
        city["name"]: city
        for city in cities
    }

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
    )


    # ==============================
    # 도시 연결선
    # ==============================

    for city in cities:

        start_x, start_y = (
            get_city_screen_position(city)
        )

        for neighbor_name in city["neighbors"]:

            neighbor = city_lookup.get(neighbor_name)

            if neighbor is None:
                continue

            end_x, end_y = (
                get_city_screen_position(
                    neighbor
                )
            )

            pygame.draw.line(
                screen,
                BORDER,
                (start_x, start_y),
                (end_x, end_y),
                2,
            )


    # ==============================
    # 도시 표시
    # ==============================

    for city in cities:

        x, y = get_city_screen_position(
            city
        )

        # 현재 선택된 도시
        if city is current_city:

            pygame.draw.circle(
                screen,
                HIGHLIGHT,
                (x, y),
                9,
            )

            city_color = HIGHLIGHT

        # 일반 도시
        else:

            pygame.draw.circle(
                screen,
                TEXT,
                (x, y),
                6,
            )

            city_color = TEXT


        # 도시 이름
        draw_centered_text(
            screen,
            font,
            city["name"],
            (
                x - 40,
                y + 10,
                80,
                25,
            ),
            city_color,
        )


# ==============================
# 선택 도시 간략 정보
# ==============================

def draw_selected_city_info(
    screen,
    font,
    city,
    faction,
):

    if city["governor"] is None:
        governor_text = "없음"
    else:
        governor_text = city["governor"]

    if faction is None:
        faction_text = "없음"
    else:
        faction_text = faction

    x = UI_MARGIN
    y = 566

    width = (
        screen.get_width()
        - UI_MARGIN * 2
    )

    height = 90

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
    )

    # 첫 번째 줄

    draw_text(
        screen,
        font,
        f"도시 : {city['name']}",
        x + 20,
        y + 18,
        HIGHLIGHT,
    )

    draw_text(
        screen,
        font,
        f"통치자 : {governor_text}",
        x + 180,
        y + 18,
    )

    draw_text(
        screen,
        font,
        f"병력 : {city['troops']:,}",
        x + 410,
        y + 18,
    )

    draw_text(
        screen,
        font,
        f"금 : {city['gold']:,}",
        x + 650,
        y + 18,
    )

    # 두 번째 줄

    draw_text(
        screen,
        font,
        f"식량 : {city['food']:,}",
        x + 20,
        y + 52,
    )

    draw_text(
        screen,
        font,
        f"치안 : {city['public_order']}",
        x + 190,
        y + 52,
    )

    draw_text(
        screen,
        font,
        f"농업 : {city['agriculture']}",
        x + 340,
        y + 52,
    )

    draw_text(
        screen,
        font,
        f"상업 : {city['commerce']}",
        x + 490,
        y + 52,
    )

    draw_text(
        screen,
        font,
        f"세력 : {faction_text}",
        x + 650,
        y + 52,
    )

# ==============================
# 출진 대상 선택
# ==============================

def draw_sortie_target_menu(
    screen,
    font,
    targets,
    selected_target,
):

    width = 420
    height = 340
    x, y = get_centered_position(screen, width, height)

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=PANEL_ALT_BG,
    )

    draw_centered_text(
        screen,
        font,
        "출 진",
        (x, y + 15, width, 30),
        HIGHLIGHT,
    )

    menu_y = y + 55

    for index, target in enumerate(targets):

        if index == selected_target:
            prefix = "> "
            color = HIGHLIGHT
        else:
            prefix = "  "
            color = TEXT

        draw_text(
            screen,
            font,
            prefix + target["name"],
            x + 70,
            menu_y,
            color,
        )

        menu_y += 30

    draw_centered_text(
        screen,
        font,
        "Enter : 선택   ESC : 취소",
        (x, y + height - 45, width, 30),
        MUTED,
    )

# ==============================
# 출진 병력 선택
# ==============================

def draw_sortie_troops_menu(
    screen,
    font,
    city,
    target_city,
    sortie_troops,
):

    width = 400
    height = 340
    x, y = get_centered_position(screen, width, height)

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=PANEL_ALT_BG,
    )

    draw_centered_text(
        screen,
        font,
        "출 진",
        (x, y + 15, width, 35),
        HIGHLIGHT,
    )

    draw_text(
        screen,
        font,
        f"출발 도시 : {city['name']}",
        x + 65,
        y + 75,
    )

    draw_text(
        screen,
        font,
        f"목표 도시 : {target_city['name']}",
        x + 65,
        y + 110,
    )

    draw_text(
        screen,
        font,
        f"현재 병력 : {city['troops']:,}",
        x + 65,
        y + 145,
    )

    draw_centered_text(
        screen,
        font,
        f"<  {sortie_troops:,}명  >",
        (x, y + 185, width, 40),
        HIGHLIGHT,
    )

    draw_centered_text(
        screen,
        font,
        "← → : 병력 변경",
        (x, y + 235, width, 30),
        MUTED,
    )

    draw_centered_text(
        screen,
        font,
        "Enter : 출진   ESC : 취소",
        (x, y + height - 50, width, 30),
        MUTED,
    )

# ==============================
# 통치자 선택
# ==============================

def draw_governor_select_menu(
    screen,
    font,
    city,
    candidates,
    selected_governor,
):
    width = 440
    height = 460

    x, y = get_centered_position(
        screen,
        width,
        height,
    )

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=PANEL_ALT_BG,
    )

    # ==============================
    # 제목
    # ==============================

    draw_centered_text(
        screen,
        font,
        "통 치 자 임 명",
        (x, y + 15, width, 35),
        HIGHLIGHT,
    )

    draw_centered_text(
        screen,
        font,
        f"{city['name']} 통치자",
        (x, y + 55, width, 30),
    )

    # ==============================
    # 페이지 설정
    # ==============================

    PAGE_SIZE = 8

    current_page = (
        selected_governor
        // PAGE_SIZE
    )

    total_pages = (
        len(candidates)
        + PAGE_SIZE
        - 1
    ) // PAGE_SIZE

    start = (
        current_page
        * PAGE_SIZE
    )

    end = (
        start
        + PAGE_SIZE
    )

    visible_candidates = (
        candidates[start:end]
    )

    # ==============================
    # 장수 목록
    # ==============================

    menu_y = y + 100

    for index, officer_data in enumerate(
        visible_candidates
    ):
        real_index = (
            start
            + index
        )

        if real_index == selected_governor:
            prefix = "> "
            color = HIGHLIGHT
        else:
            prefix = "  "
            color = TEXT

        draw_text(
            screen,
            font,
            (
                f"{prefix}"
                f"{officer_data['name']}  "
                f"통솔 {officer_data['leadership']}  "
                f"정치 {officer_data['politics']}"
            ),
            x + 120,
            menu_y,
            color,
        )

        menu_y += 32

    # ==============================
    # 페이지 표시
    # ==============================

    draw_centered_text(
        screen,
        font,
        f"{current_page + 1} / {total_pages}",
        (
            x,
            y + height - 95,
            width,
            25,
        ),
        MUTED,
    )

    # ==============================
    # 조작 안내
    # ==============================

    draw_centered_text(
        screen,
        font,
        "↑ ↓ : 선택   Enter : 임명",
        (
            x,
            y + height - 55,
            width,
            30,
        ),
        MUTED,
    )

# ==============================
# 병력 이동 대상 선택
# ==============================

def draw_transport_target_menu(
    screen,
    font,
    targets,
    selected_target,
):

    width = 400
    height = 300
    x, y = get_centered_position(screen, width, height)

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=PANEL_ALT_BG,
    )

    draw_centered_text(
        screen,
        font,
        "병 력 이 동",
        (x, y + height - 50, width, 30),
        HIGHLIGHT,
    )

    menu_y = y + 55

    for index, target in enumerate(targets):

        if index == selected_target:
            prefix = "> "
            color = HIGHLIGHT
        else:
            prefix = "  "
            color = TEXT

        draw_text(
            screen,
            font,
            prefix + target["name"],
            x + 70,
            menu_y,
            color,
        )

        menu_y += 30

    draw_centered_text(
        screen,
        font,
        "Enter : 선택   ESC : 취소",
        (x, y + height - 50, width, 30),
        MUTED,
    )

# ==============================
# 이동 병력 수 선택
# ==============================

def draw_transport_troops_menu(
    screen,
    font,
    city,
    target_city,
    move_troops,
):
    
    width = 460
    height = 340
    x, y = get_centered_position(screen, width, height)

    draw_panel(
        screen,
        x,
        y,
        width,
        height,
        fill_color=PANEL_ALT_BG,
    )

    draw_centered_text(
        screen,
        font,
        "병 력 이 동",
        (x, y + 15, width, 35),
        HIGHLIGHT,
    )

    draw_text(
        screen,
        font,
        f"출발 도시 : {city['name']}",
        x + 65,
        y + 75,
    )

    draw_text(
        screen,
        font,
        f"도착 도시 : {target_city['name']}",
        x + 65,
        y + 110,
    )

    draw_text(
        screen,
        font,
        f"현재 병력 : {city['troops']:,}",
        x + 65,
        y + 145,
    )

    draw_centered_text(
        screen,
        font,
        f"<  {move_troops:,}명  >",
        (x, y + 185, width, 40),
        HIGHLIGHT,
    )

    draw_centered_text(
        screen,
        font,
        "← → : 병력 변경",
        (x, y + 235, width, 30),
        MUTED,
    )

    draw_centered_text(
        screen,
        font,
        "Enter : 이동   ESC : 취소",
        (x, y + height - 50, width, 30),
        MUTED,
    )