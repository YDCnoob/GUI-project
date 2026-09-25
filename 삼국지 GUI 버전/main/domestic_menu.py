import pygame
from core import domestic

def handle_domestic_menu(
    event,
    current_city,
    domestic_items,
    selected_domestic,
):
    current_menu = "domestic"
    popup_message = None

    # 위
    if event.key == pygame.K_UP:
        selected_domestic -= 1
        selected_domestic %= len(domestic_items)

    # 아래
    elif event.key == pygame.K_DOWN:
        selected_domestic += 1
        selected_domestic %= len(domestic_items)

    # 돌아가기
    elif event.key == pygame.K_ESCAPE:
        current_menu = "main"

    # 선택
    elif event.key == pygame.K_RETURN:

        selected_item = domestic_items[selected_domestic]

        # 농업 개발
        if selected_item == "농업 개발":

            current_city["ap"], cost, gain = domestic.dev_agri(
                current_city,
                current_city["ap"],
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

        # 상업 개발
        elif selected_item == "상업 개발":

            current_city["ap"], cost, gain = domestic.dev_commerce(
                current_city,
                current_city["ap"],
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

        # 치안 강화
        elif selected_item == "치안 강화":

            current_city["ap"], cost, gain = domestic.improve_order(
                current_city,
                current_city["ap"],
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

        # 돌아가기
        elif selected_item == "돌아가기":
            current_menu = "main"

    return current_menu, selected_domestic, popup_message