# Slime.py
from Enemy import Enemy


class Slime(Enemy):
    """
    전형적인 RPG 몹 슬라임 클래스입니다.
    """
    def __init__(self, name: str):
        super().__init__(name=name, hp=150, power=30)
        self.job = "슬라임"
        self.job_eng = "Slime"
        self.set_position(0,0)
        self.add_anim("Idle",   fps=8,  loop=True)
        self.add_anim("Walk",   fps=10, loop=False)
        self.add_anim("Basic",  fps=10, loop=False)
        self.add_anim("Hurt",   fps=12, loop=False, duration = 0.3)
        self.add_anim("Death",  fps=12, loop=False)
        self.add_anim("Skill",   fps=10, loop=False, duration = 0.7)

    def basic_attack(self):
        """
        슬라임 기본공격 메서드
        """
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
        슬라임 스킬 메서드
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
            damage=int(self.power * 2),   
            move_in=True,
            move_back=True,
            is_enemy=True
        )

        



