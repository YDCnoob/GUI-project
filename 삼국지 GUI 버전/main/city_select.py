import pygame

def handle_governor_select(
    event,
    governor_candidates,
    selected_governor,
    conquered_city,
):
    current_menu = "governor_select"
    popup_message = None

    # 이전 통치자
    if event.key == pygame.K_UP:
        selected_governor -= 1
        selected_governor %= len(governor_candidates)

    # 다음 통치자
    elif event.key == pygame.K_DOWN:
        selected_governor += 1
        selected_governor %= len(governor_candidates)

    # 통치자 선택
    elif event.key == pygame.K_RETURN:
        new_governor = governor_candidates[selected_governor]

        conquered_city["governor"] = new_governor["name"]

        popup_message = (
            "통치자 임명 완료\n"
            f"{conquered_city['name']} : "
            f"{new_governor['name']}"
        )

        current_menu = "main"

    return (
        current_menu,
        selected_governor,
        popup_message,
    )


def handle_city_select(
    event,
    cities,
    current_city,
    selected_city,
):
    current_menu = "city_select"

    # 이전 도시
    if event.key == pygame.K_LEFT:
        selected_city -= 1
        selected_city %= len(cities)

        current_city = cities[selected_city]

    # 다음 도시
    elif event.key == pygame.K_RIGHT:
        selected_city += 1
        selected_city %= len(cities)

        current_city = cities[selected_city]

    # 선택 완료
    elif event.key == pygame.K_RETURN:
        current_menu = "main"

    # 돌아가기
    elif event.key == pygame.K_ESCAPE:
        current_menu = "main"

    return (
        current_menu,
        current_city,
        selected_city,
    )