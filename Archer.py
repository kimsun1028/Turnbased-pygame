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

    """
    def basic_attack(self):
        damage = int(self.power * 0.75)

        enemies_alive = Field.enemies_alive()

        # 남은 적이 한 명일 때
        if len(enemies_alive) == 1:
            only = enemies_alive[0]
            print("남은 적이 한 명입니다! 동일 대상에게 2회 타격!")
            only.take_damage(damage)
            only.take_damage(damage)
            return

        # 대상 2명 입력 받기
        print("대상 두 명을 차례대로 입력하세요:")

        # 첫 번째 대상
        while True:
            try:
                idx1 = int(input().strip()) - 1
                if 0 <= idx1 < len(enemies_alive):
                    break
                print("번호에 해당하는 적이 없습니다! 다시 입력:")
            except ValueError:
                print("숫자를 입력하세요!")

        # 두 번째 대상
        while True:
            try:
                idx2 = int(input().strip()) - 1
                if 0 <= idx2 < len(enemies_alive):
                    if idx2 != idx1:
                        break
                    print("같은 대상을 선택할 수 없습니다! 다시 입력:")
                else:
                    print("번호에 해당하는 적이 없습니다! 다시 입력:")
            except ValueError:
                print("숫자를 입력하세요!")

        # 최종 대상
        enemies_alive = Field.enemies_alive()
        target1 = enemies_alive[idx1]
        target2 = enemies_alive[idx2]

        target1.take_damage(damage)
        target2.take_damage(damage)
    """

    def basic_attack(self, target1, target2=None):

        self.queue_clear()

        anim = "Basic"
        hit1_frame = 8
        hit2_frame = 14

        self.queue_push(anim, None)

        # 첫 타격 대상
        if target1 and target1.is_alive:
            self.spawn_arrow_on_frame(anim, hit1_frame, target1, self.power)

        # 두 번째 대상 선택
        if target2 is None or not target2.is_alive:
            target2 = target1

        # 두 번째 화살
        self.spawn_arrow_on_frame(anim, hit2_frame, target2, self.power)



    # =====================================================
    # 화살 이펙트를 특정 프레임에 맞춰 생성하는 함수
    # =====================================================
    def spawn_arrow_on_frame(self, anim_name, frame_index, target, damage):

        anim = self.animations[anim_name]
        delay = frame_index * anim.time_per_frame

        self.hit_events.append({
            "time": delay,
            "spawn_arrow": True,
            "target": target,
            "damage": damage
        })

    def skill(self):
        """아처 스킬: 난사 → 랜덤 적에게 공격력 40% 피해를 10번 분배"""
        Field.skill_point -= 2
        print("아처가 '화살 난사'를 시전합니다!")

        total_hits = 10
        damage_per_hit = int(self.power * 0.4)

        for _ in range(total_hits):
            enemies_alive = Field.enemies_alive()

            # 적이 모두 죽었으면 스킬 종료
            if not enemies_alive:
                print("모든 적이 쓰러져 난사가 조기에 종료됩니다!")
                break

            target = random.choice(enemies_alive)

            print(
                f"→ {target.job}이(가) 난사 타격을 맞습니다! "
                f"({damage_per_hit} 피해)"
            )
            target.take_damage(damage_per_hit)
            time.sleep(0.3)
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
