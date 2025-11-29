import time
import random
from Animation import SpriteAnimator
import Field
from Character import Character


class Archer(Character):
    def __init__(self):
        super().__init__(
            power=40,
            max_hp=100,
            job="아처",
            job_eng="Archer",
            skill_cost=2,
            skill_name="난사(2)",
        )

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
            

    def add_arrow_effect(self, frame_index, target):
        # 화살 애니메이션 로드
        arrow_anim = SpriteAnimator(
            "animation/Archer/Archer-Arrow.png",
            scale=2.0,
            loop=False,
            duration=0.15
        )

        # 화살 출발 위치는 아처 중심
        sx, sy = self.position

        # 도착 위치는 타겟 중심 (offset으로 보정 가능)
        tx, ty = target.position

        # 호출 시점이 hit_on_frame보다 약간 빨라야 자연스럽다
        self.hit_events.append({
            "time": frame_index * self.animations["Basic"].time_per_frame - 0.05,
            "spawn_arrow": (arrow_anim, (sx, sy), (tx, ty))
        })
