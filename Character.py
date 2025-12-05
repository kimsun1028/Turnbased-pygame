import Field
import Animation
import  random
import pygame
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
        self.facing_right = True


        self.basic_desc = ""
        self.skill_desc = ""
        # 위치 정보
        self.position = (0, 0)

        # 애니메이션 저장소
        #   key: 상태 이름("Idle","Walk","Basic" 등)
        #   value: Animation.SpriteAnimator 인스턴스
        self.animations = {}
        self.current_anim = None

        # 애니메이션 큐 (행동 시퀀스)
        # 각 원소: (state, duration)
        #   state   : "Idle","Basic","Skill","Hurt","Death" 혹은 "__move__"
        #   duration: None 이면 애니 끝날 때까지, 숫자면 그 시간 지나면 다음으로
        self.anim_queue = []
        self.queue_time = 0.0

        # 이동 관련 데이터
        self.moving = False
        self.move_start = None
        self.move_target = None
        self.move_duration = 0.0
        self.move_elapsed = 0.0

        # 타격(데미지) 예약 이벤트
        # 각 원소: {"time": 남은시간, "target": 대상, "damage": 데미지}
        self.hit_events = []

    # ---------------------------------------------------------
    # 생존 여부
    # ---------------------------------------------------------
    @property
    def is_alive(self):
        return self.current_hp > 0

    # ---------------------------------------------------------
    # 애니메이션 추가
    # ---------------------------------------------------------
    def add_anim(self, state, scale=2.5, fps=8, loop=True, duration = 0.5):
        """
        state: "Idle", "Walk", "Basic", "Skill", "Hurt", "Death" 등
        animation/{job_eng}/{job_eng}-{state}.png 를 스프라이트 시트로 사용
        """
        path = f"animation/{self.job_eng}/{self.job_eng}-{state}.png"
        self.animations[state] = Animation.SpriteAnimator(path, scale, fps, loop, duration)

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
        self.move_start = None
        self.move_target = None
        self.move_duration = 0.0
        self.move_elapsed = 0.0
        self.queue_time = 0.0

    # ---------------------------------------------------------
    # 이동 명령 push
    # ---------------------------------------------------------
    def move_to(self, target_pos, duration=0.4):
        """
        이동 명령을 큐에 추가.
        duration 동안 선형보간으로 이동.
        target_pos: (x, y)
        """
        self.anim_queue.append(("__move__", (target_pos, duration)))

    # ---------------------------------------------------------
    # 큐 업데이트
    # ---------------------------------------------------------
    def queue_update(self, dt):
        # 큐가 비어 있음 → Idle 처리 후 종료
        if not self.anim_queue:
            if (
                "Idle" in self.animations
                and self.current_anim != "Idle"
                and self.is_alive
            ):
                idle_anim = self.animations["Idle"]
                idle_anim.reset()

                # 🔥 Idle duration 고정 초기화
                idle_anim.duration = 0.5
                idle_anim.time_per_frame = idle_anim.duration / idle_anim.total_frames

                self.current_anim = "Idle"

            return   # 🔥🔥🔥 여기 반드시 필요!

        # -------------------------
        # 1) 이동 처리
        # -------------------------
        state, data = self.anim_queue[0]

        if state == "__move__":
            target_pos, duration = data

            if not self.moving:
                self.moving = True
                self.move_start = self.position
                self.move_target = target_pos
                self.move_duration = max(duration, 1e-6)
                self.move_elapsed = 0.0

                # Walk 애니로 전환
                if "Walk" in self.animations and self.current_anim != "Walk":
                    walk_anim = self.animations["Walk"]
                    walk_anim.reset()
                    self.current_anim = "Walk"

            # 이동 갱신
            self.move_elapsed += dt
            t = min(self.move_elapsed / self.move_duration, 1.0)

            sx, sy = self.move_start
            tx, ty = self.move_target
            self.position = (
                sx + (tx - sx) * t,
                sy + (ty - sy) * t
            )

            # 이동 완료
            if t >= 1.0:
                self.moving = False
                self.anim_queue.pop(0)

            return   # 이동 → 종료

        # -------------------------
        # 2) 일반 애니메이션 처리
        # -------------------------
        state, duration = self.anim_queue[0]
        anim = self.animations[state]

        # 애니 바뀌는 순간
        if self.current_anim != state:
            anim.reset()
            self.current_anim = state
            self.queue_time = 0.0

        self.queue_time += dt

        # duration이 있으면 그 시간 뒤 다음 큐로
        if duration is not None:
            if self.queue_time >= duration:
                self.anim_queue.pop(0)
        else:
            # duration이 None → Animator 기준으로 끝날 때 pop
            if anim.finished:
                self.anim_queue.pop(0)


    # ---------------------------------------------------------
    # update
    # ---------------------------------------------------------
    def update(self, dt):
        self.queue_update(dt)
        if self.current_anim:
            anim = self.animations.get(self.current_anim)
            if anim:
                anim.update(dt)

        if self.hit_events:
            for ev in self.hit_events[:]:
                ev["time"] -= dt

                if ev["time"] > 0:
                    continue

                target = ev["target"]
                damage = ev["damage"]


                if target is None or not target.is_alive:
                    # 대상이 죽었거나 None인 경우, 공격자(source)를 확인하여
                    # 적절한 반대편 리스트에서 재타겟팅을 시도한다.
                    source = ev.get("source")
                    import Field as _F

                    if source is not None and source in _F.enemies:
                        candidates = _F.allies_alive()
                    else:
                        candidates = _F.enemies_alive()

                    # 후보에서 소스 자신은 제외
                    candidates = [c for c in candidates if c is not source]

                    if candidates:
                        new_target = random.choice(candidates)
                        new_target.take_damage(damage)
                    else:
                        # 교전 상대가 없으면 이 행동(스킬)을 종료하고 Idle로 전환
                        self.hit_events.remove(ev)
                        self.queue_clear()
                        self.queue_push("Idle", None)
                        return

                    self.hit_events.remove(ev)
                    continue

                # ---------- 정상 타격 ----------
                target.take_damage(damage)
                self.hit_events.remove(ev)




    # ---------------------------------------------------------
    # draw
    # ---------------------------------------------------------
    def draw(self, screen):
        frame = self.animations[self.current_anim].frames[self.animations[self.current_anim].current_frame]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        w, h = frame.get_size()
        screen.blit(frame, (self.position[0] - w//2, self.position[1] - h//2))

    # ---------------------------------------------------------
    # 위치 지정
    # ---------------------------------------------------------
    def set_position(self, x, y):
        self.position = (x, y)

    # ---------------------------------------------------------
    # 타격 이벤트 예약
    # ---------------------------------------------------------
    def hit_in(self, delay, target, damage, source=None):
        """
        delay초 뒤에 target.take_damage(damage)를 실행하도록 예약
        """
        self.hit_events.append(
                {
                "time": delay,
                "target": target,
                "damage": damage,
                "source": source,
            }
        )

    def hit_on_frame(self, anim_name, frame_index, target, damage):
        """
        anim_name 애니메이션의 frame_index 프레임에서 타격이 일어나도록 예약.
        SpriteAnimator.time_per_frame * frame_index 를 사용.
        """
        anim = self.animations[anim_name]
        delay = frame_index * anim.time_per_frame
        self.hit_in(delay, target, damage, source=self)

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
            self.anim_queue.clear()
            if "Death" in self.animations:
                self.queue_push("Death", None)
            return

        print(
            f"{self.job}이(가) {damage} 피해를 입었습니다. "
            f"(HP: {self.current_hp}/{self.max_hp})"
        )

        if "Hurt" in self.animations:
            self.queue_push("Hurt")

        if self.current_anim == "Hurt":
            self.animations["Hurt"].reset()




    def heal(self, amount):
        heal_amount = min(amount, self.max_hp - self.current_hp)
        self.current_hp += heal_amount
        print(
            f"{self.job}이(가) {heal_amount} 만큼 회복했습니다! "
            f"(HP: {self.current_hp}/{self.max_hp})"
        )
        if "Heal" in self.animations:
            self.queue_push("Heal", 0.5)

    def can_use_skill(self):
        return Field.skill_point >= self.skill_cost

    # ---------------------------------------------------------
    # 기본 공격(애니 + 데미지 + 이동/복귀까지 포함)
    # ---------------------------------------------------------
    def basic_attack(
        self,
        target,
        anim="Basic",
        hit_frame=5,
        damage=None,
        move_in=True,
        move_back=True,
        is_enemy=False
    ):
        if damage is None:
            damage = self.power

        # 이전 행동 제거
        self.queue_clear()

        ox, oy = self.position  # 원래 위치 저장

        # 1) 이동 (근접 캐릭터용)
        if move_in and target is not None and not is_enemy:
            tx, ty = target.position
            attack_x = tx - 100  # 적 왼쪽 100px 지점
            attack_y = ty
            self.move_to((attack_x, attack_y), duration=0.25)
        elif move_in and target is not None and is_enemy:
            tx, ty = target.position
            attack_x = tx + 100  # 아군 오른쪽 100px 지점
            attack_y = ty
            self.move_to((attack_x, attack_y), duration=0.25)

        # 2) 공격 애니메이션
        self.queue_push(anim, None)

        # 3) 타격 타이밍 예약
        if target is not None:
            self.hit_on_frame(anim, hit_frame, target, damage)

        # 4) 복귀
        if move_back:
            self.move_to((ox, oy), duration=0.25)
