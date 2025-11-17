# character.py
import time

class Character:
    def __init__(self, power=0, max_hp=0, job="", skill_name="", skill_cost=0):
        self.power = power
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.job = job
        self.skill_name = skill_name
        self.skill_cost = skill_cost

    @property
    def is_alive(self):
        return self.current_hp > 0

    def act(self, allies, enemies):
        
        # override용 메서드
        
        pass

    def basic_attack(self):
        
        print("대상을 입력하세요 : ", end="")
        enemy_index = int(input()) - 1

        target = Field.enemies_alive[enemy_index]
        target.take_damage(self.power)

        Field.skill_point += 1
        if Field.skill_point > Field.max_skill_point:
            Field.skill_point = Field.max_skill_point

    def skill(self):
        raise NotImplementedError("Skill() must be overridden in subclasses.")

    def take_damage(self, damage):
        time.sleep(0.4)
        self.current_hp -= damage

        if not self.eis_alive():
            # self.current_hp <= 0:
            self.current_hp = 0
            print(f"{self.job}이(가) {damage}의 피해를 입고 사망했습니다.")
        else:
            print(f"{self.job}이(가) {damage}의 피해를 입었습니다. (HP : {self.current_hp}/{self.max_hp})")

    def heal(self, amount):
        time.sleep(1.0)

        if self.current_hp + amount >= self.max_hp:
            heal_amount = self.max_hp - self.current_hp
        else:
            heal_amount = amount

        self.current_hp += heal_amount
        print(f"{self.job}이(가) {heal_amount}만큼 체력을 회복했습니다! (HP : {self.current_hp}/{self.max_hp})")

    def can_use_skill(self):
        return Field.skill_point >= self.skill_cost



# 임시 Field Class
class Field:
    enemies_alive = []       
    skill_point = 0
    max_skill_point = 10
