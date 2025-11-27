import Field
import Animation


class Character:
    def __init__(self, power=0, max_hp=0, job="",job_eng="", skill_cost=0, skill_name=""):
        # 기본 스탯
        self.power = power
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.skill_cost = skill_cost
        self.job = job
        self.job_eng = job_eng
        self.skill_name = skill_name
        
        # 위치 정보
        self.position = (0,0)

        # 애니메이터 정보
        self.animations = {}    # 애니매이션 정보 저장 set
        self.current_anim = None    # 재생중인 애니메이션 정보

        # 매우중요!!!! 애니메이션 큐
        self.anim_queue = []
        self.queue_time = 0.0   # 현재 큐 내 항목 경과 시간

        self.moving = False
        self.move_start = None
        self.move_target = None
        self.move_speed = 300
        self.move_duration = 0
        self.move_elapsed = 0

    # 생존 정보
    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    # 애니메이션 추가 메서드
    def add_anim(self, state, scale = 2.0, fps = 8, loop = True):
        path = f"animation/{self.job_eng}/{self.job_eng}-{state}.png"

        self.animations[state] = Animation.SpriteAnimator(path,scale,fps,loop)

        if self.current_anim is None:
            self.current_anim = state 


    def queue_push(self, state, duration=None):
        self.anim_queue.append((state, duration))

    def queue_clear(self):
        self.anim_queue.clear()

def queue_update(self, dt):
    # 큐가 비었으면 Idle로 복귀
    if not self.anim_queue:
        if "Idle" in self.animations and self.current_anim != "Idle" and self.is_alive:
            idle_anim = self.animations["Idle"]
            idle_anim.reset()
            self.current_anim = "Idle"
        return

    state, data = self.anim_queue[0]

    # ────────────────────────────
    #       1) 이동 명령 처리
    # ────────────────────────────
    if state == "__move__":
        start_pos, target_pos, duration = data

        # 이동 시작 초기화
        if not self.moving:
            self.moving = True
            self.move_start = start_pos
            self.move_target = target_pos
            self.move_duration = duration
            self.move_elapsed = 0.0

            # Walk 애니로 전환
            if "Walk" in self.animations and self.current_anim != "Walk":
                self.animations["Walk"].reset()
                self.current_anim = "Walk"

        # 이동 진행
        self.move_elapsed += dt
        t = min(self.move_elapsed / self.move_duration, 1.0)

        # 보간 (linear interpolation)
        sx, sy = self.move_start
        tx, ty = self.move_target
        nx = sx + (tx - sx) * t
        ny = sy + (ty - sy) * t
        self.position = (nx, ny)

        # 이동 종료
        if t >= 1.0:
            self.moving = False
            self.anim_queue.pop(0)
        return  # 이동은 여기서 종료

    # ────────────────────────────
    #       2) 일반 애니메이션 처리
    # ────────────────────────────
    state, duration = self.anim_queue[0]

    if self.current_anim != state:
        anim = self.animations[state]
        anim.reset()
        self.current_anim = state
        self.queue_time = 0.0

    self.queue_time += dt

    # duration이 있는 경우
    if duration is not None:
        if self.queue_time >= duration:
            self.anim_queue.pop(0)
            return

    # duration이 None이고 애니가 끝난 경우
    anim = self.animations[state]
    if duration is None and anim.finished:
        self.anim_queue.pop(0)


    # 애니메이션 업데이트 메서드
    def update(self, dt):
        self.queue_update(dt)
        if self.current_anim:
            self.animations[self.current_anim].update(dt)

    # 화면 출력 메서드
    def draw(self,screen):
        if self.current_anim:
            self.animations[self.current_anim].draw(screen, self.position)

    # 위치 설정 메서드
    def set_position(self,x,y):
        self.position = (x,y)

    def move_to(self, target_pos, duration = None):
        self.move_target = target_pos
        self.anim_queue.append(("__move__",duration))
    


    # 기본공격 메서드 (특정 class 오버라이드)
    """
    def basic_attack(self):
        print("대상을 입력하세요 : ")
        enemy_index = int(input()) - 1
        enemies_alive = Field.enemies_alive()

        # 예외 처리
        if not (0 <= enemy_index < len(enemies_alive)):
            print("번호에 해당하는 적이 없습니다!")
            return

        # 기본공격 애니메이션 재생
        self.queue_clear()
        self.queue_push("Basic", None)

        # 적에게 데미지 입히기
        target = enemies_alive[enemy_index]
        target.take_damage(self.power)

        # 스킬 포인트 회복
        Field.skill_point += 1
        if Field.skill_point > Field.max_skill_point:
            Field.skill_point = Field.max_skill_point
    """
    # 스킬 메서드
    # 자식 클래스에서 반드시 오버라이드!!!!
    def skill(self):        
        raise NotImplementedError

    # 데미지를 입는 메서드
    def take_damage(self, damage):
        self.current_hp -= damage

        if self.current_hp <= 0:
            self.current_hp = 0
            print(f"{self.job}이(가) {damage}의 피해를 입고 사망했습니다.")
            self.queue_push("Death", None)
        else:
            print(
                f"{self.job}이(가) {damage}의 피해를 입었습니다. "
                f"(HP : {self.current_hp}/{self.max_hp})"
            )
            self.queue_push("Hurt", 0.3)

    def heal(self, amount):
        heal_amount = min(amount, self.max_hp - self.current_hp)
        self.current_hp += heal_amount
        print(
            f"{self.job}이(가) {heal_amount}만큼 체력을 회복했습니다! "
            f"(HP : {self.current_hp}/{self.max_hp})"
        )
        self.queue_push("Heal",0.5)

    def can_use_skill(self) -> bool:
        return Field.skill_point >= self.skill_cost

