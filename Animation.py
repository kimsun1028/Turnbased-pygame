import pygame
from pygame import Rect
class SpriteAnimator:
    def __init__(self, file_path, scale=2.0, fps=12):
        self.sheet = pygame.image.load(file_path).convert_alpha()
        self.sheet_width, self.sheet_height = self.sheet.get_size()

        self.FRAME_SIZE = 100
        self.frame_num = self.sheet_width // self.FRAME_SIZE
        self.scale = scale
        self.fps = fps

        self.frames = []
        self.current = 0
        self.counter = 0

        for i in range(self.frame_num):
            frame = self.sheet.subsurface(
                Rect(i * self.FRAME_SIZE, 0, self.FRAME_SIZE, self.FRAME_SIZE)
            )
            frame = pygame.transform.scale(
                frame,
                (int(self.FRAME_SIZE * scale), int(self.FRAME_SIZE * scale))
            )
            self.frames.append(frame)

    def update(self):
        self.counter += 1
        if self.counter >= (60 // self.fps):
            self.counter = 0
            self.current = (self.current + 1) % self.frame_num

    def draw(self, screen, pos):
        screen.blit(self.frames[self.current], pos)





def anim_play(file_path, screen, pos, scale=2.0, fps=12, loop_count=1):
    """
    file_path  : 스프라이트 시트 경로
    screen     : pygame surface
    pos        : (x, y) 위치
    scale      : 확대 비율
    fps        : 애니메이션 속도
    loop_count : 반복 횟수 (1이면 1번만 재생, 0이면 무한루프)
    """

    sheet = pygame.image.load(file_path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()

    FRAME_SIZE = 100  # 정사각형 프레임

    frame_num = sheet_width // FRAME_SIZE

    frames = []

    # 프레임 추출
    for i in range(frame_num):
        frame = sheet.subsurface(Rect(i * FRAME_SIZE, 0, FRAME_SIZE, FRAME_SIZE))

        frame = pygame.transform.scale(
            frame,
            (int(FRAME_SIZE * scale), int(FRAME_SIZE * scale))
        )
        frames.append(frame)

    current = 0
    counter = 0
    clock = pygame.time.Clock()

    # ★ 반복 횟수 설정
    played_loops = 0

    running = True
    while running:

        # 종료 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 프레임 업데이트
        current += 1

        # 한 사이클 끝
        if current >= frame_num:
            current = 0
            played_loops += 1

            # loop_count 만큼 재생 후 종료
            if loop_count != 0 and played_loops >= loop_count:
                return  # 함수 종료 → 애니메이션 종료

        # 화면 렌더링
        screen.fill((20, 20, 20))
        screen.blit(frames[current], pos)
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()
