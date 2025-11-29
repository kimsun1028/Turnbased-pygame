# Slime.py
import random
import Field
from Enemy import Enemy


class Slime(Enemy):
    def __init__(self, name: str):
        super().__init__(name=name, hp=150, power=35)
        self.job = "슬라임"
        self.job_eng = "Slime"
        self.set_position(0,0)
        self.add_anim("Idle",  scale=3, fps=8,  loop=True)
        self.add_anim("Walk",  scale=3, fps=10, loop=True)
        self.add_anim("Basic", scale=3, fps=10, loop=False)
        self.add_anim("Hurt",  scale=3, fps=12, loop=False, duration = 0.3)
        self.add_anim("Death", scale=3, fps=12, loop=False)
        self.add_anim("Skill",  scale=3, fps=10, loop=True)

    def basic_attack(self):
        target1 = random.choice(Field.allies_alive())
        super().basic_attack(
            target=target1,
            anim="Basic",
            hit_frame=5,
            damage=self.power,
            move_in=True,
            move_back=True,
            is_enemy=True
        )

    def skill(self):
        target1 = random.choice(Field.allies_alive())
        super().basic_attack(
            target=target1,
            anim="Skill",
            hit_frame=9,
            damage=self.power,
            move_in=True,
            move_back=True,
            is_enemy=True
        )
        target2 = random.choice(Field.allies_alive())
        super().basic_attack(
            target=target2,
            anim="Skill",
            hit_frame=9,
            damage=self.power,
            move_in=True,
            move_back=True,
            is_enemy=True
        )

