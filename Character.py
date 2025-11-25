import time
import Field
import Animation


class Character:
    def __init__(self, power=0, max_hp=0, job="", skill_cost=0, skill_name=""):
        self.power = power
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.skill_cost = skill_cost
        self.job = job
        self.skill_name = skill_name
        self.animator = None
        self.position = (0,0)


    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    # 기본공격 메서드 (특정 class 오버라이드)
    def basic_attack(self):
        print("대상을 입력하세요 : ")
        enemy_index = int(input().strip()) - 1

        enemies_alive = Field.enemies_alive()
        if enemy_index < 0 or enemy_index >= len(enemies_alive):
            print("번호에 해당하는 적이 없습니다!")
            return

        target = enemies_alive[enemy_index]
        target.take_damage(self.power)

        Field.skill_point += 1
        if Field.skill_point > Field.max_skill_point:
            Field.skill_point = Field.max_skill_point

    # 스킬 메서드
    # 자식 클래스에서 반드시 오버라이드!!!!
    def skill(self):        
        raise NotImplementedError

    # 데미지를 입는 메서드
    def take_damage(self, damage: int):
        time.sleep(0.4)
        self.current_hp -= damage

        if self.current_hp <= 0:
            self.current_hp = 0
            print(f"{self.job}이(가) {damage}의 피해를 입고 사망했습니다.")
        else:
            print(
                f"{self.job}이(가) {damage}의 피해를 입었습니다. "
                f"(HP : {self.current_hp}/{self.max_hp})"
            )

    def heal(self, amount: int):
        time.sleep(1.0)

        if self.current_hp + amount >= self.max_hp:
            heal_amount = self.max_hp - self.current_hp
        else:
            heal_amount = amount

        self.current_hp += heal_amount
        print(
            f"{self.job}이(가) {heal_amount}만큼 체력을 회복했습니다! "
            f"(HP : {self.current_hp}/{self.max_hp})"
        )

    def can_use_skill(self) -> bool:
        return Field.skill_point >= self.skill_cost


    def set_animator(self, file_path, scale=2.0, fps=8):
        self.animator = Animation.SpriteAnimator(file_path, scale, fps)

    def set_position(self,x,y):
        self.position = (x,y)