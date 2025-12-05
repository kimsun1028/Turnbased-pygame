# Interface.py
import Field
import pygame


def auto_layout(positions_x, start_y, gap, objects):
    for idx, obj in enumerate(objects):
        x = positions_x
        y = start_y + gap * idx
        obj.set_position(x, y)


def show_status(screen, character, index=None, offset_x=25, offset_y=120):
    font = pygame.font.SysFont("malgungothic", 12)

    x, y = character.position

    # 번호 prefix 추가
    if index is None:
        prefix = ""
    else:
        prefix = f"({index}) "

    text = f"{prefix}{character.job}  HP:{character.current_hp}/{character.max_hp}  PW:{character.power}"
    surface = font.render(text, True, (255, 255, 255))

    screen.blit(surface, (x + offset_x-100, y + offset_y-100))


def draw_top_hud(screen):
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
