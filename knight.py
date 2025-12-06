import Field
from Character import Character

class Knight(Character):
    """
    나이트 클래스입니다. 판타지 RPG 직업에서 가장 전형적인 기사를 구현하였습니다.
    캐릭터.py의 자식 클래스로 기본공격과 스킬, 도발 시 take_damage를 추가로 구현하였습니다.
    """
    def __init__(self):
        super().__init__(power=40, max_hp=150, job="나이트", job_eng="Knight",
                         skill_cost=1, skill_name="도발")
        
        self.basic_desc = "         | 지정한 적에게 공격해 피해를 입힙니다."
        self.sbasic_desc = " | 지정한 적에게 공격해 더 강한 피해를 입힙니다."
        self.skill_desc = "        | 3턴 동안 적을 도발합니다."

    # -----------------------------
    # take_damage 오버라이드 메서드
    # -----------------------------
    def take_damage(self, damage: int):
        """
        도발중일 때 데미지를 25% 경감합니다.
        """
        if Field.is_taunt():
            damage = damage*3//4
        super().take_damage(damage)
        if self.current_hp == 0:
            Field.remain_taunt_turn = 0

    # -----------------------------
    # 스킬 메서드
    # -----------------------------
    def skill(self):
        """
        Field.남은 도발 턴 += 3
        체력 회복 50, 최대 체력 50증가
        """
        # 도발 지속 2턴
        Field.remain_taunt_turn += 3

        # 최대 체력 증가 (원본 C#: 도발 시 MaxHP 증가)
        self.max_hp = 200

        # 회복 효과 + 50
        self.current_hp += 50
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        # 스킬포인트 소모
        Field.skill_point -= 1

        self.queue_push("Skill")


    # -----------------------------
    # 기본 공격 메서드
    # -----------------------------
    def basic_attack(self, target):
        """
        도발중일 경우 애니메이션과 데미지가 다르게 계산됩니다
        """
        Field.skill_point += 1
        if Field.is_taunt():
            damage = self.power + (self.max_hp - self.current_hp)//5
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