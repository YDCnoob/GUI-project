import pygame

def handle_info_menu(event):
    """정보 화면의 키 입력을 처리한다."""
    current_menu = "info"

    # Enter 또는 ESC로 메인 메뉴 복귀
    if (
        event.key == pygame.K_RETURN
        or event.key == pygame.K_ESCAPE
    ):
        current_menu = "main"

    return current_menu
