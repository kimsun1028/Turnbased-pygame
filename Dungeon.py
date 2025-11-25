import pygame
import random
import Field
import Interface


def first_floor(screen):
    clock = pygame.time.Clock()
    run = True

    enemy_positions = [(900, 150), (1000, 300), (900, 450)]
    for enemy,pos in zip(Field.enemies, enemy_positions):
        enemy.set_position(pos[0], pos[1])
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        

        screen.fill((30,30,30))

        Interface.draw_top_hud(screen)
        alive_allies = Field.allies_alive()
        alive_enemies = Field.enemies_alive()

        Interface.auto_layout(positions_x=200, start_y=150, gap=150, objects=alive_allies)
        Interface.auto_layout(positions_x=900, start_y=150, gap=150, objects=alive_enemies)

        for ally in Field.allies:
            if ally.animator:
                ally.animator.update()
                ally.animator.draw(screen, ally.position)
                Interface.show_status(screen, ally)
        
        for enemy in Field.enemies:
            enemy.animator.update()
            enemy.animator.draw(screen, enemy.position)
            Interface.show_status(screen, enemy)

        pygame.display.flip()
        clock.tick(60)

        """
        turn += 1
        Field.start_turn()

        # ───────────────────────
        # 아군 행동 (2번)
        # ───────────────────────
        for action_idx in range(2):
            print("\n" * 40)
            print(f"(아군) 턴 {turn} - {action_idx+1}번째 행동")
            Interface.show_status()

            # 아군 선택
            while True:
                print("행동할 아군 번호를 선택하세요:")
                try:
                    idx = int(input().strip()) - 1
                except ValueError:
                    print("숫자를 입력하세요.")
                    continue

                allies_alive = Field.allies_alive()
                if 0 <= idx < len(allies_alive):
                    selected = allies_alive[idx]
                    break
                print("잘못된 번호입니다.")

            # 행동 선택
            while True:
                print(f"기본공격 : 1 | {selected.skill_name} : 2")
                act = input().strip()

                if act == "1":
                    selected.basic_attack()
                    break
                elif act == "2":
                    if selected.can_use_skill():
                        selected.skill()
                        break
                    else:
                        print("스킬 포인트 부족!")
                else:
                    print("1 또는 2를 입력하세요.")

            Interface.pause()

            # 적 전멸 체크
            if not Field.enemies_alive():
                print("던전 1층 클리어!")
                return True

        # ───────────────────────
        # 적 공격 1
        # ───────────────────────
        print("\n" * 40)
        print(f"(적) 턴 {turn} - 1번째 행동")
        Interface.show_status()

        enemies_alive = Field.enemies_alive()
        if enemies_alive:
            e1 = random.choice(enemies_alive)
            print("적이 기본 공격을 시전합니다!")
            Interface.pause()
            e1.basic_attack()
            Interface.pause()

        # 아군 전멸 체크
        if not Field.allies_alive():
            print("던전 1층 실패!")
            return False

        # ───────────────────────
        # 적 공격 2 (스킬)
        # ───────────────────────
        print("\n" * 40)
        print(f"(적) 턴 {turn} - 2번째 행동")
        Interface.show_status()

        enemies_alive = Field.enemies_alive()
        if enemies_alive:
            e2 = random.choice(enemies_alive)
            print("적이 스킬을 사용합니다!")
            Interface.pause()
            e2.skill()
            Interface.pause()

        if not Field.allies_alive():
            print("던전 1층 실패!")
            return False
        """