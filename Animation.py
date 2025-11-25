import pygame
from pygame import Rect
class SpriteAnimator:
    def __init__(self, file_path, scale=2.0, fps=8, loop=True):
        self.sheet = pygame.image.load(file_path).convert_alpha()       # png 이미지 읽기, 배경처리
        self.sheet_width = self.sheet.get_size()[0]                     # png 이미지 가로 크기 얻기 (세로 = 무조건 100px 고정)

        self.FRAME_SIZE = 100                                   # 프레임 크기 (100 by 100)
        self.frame_num = self.sheet_width // self.FRAME_SIZE    # 프레임 수 (width = 100단위)
        self.scale = scale                                      # 스케일 
        self.fps = fps                                          # 초당 프레임 수
        self.loop = loop                                        # 반복 유무

        # 시간 기반 프레임 변경
        self.time_per_frame = 1.0 / fps     # 1프레임당 걸리는 시간
        self.accum_time = 0.0               # 다음 프레임을 위한 누적 시간 변수. time per frame 변수보다 커지면 다음 프레임 출력

        # 현재 프레임
        self.current_frame = 0              # 현재 프레임 인덱스 저장
        self.finished = False               # loop = false일 때 애니메이션을 멈추기 위한 변수

        # 프레임 준비
        self.frames = []                    # 프레임 이미지 저장 공간
        self._load_frames()

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

    # current_frame 증가시키는 메서드
    def update(self,dt):
        if self.finished:
            return
        self.accum_time += dt
        
        if self.accum_time >= self.time_per_frame:
            self.accum_time -= self.time_per_frame
            self.current_frame += 1

            if self.current_frame >= self.frame_num:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.frame_num - 1
                    self.finished = True

    # 위치에 현 프레임 출력
    def draw(self, screen, pos):
        screen.blit(self.frames[self.current_frame], pos)

