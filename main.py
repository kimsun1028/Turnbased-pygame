import pygame
import Animation
from PartySelect import PartySelect
import Dungeon
import Field
from Slime import Slime



def setup_first_floor():
    Field.enemies = [
        Slime("슬라임1"),
        Slime("슬라임2"),
        Slime("슬라임3"),
    ]


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Turn-Based PYGAME")

    party_scene = PartySelect(screen)
    party_scene.run()

    # 지속 루프 (메인 루프)
    running = True
    clock = pygame.time.Clock()

    setup_first_floor()
    Dungeon.first_floor(screen)

    pygame.quit()
    


if __name__ == "__main__":
    main()
