# =====================================
# Base Class (모든 이펙트의 공통 부모)
# =====================================
class EffectBase:
    """
    모든 이펙트 객체의 공통 부모 클래스입니다.
    위치(pos)와 생존 여부(alive)를 기본으로 가집니다.
    """
    def __init__(self, pos):
        """
        pos : 화면에 출력할 위치(x, y)
        """
        self.pos = list(pos)
        self.alive = True

    def update(self, dt):
        """
        dt에 따른 상태 갱신. 자식 클래스에서 구현
        """
        pass

    def draw(self, screen):
        """
        화면에 이펙트를 출력. 자식 클래스에서 구현
        """
        pass


# =====================================
# StaticEffect (힐 효과, 폭발, 빛나는 스파크 등)
# =====================================
class StaticEffect(EffectBase):
    """
    위치에 고정된 애니메이션 이펙트(힐, 폭발 등)를 표현하는 클래스입니다.
    """
    def __init__(self, animator, pos, duration=0.6):
        super().__init__(pos)
        self.anim = animator
        self.timer = 0
        self.duration = duration

    def update(self, dt):
        """
        dt만큼 시간을 진행시키며 애니메이션과 지속시간을 갱신합니다.
        duration을 초과하면 alive=False가 됩니다.
        """
        if not self.alive:
            return
        
        self.timer += dt
        self.anim.update(dt)

        if self.timer >= self.duration:
            self.alive = False

    def draw(self, screen):
        """
        현재 프레임을 화면에 출력합니다.
        """
        self.anim.draw(screen, self.pos)


# =====================================
# Manager
# =====================================
class EffectManager:
    """
    모든 이펙트를 일괄 관리하는 매니저 클래스입니다.
    update/draw로 전체 이펙트를 처리합니다.
    """
    def __init__(self):
        """
        effects : 현재 활성화된 이펙트 리스트
        """
        self.effects = []

    def add(self, effect):
        """
        새로운 이펙트를 리스트에 추가.
        """
        self.effects.append(effect)

    def update(self, dt):
        """
        모든 이펙트의 update를 호출하고,
        alive=False인 이펙트는 제거
        """
        for e in self.effects[:]:
            e.update(dt)
            if not e.alive:
                self.effects.remove(e)

    def draw(self, screen):
        """
        모든 이펙트의 draw를 호출합니다.
        """
        for e in self.effects:
            e.draw(screen)
