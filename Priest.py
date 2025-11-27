import Field
from Character import Character


class Priest(Character):
    def __init__(self):
        super().__init__(
            power=30,
            max_hp=70,
            job="프리스트",
            job_eng="Priest",
            skill_cost=1,
            skill_name="힐/딜(1)",
        )


    def skill(self):
        Field.skill_point -= 1
        print("스킬유형을 선택하세요  힐(1) / 딜(2)")
        mode = input().strip()

        # 힐
        if mode == "1":
            allies_alive = Field.allies_alive()
            print("아군 대상을 선택하세요:")
            idx = int(input().strip()) - 1

            if 0 <= idx < len(allies_alive):
                target = allies_alive[idx]
                target.heal(self.power * 2)
            else:
                print("잘못된 대상입니다.")

        # 딜
        elif mode == "2":
            enemies_alive = Field.enemies_alive()
            print("적 대상을 선택하세요:")
            idx = int(input().strip()) - 1

            if 0 <= idx < len(enemies_alive):
                target = enemies_alive[idx]
                target.take_damage(int(self.power * 1.5))
            else:
                print("잘못된 대상입니다.")

        else:
            print("잘못된 입력입니다.")
