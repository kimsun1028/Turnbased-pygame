import Field
import Animation


class Character:
    def __init__(self, power=0, max_hp=0, job="", job_eng="", skill_cost=0, skill_name=""):
        # 기본 스탯
        self.power = power
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.skill_cost = skill_cost
        self.job = job
        self.job_eng = job_eng
        self.skill_name = skill_name

        # 위치 정보
        self.position = (0, 0)

        # 애니메이션 저장소
        self.animations = {}
        self.current_anim = None

        # 애니메이션 큐
        self.anim_queue = []
        self.queue_time = 0.0

        # 이동 관련 데이터
        self.moving = False
        self.move_start = None
        self.move_target = None
        self.move_duration = 0
        self.move_elapsed = 0

    # ---------------------------------------------------------
    # 생존 여부
    # ---------------------------------------------------------
    @property
    def is_alive(self):
        return self.current_hp > 0

    # ---------------------------------------------------------
    # 애니메이션 추가
    # ---------------------------------------------------------
    def add_anim(self, state, scale=2.0, fps=8, loop=True):
        path = f"animation/{self.job_eng}/{self.job_eng}-{state}.png"
        self.animations[state] = Animation.SpriteAnimator(path, scale, fps, loop)

        if self.current_anim is None:
            self.current_anim = state

    # ---------------------------------------------------------
    # 큐 조작
    # ---------------------------------------------------------
    def queue_push(self, state, duration=None):
        self.anim_queue.append((state, duration))

    def queue_clear(self):
        self.anim_queue.clear()
        self.moving = False

    # ---------------------------------------------------------
    # 이동 명령 push
    # ---------------------------------------------------------
    def move_to(self, target_pos, duration=0.4):
        """
        이동 명령을 큐에 추가.
        duration을 지정하지 않으면 0.4초 동안 걷기 이동.
        start_pos는 queue_update에서 자동 계산.
        """
        self.anim_queue.append(("__move__", (target_pos, duration)))

    # ---------------------------------------------------------
    # 큐 업데이트
    # ---------------------------------------------------------
    def queue_update(self, dt):
        if not self.anim_queue:
            # Idle로 복귀
            if (
                "Idle" in self.animations
                and self.current_anim != "Idle"
                and self.is_alive
            ):
                self.animations["Idle"].reset()
                self.current_anim = "Idle"
            return

        state, data = self.anim_queue[0]

        # =====================================================
        # 이동 처리 (__move__)
        # =====================================================
        if state == "__move__":
            target_pos, duration = data

            # 이동 시작 순간
            if not self.moving:
                self.moving = True
                self.move_start = self.position
                self.move_target = target_pos
                self.move_duration = duration
                self.move_elapsed = 0.0

                # 걷기 애니메이션
                if "Walk" in self.animations and self.current_anim != "Walk":
                    self.animations["Walk"].reset()
                    self.current_anim = "Walk"

            # 이동 진행
            self.move_elapsed += dt
            t = min(self.move_elapsed / self.move_duration, 1.0)

            sx, sy = self.move_start
            tx, ty = self.move_target
            nx = sx + (tx - sx) * t
            ny = sy + (ty - sy) * t
            self.position = (nx, ny)

            # 이동 완료
            if t >= 1.0:
                self.moving = False
                self.anim_queue.pop(0)

            return

        # =====================================================
        # 일반 애니메이션 처리
        # =====================================================
        state, duration = self.anim_queue[0]

        if self.current_anim != state:
            anim = self.animations[state]
            anim.reset()
            self.current_anim = state
            self.queue_time = 0.0

        # 시간 경과
        self.queue_time += dt

        # duration이 있는 경우
        if duration is not None:
            if self.queue_time >= duration:
                self.anim_queue.pop(0)
                return
        else:
            # duration이 None이면 애니 끝나는 순간 pop
            anim = self.animations[state]
            if anim.finished:
                self.anim_queue.pop(0)

    # ---------------------------------------------------------
    # update
    # ---------------------------------------------------------
    def update(self, dt):
        self.queue_update(dt)
        if self.current_anim:
            self.animations[self.current_anim].update(dt)

    # ---------------------------------------------------------
    # draw
    # ---------------------------------------------------------
    def draw(self, screen):
        if self.current_anim:
            self.animations[self.current_anim].draw(screen, self.position)

    # ---------------------------------------------------------
    # 위치 지정
    # ---------------------------------------------------------
    def set_position(self, x, y):
        self.position = (x, y)

    # ---------------------------------------------------------
    # 전투 관련 (자식 클래스에서 오버라이드)
    # ---------------------------------------------------------
    def skill(self):
        raise NotImplementedError

    def take_damage(self, damage):
        self.current_hp -= damage

        if self.current_hp <= 0:
            self.current_hp = 0
            print(f"{self.job}이(가) {damage} 피해를 받고 사망했습니다!")
            self.queue_push("Death", None)
        else:
            print(
                f"{self.job}이(가) {damage} 피해를 입었습니다. "
                f"(HP: {self.current_hp}/{self.max_hp})"
            )
            self.queue_push("Hurt", 0.3)

    def heal(self, amount):
        heal_amount = min(amount, self.max_hp - self.current_hp)
        self.current_hp += heal_amount
        print(
            f"{self.job}이(가) {heal_amount} 만큼 회복했습니다! "
            f"(HP: {self.current_hp}/{self.max_hp})"
        )
        self.queue_push("Heal", 0.5)

    def can_use_skill(self):
        return Field.skill_point >= self.skill_cost
