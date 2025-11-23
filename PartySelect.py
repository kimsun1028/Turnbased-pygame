import pygame
import Field
from Knight import Knight
from Archer import Archer
from Priest import Priest

class PartySelect:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 48)

        self.jobs = [
            ("나이트", Knight),
            ("아처", Archer),
            ("프리스트", Priest)   
        ]

        self.selected = []

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.selected.append(Knight())
                    elif event.key == pygame.K_2:
                        self.selected.append(Archer())
                    elif event.key == pygame.K_3:
                        self.selected.append(Priest())

                    # 파티 인원 채워졌으면 종료
                    if len(self.selected) == Field.party_len:
                        Field.allies = self.selected
                        return

            # -------------------------
            #       ★ 화면 렌더링 ★
            # -------------------------
            self.screen.fill((30,30,30))
            self.draw_text(f"파티를 선택하세요! ({Field.party_len}명 선택)", 50, 50)

            self.draw_text("1. 나이트", 100, 200)
            self.draw_text("2. 아처", 100, 300)
            self.draw_text("3. 프리스트", 100, 400)
            
            # 선택된 캐릭터 표시
            for i, char in enumerate(self.selected):
                self.draw_text(f"{i+1}. {char.job}", 800, 200 + i * 100)

            pygame.display.flip()   # ★ 화면 업데이트
    
    def draw_text(self, message, x, y):
        text_surface = self.font.render(message, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))