import Field
from Character import Character
from Effects import StaticEffect
from Animation import SpriteAnimator

class Wizard(Character):
    def __init__(self):
        super().__init__(
            power=60,
            max_hp=100,
            job="위자드",
            job_eng="Wizard",
            skill_cost=2,
            skill_name="블리자드"  
        )

        self.ult_remain = 2
        self.basic_desc = "       | 지정한 적에게 피해를 입힙니다."
        self.skill_desc = f" | 얼음결정을 소환해 모든 적에게 피해를 입힙니다. (강화 남은 횟수 = {self.ult_remain})"
        

    def basic_attack(self, target):
        Field.skill_point +=1
        super().basic_attack(
            target=target,
            anim="Basic",
            hit_frame=11,
            damage=self.power,
            move_in=True,
            move_back=True            
            )
        
    def skill(self, target=None):
        # 🔥 딜 이펙트 추가
        attack_anim = SpriteAnimator(
            "animation/Wizard/Wizard-Skill_Effect.png",
            scale=4.0,
            loop=False,
            duration=0.7       )
        ult_anim =  SpriteAnimator(
            "animation/Wizard/Wizard-Skill_Effect.png",
            scale=8.0,
            loop=False,
            duration=1.0       )

        Field.skill_point -= 2
        # Wizard 평타 애니메이션
        self.queue_clear()
        self.queue_push("Skill")
        hit_frame = 7
        damage = self.power*3//4
        tx,ty = Field.enemies[1].position
        enemies_alive = Field.enemies_alive()
        if self.ult_remain > 0:
            self.ult_remain -= 1
            Field.effects.add(StaticEffect(attack_anim, (tx-200, ty-200), duration=1.0))
            for target in enemies_alive:
                if target and target.is_alive:
                    self.hit_on_frame("Skill", hit_frame, target, damage)
            if self.ult_remain == 0:
                self.skill_desc = f" | 거대 얼음결정을 소환해 모든 적에게 강력한 피해를 입힙니다. (강화)"
        else:
            Field.effects.add(StaticEffect(ult_anim, (tx-400, ty-400), duration=1.0))
            for target in enemies_alive:
                if target and target.is_alive:
                    self.hit_on_frame("Skill", hit_frame+3, target, damage*2)
            self.ult_remain += 2
        self.skill_desc = f" | 얼음결정을 소환해 모든 적에게 피해를 입힙니다. (강화 남은 횟수 = {self.ult_remain})"
                    
        

       



 
    