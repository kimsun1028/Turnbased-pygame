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
# StaticEffect (힐 효과, 폭발, 빛나는 스파크 등)
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
# Manager
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
