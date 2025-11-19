# Interface.py
import Field


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
