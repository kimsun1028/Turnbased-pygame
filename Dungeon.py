import pygame
import random
import Field
import Interface



def _is_animating():
    """아군/적 중 애니메이션 큐나 타격 이벤트가 남아 있으면 True"""
    for c in Field.allies + Field.enemies:
        if getattr(c, "anim_queue", None):
            if c.anim_queue:
                return True
        if getattr(c, "hit_events", None):
            if c.hit_events:
                return True
    return False


def _draw_text_lines(screen, font, lines, x, y):
    for i, line in enumerate(lines):
        surf = font.render(line, True, (255, 255, 255))
        screen.blit(surf, (x, y + i * 28))


def floor(screen, bg_path, start_pos = (350,300),gap = 100,gap2 = 600):
    clock = pygame.time.Clock()
    running = True
    
    bg_image = pygame.image.load(bg_path).convert()
    bg_image = pygame.transform.scale(bg_image, (1280, 720))

    # ============================
    # 1) 포지션 배치
    # ============================
    ally_positions = [(start_pos[0], start_pos[1] + i*gap) for i in range(3)]
    for ally, pos in zip(Field.allies, ally_positions):
        ally.set_position(*pos)

    enemy_positions = [(start_pos[0] + gap2, start_pos[1] + i*gap) for i in range(3)]
    for enemy, pos in zip(Field.enemies, enemy_positions):
        enemy.set_position(*pos)

    # ============================
    # 2) 고정 번호 부여
    # ============================
    for i, ch in enumerate(Field.allies):
        ch.fixed_index = i + 1
    for i, en in enumerate(Field.enemies):
        en.fixed_index = i + 1

    # ============================
    # 3) 턴 변수
    # ============================
    Field.skill_point = 3
    Field.turn = 1
    Field.start_turn()
    action_left = 2
    enemy_action_step = 0

    state = "PLAYER_SELECT_ACTOR"
    next_floor_choice = None
    selected_char = None
    selected_action = None
    selected_targets = []

    font = pygame.font.SysFont("malgungothic", 20)

    # =====================================================
    # 메인 루프
    # =====================================================
    while running:
        dt = clock.tick(60) / 1000.0

        # ======================
        # 이벤트 처리
        # ======================
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            # KEYDOWN 외에는 key 속성이 없으므로 반드시 체크
            if event.type != pygame.KEYDOWN:
                continue

            # ============================
            # 다음 층 이동 여부 질문 상태
            # ============================
            if state == "NEXT_FLOOR_QUERY":
                if event.key == pygame.K_y:
                    print("다음 층으로 이동합니다.")
                    return "NEXT"
                elif event.key == pygame.K_n:
                    print("던전을 종료합니다.")
                    return False

            # ============================
            # 아군 선택
            # ============================
            if state == "PLAYER_SELECT_ACTOR":

                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    key_idx = event.key - pygame.K_1 + 1  # 1~3 고정 번호

                    for ch in Field.allies:
                        if ch.fixed_index == key_idx and ch.is_alive:
                            selected_char = ch
                            selected_targets = []
                            selected_action = None
                            state = "PLAYER_SELECT_ACTION"
                            break

            # ============================
            # 행동 선택
            # ============================
            elif state == "PLAYER_SELECT_ACTION" and selected_char is not None:

                # ① 기본 공격
                if event.key == pygame.K_1:
                    selected_action = "BASIC"
                    enemies_alive = Field.enemies_alive()

                    if selected_char.job == "아처":
                        if len(enemies_alive) == 1:
                            selected_char.basic_attack(enemies_alive[0])
                            action_left -= 1
                            state = "WAIT_ANIMATION"
                        else:
                            selected_targets = []
                            state = "PLAYER_SELECT_TARGET"
                    else:
                        selected_targets = []
                        state = "PLAYER_SELECT_TARGET"

                # ② 스킬
                elif event.key == pygame.K_2:
                    selected_action = "SKILL"

                    if not selected_char.can_use_skill():
                        print("스킬 포인트 부족!")
                        continue

                    if selected_char.job == "아처":
                        selected_char.skill()
                        action_left -= 1
                        state = "WAIT_ANIMATION"

                    elif selected_char.job == "프리스트":
                        selected_targets = []
                        state = "PLAYER_SELECT_TARGET"

                    else:
                        selected_char.skill()
                        action_left -= 1
                        state = "WAIT_ANIMATION"

                # ③ 취소
                elif event.key == pygame.K_3:
                    selected_char = None
                    selected_action = None
                    selected_targets = []
                    state = "PLAYER_SELECT_ACTOR"

            # ============================
            # 대상 선택
            # ============================
            elif state == "PLAYER_SELECT_TARGET" and selected_char is not None:

                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    key_idx = event.key - pygame.K_1 + 1

                    # 기본 공격
                    if selected_action == "BASIC":

                        # 아처: 2명 필요
                        if selected_char.job == "아처":
                            for enemy in Field.enemies:
                                if enemy.fixed_index == key_idx and enemy.is_alive:
                                    selected_targets.append(enemy)

                                    if len(selected_targets) == 2:
                                        selected_char.basic_attack(
                                            selected_targets[0],
                                            selected_targets[1]
                                        )
                                        action_left -= 1
                                        state = "WAIT_ANIMATION"
                                    break

                        else:  # 나이트, 프리스트 1명만
                            for enemy in Field.enemies:
                                if enemy.fixed_index == key_idx and enemy.is_alive:
                                    selected_char.basic_attack(enemy)
                                    action_left -= 1
                                    state = "WAIT_ANIMATION"
                                    break

                    # 프리스트 힐
                    elif selected_action == "SKILL" and selected_char.job == "프리스트":

                        for ally in Field.allies:
                            if ally.fixed_index == key_idx and ally.is_alive:
                                alive_list = Field.allies_alive()
                                heal_idx = alive_list.index(ally)
                                selected_char.skill(heal_idx)
                                action_left -= 1
                                state = "WAIT_ANIMATION"
                                break

        # =====================================================
        # 업데이트
        # =====================================================
        for a in Field.allies:
            a.update(dt)
        for e in Field.enemies:
            e.update(dt)
        Field.effects.update(dt)

        # Death 애니가 끝났을 때 큐 정리
        for ch in Field.allies + Field.enemies:
            if not ch.is_alive and ch.current_anim == "Death":
                anim = ch.animations.get("Death")
                if anim and anim.finished:
                    ch.anim_queue.clear()

        # ============================
        # WAIT 상태 → 애니 끝나면 다음 단계
        # ============================
        if state == "WAIT_ANIMATION":

            # 적 전멸 → 다음 층 이동 질문
            if not Field.enemies_alive():
                """
                for ch in Field.allies + Field.enemies:
                    ch.anim_queue.clear()
                    ch.hit_events.clear()
                    ch.current_anim = None
                    """

                state = "NEXT_FLOOR_QUERY"
                next_floor_choice = None
                continue

            if not _is_animating():
                if not Field.allies_alive():
                    pygame.time.delay(800)
                    return False

                if action_left > 0:
                    selected_char = None
                    selected_action = None
                    selected_targets = []
                    state = "PLAYER_SELECT_ACTOR"
                else:
                    enemy_action_step = 0
                    state = "ENEMY_TURN"

        # ============================
        # 적 턴 시작
        # ============================
        if state == "ENEMY_TURN":

            enemies_alive = Field.enemies_alive()
            if not enemies_alive:
                pygame.time.delay(500)
                state = "NEXT_FLOOR_QUERY"
                continue

            attacker = random.choice(enemies_alive)

            if enemy_action_step == 0:
                try:
                    attacker.basic_attack()
                except:
                    allies_alive = Field.allies_alive()
                    if allies_alive:
                        attacker.basic_attack(allies_alive[0])
                state = "ENEMY_WAIT"

            elif enemy_action_step == 1:
                for enemy in enemies_alive:
                    if enemy.isBoss == True:
                        attacker = enemy
                attacker.skill()
                state = "ENEMY_WAIT"

        # ============================
        # 적 WAIT → 애니 끝 → 다음 행동
        # ============================
        if state == "ENEMY_WAIT":
            if not Field.enemies_alive():
                    pygame.time.delay(500)
                    state = "NEXT_FLOOR_QUERY"
                    continue
            
            if not _is_animating():

                if not Field.allies_alive():
                    pygame.time.delay(800)
                    return False

                enemy_action_step += 1
                if enemy_action_step >= 2:
                    Field.turn += 1
                    Field.start_turn()
                    action_left = 2
                    selected_char = None
                    selected_action = None
                    selected_targets = []
                    state = "PLAYER_SELECT_ACTOR"
                else:
                    state = "ENEMY_TURN"

        # ==================================================
        # 렌더링
        # ==================================================
        screen.blit(bg_image, (0, 0))
        Interface.draw_top_hud(screen)

        def should_draw(ch):
            if ch.is_alive:
                return True
            if ch.current_anim == "Death":
                return True
            if ch.anim_queue and ch.anim_queue[0][0] == "Death":
                return True
            return False

        # 아군 출력
        for a in Field.allies:
            if should_draw(a):
                a.draw(screen)
                if a.is_alive:
                    Interface.show_status(screen, a, index=a.fixed_index)

        # 적 출력
        for e in Field.enemies:
            if should_draw(e):
                e.draw(screen)
                if e.is_alive:
                    Interface.show_status(screen, e, index=e.fixed_index)

        Field.effects.draw(screen)

        # 안내 텍스트
        guide_lines = []

        if state == "PLAYER_SELECT_ACTOR":
            guide_lines.append(f"[플레이어 턴] 행동 남은 횟수: {action_left}/2")
            guide_lines.append("아군 선택: 1,2,3")

        elif state == "PLAYER_SELECT_ACTION" and selected_char is not None:
            guide_lines.append(f"선택된 아군: {selected_char.job}")

            if selected_char.job == "나이트" and Field.is_taunt():
                guide_lines.append(f"1: 기본 공격(강화) | {selected_char.sbasic_desc}")
            else:
                guide_lines.append(f"1: 기본 공격  | {selected_char.basic_desc}")

            guide_lines.append(f"2: {selected_char.skill_name}(스킬)  | {selected_char.skill_desc}")
            guide_lines.append("3: 취소")

        elif state == "PLAYER_SELECT_TARGET" and selected_char is not None:
            if selected_action == "BASIC":
                if selected_char.job == "아처":
                    guide_lines.append("공격할 적 2명 선택")
                    guide_lines.append(f"현재 선택 {len(selected_targets)}/2")
                else:
                    guide_lines.append("공격할 적 선택: 1,2,3")

            elif selected_action == "SKILL" and selected_char.job == "프리스트":
                guide_lines.append("힐할 아군 선택: 1,2,3")

        elif state == "NEXT_FLOOR_QUERY":
            guide_lines.append("던전 1층 클리어!")
            guide_lines.append("다음 층으로 이동하시겠습니까? (Y/N)")

        elif state in ("WAIT_ANIMATION", "ENEMY_WAIT"):
            guide_lines.append("진행 중...")

        elif state == "ENEMY_TURN":
            guide_lines.append("[적 턴 진행 중]")

        if guide_lines:
            _draw_text_lines(screen, font, guide_lines, 40, 600)

        pygame.display.flip()

    return False
