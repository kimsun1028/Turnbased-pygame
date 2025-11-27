import pygame
from pygame import Rect
class SpriteAnimator:
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

        # duration 기반 재생
        self.duration = duration       # 애니 전체 길이
        self.time_per_frame = self.duration / self.total_frames

        self.current_frame = 0
        self.accum_time = 0.0
        self.finished = False

    # frames에 프레임 넣는 메서드
    def _load_frames(self):
        for i in range(self.frame_num):
            frame = self.sheet.subsurface(      # 스프라이트 시트에서 프레임 잘라내기
                Rect(i * self.FRAME_SIZE, 0, self.FRAME_SIZE, self.FRAME_SIZE)
            )
            frame = pygame.transform.scale(     # 프레임의 스케일 변환하기
                frame,
                (int(self.FRAME_SIZE * self.scale), int(self.FRAME_SIZE * self.scale))
            )
            self.frames.append(frame)           # frames 리스트에 저장하기
    
    # 재생 초기화 메서드
    def reset(self):
        self.current_frame = 0
        self.accum_time = 0.0
        self.finished = False

    def update(self, dt):
        if self.finished and not self.loop:
            return

        self.accum_time += dt

        # 프레임 계산 (duration 기반)
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

    # 위치에 현 프레임 출력
    def draw(self, screen, pos):
        frame = self.frames[self.current_frame]
        screen.blit(frame, pos)
