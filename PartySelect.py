import pygame
import Field
from knight import Knight
from Archer import Archer
from Priest import Priest

class PartySelect:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 24)

        self.jobs = [
            ("나이트", Knight),
            ("아처", Archer),
            ("프리스트", Priest)
        ]

        self.selected = []
        self.preview_chars = []
        self.bg = pygame.image.load("image/Party_select (2).jpg").convert()
        self.bg = pygame.transform.scale(self.bg, (1280,720))

    def register_anims(self, character):
        """캐릭터 생성 직후 애니메이션 자동 등록"""

        character.add_anim("Idle",   fps=8,  loop=True)
        character.add_anim("Walk",   fps=10, loop=True)
        if character.job == "아처":
            character.add_anim("Basic",  fps=10, loop=False, duration = 0.7)
        else: 
            character.add_anim("Basic",  fps=10, loop=False)
        character.add_anim("Hurt",   fps=12, loop=False)
        character.add_anim("Death",  fps=12, loop=False)

        # 스킬 파일이 존재하면 자동 등록
        try:
            if character.job == "아처":
                character.add_anim("Skill", scale=2, fps=12, loop=False, duration = 2.0)
            else:
                character.add_anim("Skill",  fps=12, loop=False)
        except:
            pass  # 스킬 파일 없으면 무시

        try:
            character.add_anim("TauntBasic", fps = 12, loop=False)
        except:
            pass

        try:
            character.add_anim("Heal_Effect", scale = 3, fps = 12, loop=False)
        except:
            pass

    def run(self):
        running = True
        clock = pygame.time.Clock()

        if not self.preview_chars:
            base_y = 350
            gap = 80

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
                    new_char = None

                    if event.key == pygame.K_1:
                        new_char = Knight()

                    elif event.key == pygame.K_2:
                        new_char = Archer()

                    elif event.key == pygame.K_3:
                        new_char = Priest()
                    # 4번째 직업 만들면 추가!!

                    # 중복 체크
                    if new_char:
                        if any(type(c) is type(new_char) for c in self.selected):
                            print("이미 해당 직업이 파티에 있습니다!")
                        else:
                            for p in self.preview_chars:
                                if isinstance(p, type(new_char)):
                                    p.queue_clear()
                                    x,y = p.position
                                    p.move_to((1600,y), duration = 2.0)
                                    p.queue_push("Walk",None)
                                    break
                            # 🔥 여기서 애니메이션 등록!
                            self.register_anims(new_char)
                            self.selected.append(new_char)

                    # 파티 인원 채워졌으면 종료
                    if len(self.selected) == Field.party_len:
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

            for c in self.preview_chars:
                c.update(dt)
            # -------------------------
            #       화면 렌더링
            # -------------------------
            self.screen.blit(self.bg,(0,0))
            self.draw_text(f"파티를 선택하세요! ({Field.party_len}명 선택)", 30, 30)

            self.draw_text("1. 나이트   - 튼튼한 전사 (도발 가능)", 30, 600)
            self.draw_text("2. 아처     - 원거리 연속 공격" , 30, 630)
            self.draw_text("3. 프리스트  - 회복 및 지원 담당", 30, 660)

            for c in self.preview_chars:
                c.draw(self.screen)

            # 현재 선택된 캐릭터 목록 표시
            for i, char in enumerate(self.selected):
                self.draw_text(f"{i+1}. {char.job}", 500+ i*150, 30)

            pygame.display.flip()

    def draw_text(self, message, x, y):
        text_surface = self.font.render(message, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))
