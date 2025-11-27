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


def animation_test_loop(screen):
    """
    애니메이션 테스트 모드
    - 1: MoveTo 테스트
    - 2: Basic 애니메이션 재생
    - 3: Hurt 애니메이션
    - 4: Death 애니메이션
    """


    clock = pygame.time.Clock()
    running = True

    # 첫 번째 아군만 테스트 대상으로 사용
    test_char = Field.allies[0]
    test_enemy = Field.enemies[0]
    test_char.set_position(400, 300)
    test_enemy.set_position(660,300)
    # 화면 안내용 폰트
    font = pygame.font.SysFont("malgungothic", 28)

    while running:
        dt = clock.tick(60) / 1000.0  # dt = 초 단위
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 키보드 입력 애니메이션 테스트
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # MoveTo 테스트: 오른쪽으로 200px 이동
                    x, y = test_char.position
                    test_char.move_to((x + 200, y))
                
                elif event.key == pygame.K_2:
                    # Walk 뒤로 (왼쪽)
                    x, y = test_char.position
                    test_char.move_to((x - 200, y))

                elif event.key == pygame.K_3:
                    # Basic 공격 모션
                    test_char.queue_clear()
                    test_char.queue_push("Basic", None)

                elif event.key == pygame.K_4:
                    # Skill 모션
                    test_char.queue_clear()
                    Field.remain_taunt_turn = 2
                    test_char.queue_push("Skill", None)

                elif event.key == pygame.K_5:
                    # Hurt 모션
                    test_char.queue_clear()
                    test_char.queue_push("Hurt", 0.4)

                elif event.key == pygame.K_6:
                    # Death 모션
                    test_char.queue_clear()
                    test_char.queue_push("Death", None)

                elif event.key == pygame.K_7 :
                    test_enemy = Field.enemies.pop()

                

                elif event.key == pygame.K_SPACE:
                    # Idle로 강제 복귀
                    test_char.queue_clear()
                    test_char.queue_push("Idle", None)
                elif event.key == pygame.K_e:
                    test_char.basic_attack(test_enemy)
                    # Enter → 테스트 종료

                elif event.key == pygame.K_RETURN:
                    return

        # 업데이트
        test_char.update(dt)
        test_enemy.update(dt)


        # 화면 렌더링
        screen.fill((30, 30, 30))

        # 안내 텍스트 출력
        guide = [
            "애니메이션 테스트 모드",
            "1: MoveTo (오른쪽으로 이동)",
            "2: MoveTo (왼쪽으로 이동)",
            "3: Basic 애니메이션",
            "4: Skill 애니메이션",
            "5: Hurt 애니메이션",
            "6: Death 애니메이션",
            "E: 이동 평타(강화) 모션 애니메이션"
            "SPACE: Idle 복귀",
            "ENTER: 테스트 종료"
        ]

        for i, line in enumerate(guide):
            img = font.render(line, True, (255, 255, 255))
            screen.blit(img, (20, 20 + i * 30))

        test_char.draw(screen)
        test_enemy.draw(screen)

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
