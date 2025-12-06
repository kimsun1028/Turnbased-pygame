import Field
import Animation
import  random
import pygame
class Character:
    """
    캐릭터.py의 캐릭터 클래스는 게임 내 모든 캐릭터(적,아군)의 부모 클래스입니다.
    애니메이션 관련 로직, 게임 내 행동 로직 등이 구현되어 있습니다.
    """
    # 생성자 
    def __init__(self, power=0, max_hp=0, job="", job_eng="", skill_cost=0, skill_name=""):
        # 기본 스탯
        self.power = power
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.skill_cost = skill_cost
        self.job = job
        self.job_eng = job_eng
        self.skill_name = skill_name

        # 오른쪽을 주시하는지
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
    # 생존 여부 속성
    # ---------------------------------------------------------
    @property
    def is_alive(self):
        return self.current_hp > 0

    # ---------------------------------------------------------
    # 애니메이션 추가 메서드
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
    # 큐 조작 메서드들
    # ---------------------------------------------------------
    def queue_push(self, state, duration=None):
        """
        큐에 특정 상태 애니메이션 넣기
        """
        self.anim_queue.append((state, duration))

    def queue_clear(self):
        """
        캐릭터 애니메이션 큐 전부 비우기
        관련 변수도 모두 초기화
        """
        self.anim_queue.clear()
        self.moving = False
        self.move_start = None
        self.move_target = None
        self.move_duration = 0.0
        self.move_elapsed = 0.0
        self.queue_time = 0.0

    # ---------------------------------------------------------
    # 이동 명령 push하는 메서드
    # ---------------------------------------------------------
    def move_to(self, target_pos, duration=0.4):
        """
        이동 명령을 큐에 추가
        duration 동안 선형이동
        target_pos: (x, y) 튜플
        """
        self.anim_queue.append(("__move__", (target_pos, duration)))

    # ---------------------------------------------------------
    # 큐 업데이트 메서드 !!매우중요!!
    # ---------------------------------------------------------
    def queue_update(self, dt):
        """
        게임 함수에서 매 프레임 호출
        현재 캐릭터가 어떤 행동을 히야하는지 결정
        이동 명령도 처리함
        """
        # 큐가 비어 있음 -> Idle 처리 후 종료
        if not self.anim_queue:
            if (
                "Idle" in self.animations
                and self.current_anim != "Idle"
                and self.is_alive
            ):
                idle_anim = self.animations["Idle"]
                idle_anim.reset()

                # Idle duration 고정 초기화
                idle_anim.duration = 0.5
                idle_anim.time_per_frame = idle_anim.duration / idle_anim.total_frames

                self.current_anim = "Idle"

            return  

        state, data = self.anim_queue[0]

        # -------------------------
        # 현 상태가 "__move__" = 이동 명령일 때
        # -------------------------

        if state == "__move__":
            target_pos, duration = data

            if not self.moving:
                self.moving = True
                self.move_start = self.position
                self.move_target = target_pos
                self.move_duration = max(duration, 1e-6)  # duration이 0이되어 0으로 나누는 오류 방지!
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

            return   # 이동 -> 종료

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
            # duration이 None -> Animator 기준으로 끝날 때 pop
            if anim.finished:
                self.anim_queue.pop(0)


    # ---------------------------------------------------------
    # 캐릭터들의 애니메이션을 진행하는 등 매우중요한 함수 !!!!
    # ---------------------------------------------------------
    def update(self, dt):
        """
        캐릭터 애니메이션 진행
        타격 이벤트 처리 담당 함수
        """
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
                    # 아처 스킬 사용시 발동된다. 거의 전용 코드
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
    # 매 프레임당 해당 캐릭터의 애니메이션 재생하는 함수
    # ---------------------------------------------------------
    def draw(self, screen):
        """
        self.current_anim 변수에 들어간 애니메이션을 self.animations 리스트에서 찾아 
        현 프레임에 맞는 프레임을 처리해서 self.position에 출력
        """
        frame = self.animations[self.current_anim].frames[self.animations[self.current_anim].current_frame]
        # facing_right 변수가 False = 왼쪽 보게 뒤집기
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        w, h = frame.get_size()
        screen.blit(frame, (self.position[0] - w//2, self.position[1] - h//2))

    # ---------------------------------------------------------
    # 위치 지정 함수
    # ---------------------------------------------------------
    def set_position(self, x, y):
        """
        위치 지정
        """
        self.position = (x, y)

    # ---------------------------------------------------------
    # 타격 이벤트 예약함수
    # ---------------------------------------------------------
    def hit_in(self, delay, target, damage, source=None):
        """
        delay초 뒤에 특정 target에 take_damage(damage)를 실행하도록 예약
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
        anim_name 애니메이션의 frame_index 프레임에서 특정 target에 타격이 일어나도록 예약
        SpriteAnimator.time_per_frame * frame_index 를 사용
        """
        anim = self.animations[anim_name]
        delay = frame_index * anim.time_per_frame
        self.hit_in(delay, target, damage, source=self)


    # ------------------------------------------------------------------------------------------------------------------
    # 여기서부턴 전투 관련 메서드!!!
    # ------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------
    # 스킬 함수
    # ---------------------------------------------------------
    def skill(self):
        """
        캐릭터들 스킬 오버라이드용
        오버라이드 안되면 에러
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # 데미지를 입는 함수
    # ---------------------------------------------------------
    def take_damage(self, damage):
        """
        damage 수치만큼을 self.current_hp에서 빼는 메서드
        current.hp가 0이하가 되면 사망 애니메이션이 출력된다
        """
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

        # 연속으로 공격을 받을 경우 = 현 애니메이션이 Hurt를 아직 출력중 -> 애니메이션 리셋해 다시 출력
        if self.current_anim == "Hurt":
            self.animations["Hurt"].reset()

    # ---------------------------------------------------------
    # 캐릭터의 체력을 회복하는 함수
    # ---------------------------------------------------------
    def heal(self, amount):
        """
        amount 수치만큼 self.current_hp를 추가시킨다
        max_hp 를 넘어갈 시 최대체력만큼 힐량 조정 
        거의 Priest 전용 함수
        """

        heal_amount = min(amount, self.max_hp - self.current_hp)
        self.current_hp += heal_amount
        print(
            f"{self.job}이(가) {heal_amount} 만큼 회복했습니다! "
            f"(HP: {self.current_hp}/{self.max_hp})"
        )
        if "Heal" in self.animations:
            self.queue_push("Heal", 0.5)
    
    # ---------------------------------------------------------
    # 스킬 사용가능 여부 확인 함수
    # ---------------------------------------------------------
    def can_use_skill(self):
        """
        각 캐릭터당 있는 skill_cost와 게임 내 스킬포인트 비교하는 bool형 함수
        스킬을 사용못하면 False return
        """
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
        """
        캐릭터 기본공격 함수. is_enemy = 적일 경우, move_in, move_back = 근접캐릭일 때 True
        hit_frame = 애니메이션 특정 프레임에서 타격 이벤트 발생
        """
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

### 체감상 구현 난이도 압도적 1위