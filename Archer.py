import time
import random
from Animation import SpriteAnimator
import Field
from Character import Character


class Archer(Character):
    def __init__(self):
        super().__init__(
            power=4000,
            max_hp=100,
            job="아처",
            job_eng="Archer",
            skill_cost=2,
            skill_name="난사(2)",
        )

        self.basic_desc = "     | 지정한 두 명의 적에게 연속 사격으로 피해를 입힙니다."
        self.skill_desc = " | 무작위 10명의 적에게 화살을 난사하여 피해를 입힙니다."
    def basic_attack(self, target1, target2=None):

        self.queue_clear()
        anim = "Basic"
        hit1_frame = 8
        hit2_frame = 14
        dmg = self.power

        # 기본 공격 애니 재생
        self.queue_push(anim, None)
        # -----------------------------
        # 첫 번째 타격
        # -----------------------------
        if target1 and target1.is_alive:
            self.hit_on_frame(anim, hit1_frame, target1, dmg)

        # -----------------------------
        # 두 번째 대상 결정
        # -----------------------------
        if target2 is None or not target2.is_alive:
            target2 = target1

        # -----------------------------
        # 두 번째 타격
        # -----------------------------
        self.hit_on_frame(anim, hit2_frame, target2, dmg)
    
    def skill(self):
        Field.skill_point -= self.skill_cost
        print("아처가 '화살 난사'를 시전합니다!")
        total_hits = 10
        damage_per_hit = int(self.power * 0.4)
        self.queue_clear()
        anim = "Skill"
        hit_start_frame = 12
        self.queue_push(anim, None)
        
        for _ in range(total_hits):
            enemies_alive = Field.enemies_alive()
            # 적이 모두 죽었으면 스킬 종료
            if not enemies_alive:
                self.queue_clear()
                self.queue_push("Idle", None)
                return
            target = random.choice(enemies_alive)

            expected_hp  = target.current_hp - damage_per_hit
            if expected_hp <= 0:
                enemies_alive.remove(target)
                if not enemies_alive:
                    self.queue_clear()
                    self.queue_push("Idle", None)
                    return
                
                target = random.choice(enemies_alive)

            self.hit_on_frame(anim, hit_start_frame, target,  damage_per_hit)
            hit_start_frame += 6
            
