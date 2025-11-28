# Effects.py
import pygame

# =====================================
# Base Class (모든 이펙트의 공통 부모)
# =====================================
class EffectBase:
    def __init__(self, pos):
        self.pos = list(pos)
        self.alive = True

    def update(self, dt):
        pass

    def draw(self, screen):
        pass


# =====================================
# 1) StaticEffect (힐 효과, 폭발, 빛나는 스파크 등)
# =====================================
class StaticEffect(EffectBase):
    def __init__(self, animator, pos, duration=0.6):
        super().__init__(pos)
        self.anim = animator
        self.timer = 0
        self.duration = duration

    def update(self, dt):
        if not self.alive:
            return
        
        self.timer += dt
        self.anim.update(dt)

        if self.timer >= self.duration:
            self.alive = False

    def draw(self, screen):
        self.anim.draw(screen, self.pos)


# =====================================
# 2) ProjectileEffect (화살, 힐구체, 마법탄)
# =====================================
class ProjectileEffect(EffectBase):
    def __init__(self, image_path, start_pos, target, speed=400, on_hit=None):
        super().__init__(start_pos)

        self.image = pygame.image.load(image_path).convert_alpha()
        self.target = target
        self.speed = speed
        self.on_hit = on_hit  # 충돌 시 실행할 함수

    def update(self, dt):
        if not self.target.is_alive:
            self.alive = False
            return

        t_frame = self.target.animations[self.target.current_anim].frames[0]
        tw, th = t_frame.get_size()
        tx = self.target.position[0] + tw//2
        ty = self.target.position[1] + th//2

        x, y = self.pos

        dx = tx - x
        dy = ty - y
        dist = (dx*dx + dy*dy) ** 0.5

        if dist < 10:
            # 타격 발생
            if self.on_hit:
                self.on_hit(self.target)
            self.alive = False
            return

        nx = dx / dist
        ny = dy / dist

        self.pos[0] += nx * self.speed * dt
        self.pos[1] += ny * self.speed * dt

    def draw(self, screen):
        screen.blit(self.image, self.pos)


# =====================================
# 3) Manager
# =====================================
class EffectManager:
    def __init__(self):
        self.effects = []

    def add(self, effect):
        self.effects.append(effect)

    def update(self, dt):
        for e in self.effects[:]:
            e.update(dt)
            if not e.alive:
                self.effects.remove(e)

    def draw(self, screen):
        for e in self.effects:
            e.draw(screen)
