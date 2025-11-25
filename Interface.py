# Interface.py
import Field
import pygame


def auto_layout(positions_x, start_y, gap, objects):
    for idx, obj in enumerate(objects):
        x = positions_x
        y = start_y + gap * idx
        obj.set_position(x, y)


def show_status(screen, character, offset_x=25, offset_y=120):
    """
    character.position 기준으로 offset만큼 위로 텍스트 출력
    """
    font = pygame.font.SysFont("malgungothic", 12)

    x, y = character.position

    text = f"{character.job}  HP:{character.current_hp}/{character.max_hp}  PW:{character.power}"
    surface = font.render(text, True, (255, 255, 255))

    # 캐릭터 머리 위에 출력하도록 offset 적용
    screen.blit(surface, (x + offset_x, y + offset_y))


def draw_top_hud(screen):
    font = pygame.font.SysFont("malgungothic", 18)

    # 도발 턴
    taunt_text = f"도발 남은 턴: {Field.remain_taunt_turn}"

    # 스킬 포인트
    sp_text = f"스킬포인트: {Field.skill_point}/{Field.max_skill_point}"

    # 렌더링
    if Field.is_taunt():
        taunt_surface = font.render(taunt_text, True, (255, 255, 255))
        screen.blit(taunt_surface, (50, 60))
    
    sp_surface = font.render(sp_text, True, (255, 255, 255))
    screen.blit(sp_surface, (50, 20))
























"""
def show_status():
    print()
    enemies_alive = Field.enemies_alive()
    allies_alive = Field.allies_alive()

    # 적 상태
    for i, e in enumerate(enemies_alive):
        print(f"{e.job}({i+1}): HP {e.current_hp}/{e.max_hp}", end="")
        if i + 1 != len(enemies_alive):
            print("  |  ", end="")
    print("\n")

    # 아군 상태
    for i, a in enumerate(allies_alive):
        print(
            f"{a.job}({i+1}): PW {a.power}  HP {a.current_hp}/{a.max_hp}",
            end="",
        )
        if i + 1 != len(allies_alive):
            print("  |  ", end="")
    print()

    print(f"스킬포인트: {Field.skill_point}/{Field.max_skill_point}", end="")
    if Field.is_taunt():
        print(f"   (도발 {Field.remain_taunt_turn}턴 남음)")
    else:
        print()
    print()


def pause():
    input("계속하려면 엔터를 누르세요...")
"""