# Orc.py
from Enemy import Enemy


class Orc(Enemy):
    def __init__(self, name: str):
        super().__init__(name=name, hp=150, power=30)
        self.job = "오크"
        self.job_eng = "Orc"
        self.set_position(0,0)
        self.add_anim("Idle",   fps=8,  loop=True)
        self.add_anim("Walk",   fps=10, loop=False)
        self.add_anim("Basic",  fps=10, loop=False)
        self.add_anim("Hurt",   fps=12, loop=False, duration = 0.3)
        self.add_anim("Death",  fps=12, loop=False)
        self.add_anim("Skill",   fps=10, loop=False, duration = 0.7)

    def basic_attack(self):
        target = self.select_target()
        if target is None:
            return

        super().basic_attack(
            target=target,
            anim="Basic",
            hit_frame=4,
            damage=self.power,
            move_in=True,
            move_back=True,
            is_enemy=True
        )

    def skill(self):
        target = self.select_target()
        if not target:
            return

        # 스킬 이펙트(강하게 한 번 공격)
        super().basic_attack(
            target=target,
            anim="Skill",
            hit_frame=4,
            damage=int(self.power * 2),   
            move_in=True,
            move_back=True,
            is_enemy=True
        )

        



