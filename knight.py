import Field
from Character import Character

class Knight(Character):
    def __init__(self):
        super().__init__(power=40, max_hp=150, job="나이트", job_eng="Knight",
                         skill_cost=2, skill_name="도발")


    def take_damage(self, damage: int):
        super().take_damage(damage)
        if self.current_hp == 0:
            Field.remain_taunt_turn = 0

    def skill(self):
        """도발 스킬"""
        # 도발 지속 2턴
        Field.remain_taunt_turn = 2

        # 최대 체력 증가 (원본 C#: 도발 시 MaxHP 증가)
        self.max_hp = 200

        # 회복 효과 +20
        self.current_hp += 20
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        # 스킬포인트 소모
        Field.skill_point -= 1

        self.queue_push("Skill")

    def basic_attack(self, target):
        # TauntBasic 애니를 3프레임째에 타격하는 근접 공격
        Field.skill_point += 1
        if Field.is_taunt():
            damage = self.power + (self.max_hp - self.current_hp)//3
            super().basic_attack(
            target=target,
            anim="TauntBasic",
            hit_frame=9,
            damage=damage,
            move_in=True,
            move_back=True
        )
        else:
            super().basic_attack(
                target=target,
                anim="Basic",
                hit_frame=5,
                damage=self.power,
                move_in=True,
                move_back=True
            )