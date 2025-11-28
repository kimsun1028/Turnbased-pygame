import pygame
from PartySelect import PartySelect
import Field
from Slime import Slime



def setup_first_floor():
    Field.enemies = [
        Slime("슬라임1"),
        Slime("슬라임2"),
        Slime("슬라임3"),
    ]

def set_enemy_position():
    Field.enemies[0].set_position(700, 200)
    Field.enemies[1].set_position(700, 300)
    Field.enemies[2].set_position(700, 400)



def animation_test_loop(screen):

    clock = pygame.time.Clock()
    running = True

    # --- 아군 전체 불러오기 ---
    allies = Field.allies   # [Knight, Archer, Priest]
    enemies = Field.enemies

    # --- 초기 선택 캐릭터: Knight ---
    selected_idx = 0
    test_char = allies[selected_idx]

    # --- 포지션 배치 ---
    # 아군 (왼쪽에 세 명)
    allies[0].set_position(300, 200)   # Knight
    allies[1].set_position(300, 300)   # Archer
    allies[2].set_position(300, 400)   # Priest

    # 적 (오른쪽에 세 명)
    set_enemy_position()


    font = pygame.font.SysFont("malgungothic", 28)

    while running:

        dt = clock.tick(60) / 1000.0

        # -------------------------
        # 키 입력 처리
        # -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # 🔥 1, 2, 3 → 캐릭터 선택
                if event.key == pygame.K_1:
                    selected_idx = 0
                    test_char = allies[selected_idx]
                    print("선택: 나이트")

                elif event.key == pygame.K_2:
                    selected_idx = 1
                    test_char = allies[selected_idx]
                    print("선택: 아처")

                elif event.key == pygame.K_3:
                    selected_idx = 2
                    test_char = allies[selected_idx]
                    print("선택: 프리스트")

                # --- 아래는 test_char에만 적용되는 테스트 입력 ---
                elif event.key == pygame.K_4:
                    test_char.queue_clear()
                    if test_char.job == "아처":
                        test_char.skill()
                    else:
                        test_char.queue_push("Skill", None)

                elif event.key == pygame.K_5:
                    test_char.queue_clear()
                    test_char.queue_push("Hurt", 0.4)

                elif event.key == pygame.K_6:
                    test_char.queue_clear()
                    test_char.queue_push("Death", None)

                elif event.key == pygame.K_e:
                    
                    if test_char.job == "아처":
                        if Field.enemies_alive() == 2:
                            test_char.basic_attack(Field.enemies_alive()[0],Field.enemies_alive()[1])
                        else:
                            test_char.basic_attack(Field.enemies_alive()[0])
                    else:
                        test_char.basic_attack(Field.enemies_alive()[0])

                elif event.key == pygame.K_h:
                    # Priest 스킬 테스트: allies_alive()[0] 힐
                    if test_char.job == "프리스트":
                        test_char.skill(0)  # 예: 첫번째 아군을 힐
                elif event.key == pygame.K_n:
                    setup_first_floor()
                    set_enemy_position()

                elif event.key == pygame.K_SPACE:
                    test_char.queue_clear()
                    test_char.queue_push("Idle", None)

                elif event.key == pygame.K_RETURN:
                    return


        # -------------------------
        # 업데이트
        # -------------------------
        for a in allies:
            a.update(dt)

        for e in enemies:
            e.update(dt)

        Field.effects.update(dt)


        # -------------------------
        # 렌더링
        # -------------------------
        screen.fill((30, 30, 30))

        # 안내 텍스트
        guide = [
            "애니메이션 테스트 모드",
            "캐릭터 선택: 1=Knight, 2=Archer, 3=Priest",
            f"현재 선택: {test_char.job}",
            "",
            "b: Basic",
            "4: Skill",
            "5: Hurt",
            "6: Death",
            "E: BasicAttack",
            "H: Heal(Priest)",
            "SPACE: Idle",
            "ENTER: 종료"
        ]

        for i, line in enumerate(guide):
            img = font.render(line, True, (255, 255, 255))
            screen.blit(img, (20, 20 + i * 28))

        # 아군/적 모두 출력
        for a in allies:
            a.draw(screen)
        for e in enemies:
            e.draw(screen)

        Field.effects.draw(screen)

        pygame.display.flip()



def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Turn-Based PYGAME")
    setup_first_floor()
    # 파티 선택
    party_scene = PartySelect(screen)
    party_scene.run()

    # 아군 Idle, Walk, Basic 등 애니메이션 사전 등록이 되어 있어야 한다
    # Knight.py, Archer.py, Priest.py에 add_anim() 호출 넣어둬야 함

    # 🔥 애니메이션 테스트 모드 실행
    animation_test_loop(screen)

    # 🔥 테스트 종료 후 실제 게임 시작

    # setup_first_floor()
    # Dungeon.first_floor(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
