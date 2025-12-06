import pygame
from pygame import Rect

class SpriteAnimator:
    """
    스프라이트 시트를 프레임 단위로 잘라 애니메이션을 재생하는 클래스입니다.
    파일 경로 형식: animation/클래스명/클래스명-애니명.png
    """

    # ---------------------------------------------------------
    # 생성자: 시트 로드 및 기본 설정
    # ---------------------------------------------------------
    def __init__(self, file_path, scale=2.0, fps=8, loop=True, duration=0.5):
        self.sheet = pygame.image.load(file_path).convert_alpha()
        self.loop = loop

        self.FRAME_SIZE = 100
        self.scale = scale

        sheet_width = self.sheet.get_size()[0]
        self.frame_num = sheet_width // self.FRAME_SIZE

        self.frames = []
        self._load_frames()
        self.total_frames = len(self.frames)

        self.duration = duration
        self.time_per_frame = self.duration / self.total_frames

        self.current_frame = 0
        self.accum_time = 0.0
        self.finished = False

    # ---------------------------------------------------------
    # 스프라이트 시트 → 프레임 리스트로 분리
    # ---------------------------------------------------------
    def _load_frames(self):
        """
        시트를 프레임 단위로 잘라 self.frames에 저장.
        """
        for i in range(self.frame_num):
            frame = self.sheet.subsurface(
                Rect(i * self.FRAME_SIZE, 0, self.FRAME_SIZE, self.FRAME_SIZE)
            )
            frame = pygame.transform.scale(
                frame,
                (int(self.FRAME_SIZE * self.scale), int(self.FRAME_SIZE * self.scale))
            )
            self.frames.append(frame)

    # ---------------------------------------------------------
    # 애니메이션 재생 상태 초기화
    # ---------------------------------------------------------
    def reset(self):
        """
        애니메이션 상태를 처음으로 되돌리기
        """
        self.current_frame = 0
        self.accum_time = 0.0
        self.finished = False

    # ---------------------------------------------------------
    # 프레임 진행 (dt 기반)
    # ---------------------------------------------------------
    def update(self, dt):
        """
        dt에 따라 current_frame을 증가시키기
        loop=False면 마지막 프레임에서 멈춤
        """
        if self.finished and not self.loop:
            return

        self.accum_time += dt

        while self.accum_time >= self.time_per_frame:
            self.accum_time -= self.time_per_frame
            self.current_frame += 1

            if self.current_frame >= self.total_frames:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.total_frames - 1
                    self.finished = True
                    break

    # ---------------------------------------------------------
    # 현재 프레임 화면에 출력
    # ---------------------------------------------------------
    def draw(self, screen, pos):
        """
        현재 프레임을 화면(screen)에 pos 위치에 출력
        """
        frame = self.frames[self.current_frame]
        screen.blit(frame, pos)
