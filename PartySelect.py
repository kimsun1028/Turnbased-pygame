import pygame
import Field
from knight import Knight
from Archer import Archer
from Priest import Priest
from Wizard import Wizard

class PartySelect:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 24)

        self.jobs = [
            ("나이트", Knight),
            ("아처", Archer),
            ("위자드", Wizard),
            ("프리스트", Priest)
        ]

        self.selected = []
        self.preview_chars = []
        self.state = "SELECT"     # SELECT / DETAIL
        self.current_pick = None  # DETAIL에서 표시할 캐릭터
        self.bg = pygame.image.load("image/Party_select.jpg").convert()
        self.bg = pygame.transform.scale(self.bg, (1280,720))

        self.error_message = ""
        self.error_timer = 0

    def register_anims(self, character):
        character.add_anim("Idle",   fps=8,  loop=True)
        character.add_anim("Walk",   fps=8, loop=True)
        character.add_anim("Basic",  fps=8, loop=False)
        character.add_anim("Hurt",   fps=8, loop=False)
        character.add_anim("Death",  fps=8, loop=False)
        if character.job == "아처":
            character.add_anim("Skill", loop=False, duration = 1.5)
        else:
            character.add_anim("Skill", fps=12, loop = False)
        try:
            character.add_anim("TauntBasic", fps=12, loop=False)
        except:
            pass

    def run(self):
        running = True
        clock = pygame.time.Clock()

        # 미리보기 캐릭터 생성
        if not self.preview_chars:
            base_y = 350
            gap = 70
            for i, (job_name, cls) in enumerate(self.jobs):
                c = cls()
                self.register_anims(c)
                c.set_position(300, base_y + i * gap)
                c.current_anim = "Idle"
                self.preview_chars.append(c)

        while running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    # ============================================
                    # DETAIL 상태 (상세 설명 화면)
                    # ============================================
                    if self.state == "DETAIL":
                        if event.key == pygame.K_RETURN:
                            # 선택 확정!
                            # 중복 체크
                            if any(isinstance(c, self.current_pick) for c in self.selected):
                                self.error_message = "이미 해당 직업이 파티에 있습니다!"
                                self.error_timer = pygame.time.get_ticks() + 1000
                                continue
                            new_char = self.current_pick()

                            # 애니 등록 후 파티에 추가
                            self.register_anims(new_char)
                            self.selected.append(new_char)

                            self.state = "SELECT"
                            self.current_pick = None

                            # 프리뷰 캐릭터 걷기 연출
                            for p in self.preview_chars:
                                if isinstance(p, type(new_char)):
                                    x, y = p.position
                                    p.queue_clear()
                                    p.move_to((1600, y), duration=1.5)
                                    p.queue_push("Walk", None)

                            if len(self.selected) >= Field.party_len:
                                end_time = pygame.time.get_ticks() + 2000 
                                while pygame.time.get_ticks() < end_time: 
                                    dt = clock.tick(60) / 1000.0 
                                    for c in self.preview_chars: 
                                        c.update(dt) 
                                    self.screen.blit(self.bg,(0,0)) 
                                    self.draw_text("파티가 완성되었습니다!",30,30) 
                                    for i, char in enumerate(self.selected): 
                                        self.draw_text(f"{i+1}. {char.job}", 500 + i*150, 30) 
                                    for c in self.preview_chars:
                                        c.draw(self.screen) 
                                    pygame.display.flip()
                                Field.allies = self.selected
                                return

                        elif event.key == pygame.K_ESCAPE:
                            # 상세 화면 종료 → SELECT로 복귀
                            self.state = "SELECT"
                            self.current_pick = None

                        continue

                    # ============================================
                    # SELECT 상태 (기본 선택 화면)
                    # ============================================
                    if self.state == "SELECT":
                        if event.key == pygame.K_1:
                            self.current_pick = Knight
                            self.state = "DETAIL"

                        elif event.key == pygame.K_2:
                            self.current_pick = Archer
                            self.state = "DETAIL"

                        elif event.key == pygame.K_3:
                            self.current_pick = Wizard
                            self.state = "DETAIL"

                        elif event.key == pygame.K_4:
                            self.current_pick = Priest
                            self.state = "DETAIL"

                        else:
                            self.error_message = "옳지 않은 입력입니다! (1~4 선택)"
                            self.error_timer = pygame.time.get_ticks() + 1000


            # ============================================
            # 애니메이션 업데이트
            # ============================================
            for c in self.preview_chars:
                c.update(dt)

            # ============================================
            # 렌더링
            # ============================================
            self.screen.blit(self.bg, (0, 0))

            if self.state == "SELECT":
                self.draw_text("파티를 선택하세요!", 30, 30)
                self.draw_text("1. 나이트", 30, 550)
                self.draw_text("2. 아처", 30, 580)
                self.draw_text("3. 위자드", 30, 610)
                self.draw_text("4. 프리스트", 30,640)

                # 선택된 캐릭터 표시
                for i, char in enumerate(self.selected):
                    self.draw_text(f"{i+1}. {char.job}", 500 + i*150, 30)

                for c in self.preview_chars:
                    c.draw(self.screen)

            elif self.state == "DETAIL":
                # 상세 설명 레이아웃
                long_desc = self.get_long_desc(self.current_pick)
                if self.current_pick != Archer:
                    self.draw_text("기본 공격 : 스킬포인트 획득",30,60)
                base_x = 30
                base_y = 550
                y = base_y
                for line in long_desc:
                    self.draw_text(line, base_x, y)
                    y += 28
                self.draw_text("[ENTER] 선택  |  [ESC] 뒤로가기",30,30)
                
                for c in self.preview_chars:
                    c.draw(self.screen)
            # ============================
            # 오류 메시지 출력
            # ============================
            if self.error_message and pygame.time.get_ticks() < self.error_timer:
                err = self.font.render(self.error_message, True, (255, 80, 80))
                self.screen.blit(err, (30, 510))
            elif pygame.time.get_ticks() >= self.error_timer:
                self.error_message = ""

            pygame.display.flip()

    # ===============================
    # 캐릭터 상세 설명
    # ===============================
    def get_long_desc(self, cls):
        if cls == Knight:
            return [
                "1. 나이트",
                "기본 공격:          지정한 적에게 공격해 피해를 입힙니다.",
                "기본 공격(강화):  지정한 적에게 공격해 잃은 체력의 20%만큼 피해를 추가로 입힙니다.",
                "스킬:                 3턴 동안 적을 도발하여 최대 체력을 50 증가시키고 적의 공격을 유도합니다. ",
                "도발 중 기본공격이 강화되고 받는 피해가 감소합니다."
            ]

        elif cls == Archer:
            return [
                "2. 아처",
                "기본 공격:   지정한 두 명의 적에게 연속 사격으로 POWER 100% 만큼의 피해를 입힙니다.",
                "스킬:          무작위 적에게 POWER 50%의 화살을 10발 난사하여 피해를 입힙니다.",
                "기본 공격이 스킬포인트를 회복하지 않습니다."
            ]
        elif cls == Wizard:
            return [
                "3. 위자드",
                "기본 공격:   지정한 적에게 파이어볼로 POWER 100% 만큼의 피해를 입힙니다.",
                "스킬:          얼음 결정을 소환하여 모든 적에게 POWER 75%의 피해를 입힙니다.",
                "3번째 스킬마다 더욱 강력한 얼음결정을 소환하여 두배의 피해를 입힙니다."
            ]

        elif cls == Priest:
            return [
                "4. 프리스트",
                "기본 공격:   지정한 적에게 POWER 100%의 피해를 입힙니다.",
                "스킬:          지정한 아군에게 POWER 200%만큼 회복시킵니다.",
                "또 가장 잃은 체력이 많은 아군에게 POWER 100%만큼 회복시킵니다."
            ]

        return ["(설명 없음)"]

    def draw_text(self, message, x, y):
        text_surface = self.font.render(message, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))
