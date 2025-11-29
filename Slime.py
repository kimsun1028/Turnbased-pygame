# Slime.py
import random
import Field
from Enemy import Enemy


class Slime(Enemy):
    def __init__(self, name: str):
        super().__init__(name=name, hp=150, power=40)
        self.job = "슬라임"
        self.job_eng = "Slime"
        self.set_position(0,0)
        self.add_anim("Idle",  scale=3, fps=8,  loop=True)
        self.add_anim("Walk",  scale=3, fps=10, loop=False)
        self.add_anim("Basic", scale=3, fps=10, loop=False)
        self.add_anim("Hurt",  scale=3, fps=12, loop=False, duration = 0.3)
        self.add_anim("Death", scale=3, fps=12, loop=False)
        self.add_anim("Skill",  scale=3, fps=10, loop=False)

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
        damage = (3 * self.power) // 2
        self.queue_clear()
        x,y = self.position
        target1 = random.choice(Field.allies_alive())
        self.move_to((target1.position[0] + 100 , target1.position[1]), duration = 0.25)
        self.queue_push("Skill", None)
        if target1 is not None:
            # schedule first hit at the correct time after the initial move
            anim = self.animations.get("Skill")
            if anim:
                tpf = getattr(anim, 'time_per_frame', 0.0)
                duration = getattr(anim, 'duration', 0.0)
            else:
                tpf = 0.0
                duration = 0.0

            move_dur = 0.25
            start1 = move_dur
            hit_delay1 = start1 + 8 * tpf
            self.hit_in(hit_delay1, target1, damage, source=self)
        target2 = random.choice(Field.allies_alive())
        self.move_to((target2.position[0] + 100 , target2.position[1]), duration = 0.25)
        self.queue_push("Skill",None)
        if target2 is not None:
           # the second skill animation starts after first move + skill duration + second move
           anim = self.animations.get("Skill")
           if anim:
               tpf = getattr(anim, 'time_per_frame', 0.0)
               duration = getattr(anim, 'duration', 0.0)
           else:
               tpf = 0.0
               duration = 0.0

           move_dur = 0.25
           start2 = move_dur + duration + move_dur
           hit_delay2 = start2 + 8 * tpf
           self.hit_in(hit_delay2, target2, damage, source=self)
        self.move_to((x,y), duration = 0.25) 
        

