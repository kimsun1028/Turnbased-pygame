import time
import Field
from Character import Character

class Knight(Character):
    def __init__(self):
        super().__init__(
            power=20,
            max_hp=150,
            job="나이트",
            skill_cost=1,
            skill_name="도발(1)",
        )
        self.set_animator("animation/Knight/Knight-Idle.png")
        self.set_position(100,400)

    def take_damage(self, damage: int):
        time.sleep(0.4)
        self.current_hp -= damage

        # 죽었을 때 도발 즉시 해제
        if self.current_hp <= 0:
            self.current_hp = 0
            Field.remain_taunt_turn = 0
            print(f"{self.job}이(가) {damage}의 피해를 입고 사망했습니다.")
        else:
            print(
                f"{self.job}이(가) {damage}의 피해를 입었습니다. "
                f"(HP : {self.current_hp}/{self.max_hp})"
            )

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

        print("적 도발 성공")

    def basic_attack(self):
        print("대상을 입력하세요 : ")
        enemy_index = int(input().strip()) - 1

        enemies_alive = Field.enemies_alive()
        if enemy_index < 0 or enemy_index >= len(enemies_alive):
            print("번호에 해당하는 적이 없습니다!")
            return

        target = enemies_alive[enemy_index]

        # 도발 중 → 강화된 기본 공격
        if Field.is_taunt():
            damage = self.power + (self.max_hp - self.current_hp) // 2
            target.take_damage(damage)
            print(
                f"기본공격(강화)으로 {target.job}에게 {damage}의 피해를 입혔다!"
            )
        else:
            damage = self.power
            target.take_damage(damage)
            print(
                f"기본공격으로 {target.job}에게 {damage}의 피해를 입혔다!"
            )

        # 스킬포인트 생성
        Field.skill_point += 1
        if Field.skill_point > Field.max_skill_point:
            Field.skill_point = Field.max_skill_point
