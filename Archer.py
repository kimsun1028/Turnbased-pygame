import time
import random

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

    def basic_attack(self, target1=None, target2=None):
        
        """
        아처 기본공격:
        - 두 명의 적을 타격 (target1, target2)
        - 타겟을 지정하지 않으면 살아있는 적을 자동 선택
        - 적이 1명만 남으면 그 적을 두 번 타격
        - 원거리 캐릭이므로 이동 없음
        """

        # 🔥 살아있는 적 리스트
        enemies = Field.enemies_alive()

        if len(enemies) == 0:
            print("타격할 대상이 없습니다.")
            return

        # 🔥 target1 자동 보정
        if target1 is None:
            target1 = enemies[0]

        # 🔥 target2 처리
        if len(enemies) == 1:
            # 적이 1명 → 두 번 공격
            target2 = target1
        else:
            if target2 is None:
                # 두 명 이상일 때 target2 자동 선택
                # 단 target1과 동일하면 다음 적으로
                for e in enemies:
                    if e != target1:
                        target2 = e
                        break
            # 그래도 None인 경우 (적이 1명뿐이라는 뜻)
            if target2 is None:
                target2 = target1

        # 🔥 원거리 데미지 계산
        damage = int(self.power * 0.75)

        # 🔥 기존 행동 제거
        self.queue_clear()

        # 1) 공격 애니메이션 재생
        self.queue_push("Basic", None)

        # 2) 타격 예약
        # 첫 번째 타격 - 2프레임
        self.hit_on_frame("Basic", frame_index=7, target=target1, damage=damage)

        # 두 번째 타격 - 4프레임
        self.hit_on_frame("Basic", frame_index=14, target=target2, damage=damage)

        print(f"[아처 기본공격] {target1.job}, {target2.job} 에게 각각 {damage} 데미지!")

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
