import pygame
from PartySelect import PartySelect
import Field
from Slime import Slime
from Orc_rider import Orc_rider
from Orc import Orc
import Dungeon  # ← Dungeon.py 임포트

def setup_first_floor():
    Field.enemies = [
        Orc("보스"),
        Orc_rider("보스"),
        Orc("보스"),
    ]

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Turn-Based PYGAME")

    setup_first_floor()

    # 파티 선택
    party_scene = PartySelect(screen)
    party_scene.run()

    # 🔥 이제 애니메이션 테스트 대신 실제 던전 전투 실행
    Dungeon.first_floor(screen)

    pygame.quit()

if __name__ == "__main__":
    main()
