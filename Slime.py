# Slime.py
import random
import Field
from Enemy import Enemy


class Slime(Enemy):
    def __init__(self, name: str):
        super().__init__(name=name, hp=150, power=30)
        self.job = "슬라임"
        self.job_eng = "Slime"
        self.set_position(0,0)
        self.add_anim("Idle",  scale=3, fps=8,  loop=True)
        self.add_anim("Walk",  scale=3, fps=10, loop=False)
        self.add_anim("Basic", scale=3, fps=10, loop=False)
        self.add_anim("Hurt",  scale=3, fps=12, loop=False, duration = 0.3)
        self.add_anim("Death", scale=3, fps=12, loop=False)
        self.add_anim("Skill",  scale=3, fps=10, loop=False, duration = 0.7)

    def basic_attack(self):
        target = self.select_target()
        if target is None:
            return

        super().basic_attack(
            target=target,
            anim="Basic",
            hit_frame=5,
            damage=self.power,
            move_in=True,
            move_back=True,
            is_enemy=True
        )

    def skill(self):
        """
    A 모드: 슬라임 스킬을 사용하면,
    1) 슬라임 자신이 강한 공격을 먼저 하고
    2) 이어서 살아있는 모든 슬라임이 순서대로 기본공격을 한다.
    """

    # 먼저 스킬 자체 공격
        target = self.select_target()
        if not target:
            return

        # 스킬 이펙트(강하게 한 번 공격)
        super().basic_attack(
            target=target,
            anim="Skill",
            hit_frame=9,
            damage=int(self.power * 2),   # 스킬 데미지 (원하면 조절)
            move_in=True,
            move_back=True,
            is_enemy=True
        )

        



