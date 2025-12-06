import random
import Field
from Character import Character
from knight import Knight   

class Enemy(Character):
    """
    모든 적 캐릭터의 공통 부모 클래스
    Character를 상속하며 적 전용 로직(select_target 등)을 포함
    """
    
    def __init__(self, name: str, hp: int, power: int):
        super().__init__(power=power, max_hp=hp, job=name)
        self.facing_right = False  # 플레이어 방향
        self.isBoss = False


    def select_target(self):
        """
        적이 공격할 아군을 선택.
        도발 상태일 경우 Knight만 우선 대상
        """
        # 1) 도발 상태라면 → Knight만 공격 가능
        if Field.is_taunt():
            alive_knights = [c for c in Field.allies_alive() if isinstance(c, Knight)]
            if alive_knights:
                return random.choice(alive_knights)

        # 2) 일반: 모든 아군 중 하나 선택
        alive_allies = Field.allies_alive()
        if not alive_allies:
            return None   # 공격할 대상 없음

        return random.choice(alive_allies)


    def basic_attack(self, target, anim="Basic", hit_frame=5, damage=None, move_in=True, move_back=True, is_enemy=False):
        """
        Enemy는 Character.basic_attack() 구조를 그대로 사용
        매개변수를 그대로 전달하여 사용
        """
        if damage is None:
            damage = self.power

        super().basic_attack(
            target=target,
            anim=anim,
            hit_frame=hit_frame,
            damage=damage,
            move_in=move_in,
            move_back=move_back,
            is_enemy=is_enemy
        )
