import pygame
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
    
    Dungeon.first_floor(screen)
    


if __name__ == "__main__":
    main()
