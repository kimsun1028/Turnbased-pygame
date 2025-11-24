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
    Animation.anim_play("Armored Axeman-Attack03.png", screen, (0,0), loop_count=1)

    # 지속 애니메이션 생성
    idle_anim = Animation.SpriteAnimator("Armored Axeman-Idle.png", scale=2.0, fps=12)

    # 지속 루프 (메인 루프)
    running = True
    clock = pygame.time.Clock()

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        idle_anim.update()

        screen.fill((20,20,20))
        idle_anim.draw(screen, (0,0))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    


if __name__ == "__main__":
    main()
