import random
import Field
from Character import Character
from Knight import Knight   

class Enemy(Character):
    def __init__(self, name: str, hp: int, power: int):
        # Enemy도 Character를 그대로 상속하므로 super() 사용
        super().__init__(power=power, max_hp=hp, job=name)

    def select_target(self):
        """도발 여부를 고려하여 공격할 아군을 선택"""

        # 1) 도발 상태라면 → Knight만 공격 가능
        if Field.is_taunt():
            alive_knights = [c for c in Field.allies_alive() if isinstance(c, Knight)]
            if alive_knights:
                return random.choice(alive_knights)

        # 2) 기본: 살아있는 모든 아군 중 랜덤 선택
        alive_allies =Field.allies_alive()
        if not alive_allies:
            return None   # 공격할 대상 없음

        return random.choice(alive_allies)
