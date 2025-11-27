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
        self.add_anim("Hurt",  scale=3, fps=12, loop=False)
        self.add_anim("Death", scale=3, fps=12, loop=False)
        self.add_anim("Skill",  scale=3, fps=10, loop=True)

    def basic_attack(self):
        target = self.select_target()
        if target is None:
            return

        print(f"{self.job}이(가) 기본 공격! → {target.job}에게 {self.power} 피해!")
        target.take_damage(self.power)

    def skill(self):
        """슬라임 난사: 랜덤 2명에게 35 데미지"""
        allies_alive = Field.allies_alive()

        # 대상이 1명일 때 처리
        if len(allies_alive) < 2:
            target = self.select_target()
            if target:
                print(f"{self.job}이(가) 난사! 대상이 1명뿐!")
                target.take_damage(self.power)
            return

        # 도발 상태일 때
        if Field.is_taunt():
            target = self.select_target()
            print(f"{self.job}이(가) 난사! (도발 중)")
            target.take_damage(self.power)

            if target in Field.allies_alive():
                target.take_damage(self.power)
            else:
                extra = self.select_target()
                if extra:
                    extra.take_damage(self.power)
            return

        # 일반 상황: 서로 다른 2명
        t1 = self.select_target()
        t2 = None
        while t2 is None or t2 is t1:
            t2 = self.select_target()

        print(f"{self.job}이(가) 난사! {t1.job}, {t2.job}에게 피해!")
        t1.take_damage(self.power)
        t2.take_damage(self.power)
