import pygame

from core import city
from core import military
from core import officer

def handle_military_menu(
    event,
    current_city,
    military_items,
    selected_military,
    player_faction,
    recruit_count,
    recruit_count_input,
    sortie_targets,
    selected_sortie_target,
    transport_targets,
    selected_transport_target,
):
    """군사 메인 메뉴의 키 입력과 하위 메뉴 이동을 처리한다."""

    current_menu = "military"
    popup_message = None

    # 위
    if event.key == pygame.K_UP:
        selected_military -= 1
        selected_military %= len(military_items)

    # 아래
    elif event.key == pygame.K_DOWN:
        selected_military += 1
        selected_military %= len(military_items)

    # 돌아가기
    elif event.key == pygame.K_ESCAPE:
        current_menu = "main"

    # 선택
    elif event.key == pygame.K_RETURN:
        selected_item = military_items[selected_military]

        # 모병
        if selected_item == "모병":
            if current_city["recruited_this_turn"]:
                popup_message = (
                    "모병 실패\n"
                    "이번 턴에는 이미 모병했습니다."
                )
            else:
                recruit_count = 0
                recruit_count_input = ""
                current_menu = "recruit"

        # 훈련
        elif selected_item == "훈련":
            if current_city["trained_this_turn"]:
                popup_message = (
                    "훈련 실패\n"
                    "이번 턴에는 이미 훈련했습니다."
                )
            else:
                cost, gain = military.train_army(current_city)

                if gain > 0:
                    current_city["trained_this_turn"] = True

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

        # 출진
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
                    target_faction = officer.get_city_faction(
                        target_city
                    )

                    # 같은 세력 도시는 공격 대상 제외
                    if target_faction != player_faction:
                        sortie_targets.append(target_city)

                if not sortie_targets:
                    popup_message = (
                        "출진 불가\n"
                        "공격 가능한 인접 도시가 없습니다"
                    )
                else:
                    selected_sortie_target = 0
                    current_menu = "sortie_target"

        # 병력 이동
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
                    target_faction = officer.get_city_faction(
                        target_city
                    )

                    # 같은 세력 도시만 이동 가능
                    if target_faction == player_faction:
                        transport_targets.append(target_city)

                if not transport_targets:
                    popup_message = (
                        "병력 이동 불가\n"
                        "인접한 아군 도시가 없습니다."
                    )
                else:
                    selected_transport_target = 0
                    current_menu = "transport_target"

        # 돌아가기
        elif selected_item == "돌아가기":
            current_menu = "main"

    return (
        current_menu,
        selected_military,
        popup_message,
        recruit_count,
        recruit_count_input,
        sortie_targets,
        selected_sortie_target,
        transport_targets,
        selected_transport_target,
    )


def handle_recruit_menu(
    event,
    current_city,
    recruit_count,
    recruit_count_input,
):
    """모병 수량 입력과 모병 실행을 처리한다."""

    current_menu = "recruit"
    popup_message = None

    # 숫자 직접 입력
    if pygame.K_0 <= event.key <= pygame.K_9:
        recruit_count_input += event.unicode

        if recruit_count_input:
            recruit_count = int(recruit_count_input)

    # 한 자리 삭제
    elif event.key == pygame.K_BACKSPACE:
        recruit_count_input = recruit_count_input[:-1]

        if recruit_count_input:
            recruit_count = int(recruit_count_input)
        else:
            recruit_count = 0

    # 100명 감소
    elif event.key == pygame.K_LEFT:
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
            current_city["recruited_this_turn"] = True

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

    return (
        current_menu,
        recruit_count,
        recruit_count_input,
        popup_message,
    )


def handle_sortie_target(
    event,
    current_city,
    sortie_targets,
    selected_sortie_target,
    sortie_target_city,
    sortie_troops,
):
    """출진할 대상 도시 선택을 처리한다."""

    current_menu = "sortie_target"
    popup_message = None

    # 위
    if event.key == pygame.K_UP:
        selected_sortie_target -= 1
        selected_sortie_target %= len(sortie_targets)

    # 아래
    elif event.key == pygame.K_DOWN:
        selected_sortie_target += 1
        selected_sortie_target %= len(sortie_targets)

    # 취소
    elif event.key == pygame.K_ESCAPE:
        current_menu = "military"

    # 대상 결정
    elif event.key == pygame.K_RETURN:
        sortie_target_city = sortie_targets[
            selected_sortie_target
        ]

        if current_city["troops"] < 100:
            popup_message = (
                "출진 불가\n"
                "출진할 병력이 부족합니다."
            )
            current_menu = "military"

        else:
            sortie_troops = 100
            current_menu = "sortie_troops"

    return (
        current_menu,
        selected_sortie_target,
        sortie_target_city,
        sortie_troops,
        popup_message,
    )


def handle_sortie_troops(
    event,
    current_city,
    sortie_target_city,
    sortie_troops,
    sortie_troops_input,
    cities,
    player_faction,
    governor_candidates,
    conquered_city,
    selected_governor,
):
    """출진 병력 입력과 전투 후 처리를 담당한다."""

    current_menu = "sortie_troops"
    popup_message = None

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
        sortie_troops_input = sortie_troops_input[:-1]

        if sortie_troops_input:
            sortie_troops = int(sortie_troops_input)
        else:
            sortie_troops = 0

    # 100명 감소
    elif event.key == pygame.K_LEFT:
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
                sortie_troops,
            )

            # 출진 병력은 일단 출진 도시에서 빠짐.
            current_city["troops"] -= sortie_troops

            # 승리
            if result["result"] == "win":
                # 살아 남은 병력이 공격 도시 주둔
                sortie_target_city["troops"] = (
                    result["remaining_troops"]
                )

                # 점령 처리
                governor_candidates = (
                    officer.get_available_governors(
                        cities,
                        player_faction,
                    )
                )

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
                current_city["troops"] += result[
                    "remaining_troops"
                ]
                current_city["sortied_this_turn"] = True

                popup_message = (
                    "전투 패배\n"
                    f"공격군 피해 : "
                    f"{result['attacker_loss']:,}명\n"
                    f"방어군 피해 : "
                    f"{result['defender_loss']:,}명"
                )
                current_menu = "military"

    return (
        current_menu,
        sortie_troops,
        sortie_troops_input,
        popup_message,
        governor_candidates,
        conquered_city,
        selected_governor,
    )


def handle_transport_target(
    event,
    current_city,
    transport_targets,
    selected_transport_target,
    transport_target_city,
    move_troops,
    move_troops_input,
):
    """병력을 이동할 대상 도시 선택을 처리한다."""

    current_menu = "transport_target"
    popup_message = None

    # 위
    if event.key == pygame.K_UP:
        selected_transport_target -= 1
        selected_transport_target %= len(transport_targets)

    # 아래
    elif event.key == pygame.K_DOWN:
        selected_transport_target += 1
        selected_transport_target %= len(transport_targets)

    # 취소
    elif event.key == pygame.K_ESCAPE:
        current_menu = "military"

    # 대상 결정
    elif event.key == pygame.K_RETURN:
        transport_target_city = transport_targets[
            selected_transport_target
        ]

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

    return (
        current_menu,
        selected_transport_target,
        transport_target_city,
        move_troops,
        move_troops_input,
        popup_message,
    )


def handle_transport_troops(
    event,
    current_city,
    transport_target_city,
    move_troops,
    move_troops_input,
):
    """이동 병력 수 입력과 실제 병력 이동을 처리한다."""

    current_menu = "transport_troops"
    popup_message = None

    # 숫자 직접 입력
    if pygame.K_0 <= event.key <= pygame.K_9:
        move_troops_input += event.unicode

        if move_troops_input:
            move_troops = int(move_troops_input)

        # 현재 병력보다 많이 입력하면 제한
        if move_troops > current_city["troops"]:
            move_troops = current_city["troops"]
            move_troops_input = str(move_troops)

    # 한 자리 삭제
    elif event.key == pygame.K_BACKSPACE:
        move_troops_input = move_troops_input[:-1]

        if move_troops_input:
            move_troops = int(move_troops_input)
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

    return (
        current_menu,
        move_troops,
        move_troops_input,
        popup_message,
    )
