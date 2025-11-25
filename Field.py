remain_taunt_turn = 0
skill_point = 2
max_skill_point = 4
party_len = 3
turn = 1

# allies: 플레이어 캐릭터 객체 리스트
# enemies: 적 객체 리스트
allies = []
enemies = []


def is_taunt():
    return remain_taunt_turn > 0


def allies_alive():
    return [c for c in allies if c.is_alive]


def enemies_alive():
    return [e for e in enemies if e.is_alive]


def start_turn():
    global remain_taunt_turn

    if is_taunt():
        remain_taunt_turn -= 1
        if not is_taunt():
            # 도발이 끝나는 순간 나이트의 최대 체력 50 감소
            for c in allies_alive():
                if c.job == "나이트":
                    c.max_hp -= 50
                    if c.current_hp > c.max_hp:
                        c.current_hp = c.max_hp
