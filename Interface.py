# Interface.py
import Field
import pygame


def auto_layout(positions_x, start_y, gap, objects):
    """
    지정한 X 좌표와 시작 Y, 간격(gap)에 따라 objects를 세로로 자동 배치합니다.
    각 객체는 set_position() 메서드를 사용해 위치가 설정됩니다.
    """
    for idx, obj in enumerate(objects):
        x = positions_x
        y = start_y + gap * idx
        obj.set_position(x, y)


def show_status(screen, character, index=None, offset_x=25, offset_y=120):
    """
    한 캐릭터의 상태(HP, 파워 등)를 화면에 출력
    index를 주면 (1), (2) 형태의 번호를 표시
    """
    font = pygame.font.SysFont("malgungothic", 12)

    x, y = character.position

    # 번호 showingidx 추가
    if index is None:
        showingidx = ""
    else:
        showingidx = f"({index}) "

    text = f"{showingidx}{character.job}  HP:{character.current_hp}/{character.max_hp}  PW:{character.power}"
    surface = font.render(text, True, (255, 255, 255))

    screen.blit(surface, (x + offset_x-100, y + offset_y-100))


def draw_top_hud(screen):
    """
    전투 상단 HUD(턴 수, 도발 상태, 스킬 포인트)를 화면에 출력
    """
    font = pygame.font.SysFont("malgungothic", 24)

    turn_text =  f"턴 : {Field.turn}"
    # 도발 턴
    taunt_text = f"도발 남은 턴: {Field.remain_taunt_turn}"

    # 스킬 포인트
    sp_text = f"스킬포인트: {Field.skill_point}/{Field.max_skill_point}"

    # 렌더링
    if Field.is_taunt():
        taunt_surface = font.render(taunt_text, True, (255, 255, 255))
        screen.blit(taunt_surface, (30, 90))
    turn_surface = font.render(turn_text, True, (255,255,255))
    sp_surface = font.render(sp_text, True, (255, 255, 255))
    screen.blit(sp_surface, (30, 60))
    screen.blit(turn_surface, (30, 30))
