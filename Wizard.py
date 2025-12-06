import Field
from Character import Character
from Effects import StaticEffect
from Animation import SpriteAnimator

class Wizard(Character):
    """
    위자드 클래스입니다. 판타지 RPG 직업에서 가장 전형적인 마법사를 구현하였습니다.
    캐릭터.py의 자식 클래스로 기본공격과 스킬을 추가로 구현하였습니다.
    """
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
        
    # -----------------------------
    # 기본 공격 메서드
    # -----------------------------
    def basic_attack(self, target):
        """
        기본 기본 공격 메서드
        """
        Field.skill_point +=1
        super().basic_attack(
            target=target,
            anim="Basic",
            hit_frame=11,
            damage=self.power,
            move_in=True,
            move_back=True            
            )
    
    # -----------------------------
    # 스킬 메서드
    # -----------------------------
    def skill(self, target=None):
        """
        블리자드 이펙트를 적 중앙에 출력
        모든 적이 take_damage
        3번중 한번 더욱 커진 이펙트 출력
        """
        # 기본 스킬 이펙트
        attack_anim = SpriteAnimator(
            "animation/Wizard/Wizard-Skill_Effect.png",
            scale=4.0,
            loop=False,
            duration=0.7       )
        
        # 3번중 한번 쓰는 궁극기 이펙트 (스케일만 커짐)
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
                    
        

       



 
    