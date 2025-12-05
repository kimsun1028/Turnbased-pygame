import Field
from Character import Character
from Effects import StaticEffect
from Animation import SpriteAnimator

class Priest(Character):
    def __init__(self):
        super().__init__(
            power=30,
            max_hp=100,
            job="프리스트",
            job_eng="Priest",
            skill_cost=1,
            skill_name="힐"  
        )

        self.basic_desc = "지정한 적에게 POWER 100%의 피해를 입힙니다."
        self.skill_desc = "지정한 아군에게 POWER 200%만큼 체력을 회복시키고 가장 체력이 적은 아군에게 POWER 100%만큼 회복시킵니다."

    def basic_attack(self, target):
        Field.skill_point += 1
        # Priest 평타 애니메이션
        self.queue_clear()
        self.queue_push("Basic")

        
        # 🔥 딜 이펙트 추가
        attack_anim = SpriteAnimator(
            "animation/Priest/Priest-Attack_Effect.png",
            scale=2.0,
            loop=False,
            duration=0.5
        )
        self.hit_on_frame("Basic", 3, target, self.power)
        tx, ty = target.position
        Field.effects.add(
            StaticEffect(attack_anim, (tx-100, ty-100), duration=1.0)
        )

 
    
            
    def skill(self, idx):
        """
        스킬: 힐
        idx: allies_alive()에서 힐할 대상의 index
        """

        # 살아있는 아군 목록 가져오기
        alive_allies = Field.allies_alive()

        # idx 범위 체크
        if idx < 0 or idx >= len(alive_allies):
            print("잘못된 대상입니다.")
            return

        # 대상 선택
        target = alive_allies[idx]

        # 스킬포인트 체크
        if Field.skill_point < self.skill_cost:
            print("스킬 포인트 부족!")
            return

        Field.skill_point -= self.skill_cost

        # Priest 스킬 애니메이션
        self.queue_clear()
        self.queue_push("Skill", None)

        # 힐량 계산
        heal_amount = int(self.power * 2.0)
        #
        subheal_amount = int(self.power * 1.0)

        # 실제 힐 적용
        target.heal(heal_amount)
        #
        alive_allies = Field.allies_alive()
        patient = sorted(alive_allies,reverse = True, key = lambda x : x.max_hp - x.current_hp)[0]
        patient.heal(subheal_amount)

        # 🔥 힐 이펙트 추가
        heal_anim1 = SpriteAnimator(
            "animation/Priest/Priest-Heal_Effect.png",
            scale=2.0,
            loop=False,
            duration=0.6
        )
        tx, ty = target.position
        Field.effects.add(
            StaticEffect(heal_anim1, (tx-100, ty-100), duration=1.0)
        )
        #
        if patient is not target:
            heal_anim2 = SpriteAnimator(
            "animation/Priest/Priest-Heal_Effect.png",
            scale=2.0,
            loop=False,
            duration=0.6
            )
            ox,oy = patient.position
            Field.effects.add(
            StaticEffect(heal_anim2, (ox-100, oy-100), duration=1.0)
        )

        print(f"[프리스트 힐] {target.job}에게 {heal_amount} 회복!")
