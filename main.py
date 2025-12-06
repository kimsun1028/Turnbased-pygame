import pygame
from PartySelect import PartySelect
import Field
from Slime import Slime
from Orc_rider import Orc_rider
from Orc import Orc
import Dungeon  # ← Dungeon.py 임포트


def setup_first_floor():
    """
    1층에서 등장할 적들을 Field.enemies 리스트에 세팅합니다.
    """
    Field.enemies = [
        Slime("슬라임"),
        Slime("슬라임"),
        Slime("슬라임")
    ]


def setup_second_floor():
    """
    2층에서 등장할 적들을 Field.enemies 리스트에 세팅합니다.
    보스(Orc_rider)는 isBoss=True 로 설정합니다.
    """
    Field.enemies = [
        Orc("오크"),
        Orc_rider("오크라이터(Boss)", isBoss=True),
        Orc("오크")
    ]


def walk_to_next_floor(screen, bg_image):
    """
    1층과 2층 사이 전환 연출(아군 걷기 장면)을 재생합니다.
    아군 캐릭터를 오른쪽으로 이동시키며 Walk 애니메이션을 재생합니다.
    """
    clock = pygame.time.Clock()

    # 아군 걷기 모션
    for ally in Field.allies:
        if not ally.is_alive:
            continue
        ally.anim_queue.clear()
        ally.hit_events.clear()
        ally.current_anim = "Walk"

    finished = False

    while not finished:
        dt = clock.tick(60) / 1000.0
        finished = True

        # ---------------------------
        # 캐릭터 이동
        # ---------------------------
        for ally in Field.allies:
            if not ally.is_alive:
                continue
            x, y = ally.position
            ally.set_position(x + 400 * dt, y)
            ally.update(dt)

            if ally.position[0] < 2000:
                finished = False

        # ---------------------------
        # 화면 그리기
        # ---------------------------
        screen.blit(bg_image, (0, 0))  # 배경 유지

        # 죽은 포함 모든 적 그리기
        for e in Field.enemies:
            e.update(dt)
            e.draw(screen)

        # 아군 그리기 (걷는 중)
        for a in Field.allies:
            a.draw(screen)

        pygame.display.flip()


def main():
    """
    게임의 전체 흐름을 담당하는 메인 루프입니다.
    파티 선택 -> 1층 전투 -> 이동 연출 -> 2층 전투 순서로 진행합니다.
    """
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Turn-Based PYGAME")

    while True:
        setup_first_floor()

        # 파티 선택
        party_scene = PartySelect(screen)
        party_scene.run()

        # -------- 1층 전투 --------
        while True:
            result = Dungeon.floor(screen, "image/First_floor.jpg")

            if result == "RETRY":
                continue
            elif result == "RESELECT":
                break
            elif result == "QUIT":
                pygame.quit()
                return
            elif result == "NEXT":
                break   # 1층을 깼으니 2층으로 이동

        bg_image = pygame.image.load("image/First_floor.jpg").convert()
        bg_image = pygame.transform.scale(bg_image, (1280, 720))

        walk_to_next_floor(screen, bg_image)

        # -------- 2층 전투 --------
        if result == "NEXT":
            setup_second_floor()

            while True:

                # 클리어 후 남은 애니메이션 흔적 제거
                for ch in Field.allies + Field.enemies:
                    ch.anim_queue.clear()
                    ch.hit_events.clear()
                    ch.current_anim = "Idle"

                result2 = Dungeon.floor(
                    screen,
                    "image/Second_floor.jpg",
                    start_pos=(350, 250),
                    last_floor=True   #마지막 층 표시 
                )

                if result2 == "RETRY":
                    continue
                elif result2 == "RESELECT":
                    break
                elif result2 == "QUIT":
                    pygame.quit()
                    return

                # 마지막 층에서는 NEXT가 나오지 않음.


if __name__ == "__main__":
    main()
