import Field
from Enemy import Enemy


class Orc_rider(Enemy):
    """
    전형적인 RPG내 보스 캐릭터입니다.
    보스는 적 스킬 턴에 무조건 보스가 스킬을 사용합니다.
    """
    def __init__(self, name="오크라이더", isBoss = False):
        super().__init__(name=name, hp=300, power=40)
        self.job = "오크라이더"
        self.job_eng = "Orc_rider"
        self.isBoss = isBoss

        self.set_position(0, 0)

        # 애니메이션 등록
        self.add_anim("Idle",   scale=3, fps=8,  loop=True)
        self.add_anim("Walk",   scale=3, fps=10, loop=True)
        self.add_anim("Basic",  scale=3, fps=10, loop=False)
        self.add_anim("Skill",  scale=3, fps=10, loop=False)
        self.add_anim("Hurt",   scale=3, fps=12, loop=False)
        self.add_anim("Death",  scale=3, fps=12, loop=False)

    def basic_attack(self):
        """
        기본 기본공격 메서드
        """
        target = self.select_target()
        if target is None:
            return

        super().basic_attack(
            target=target,
            anim="Skill",
            hit_frame=5,
            damage=self.power,
            move_in=True,
            move_back=True,
            is_enemy=True
        )

    def skill(self):
        """
        오크라이더 스킬: 모든 아군에게 피해입히기
        도발 중이면 메인타겟 : 나이트, 아닐시 중앙 아군
        """
        
        anim = "Basic"
        hit_frame = 8
        dmg = self.power
        allies = Field.allies_alive()
        if not allies:
            return
        self.queue_clear()
        ox, oy = self.position

        if Field.is_taunt():
            maintarget = self.select_target()
        else:
            alive_sorted = sorted(allies, key=lambda c: c.fixed_index)
            mid = len(alive_sorted) // 2
            maintarget = alive_sorted[mid]

        tx, ty = maintarget.position
        tx = tx + 100
        self.move_to((tx,ty), duration = 0.5)

        alive_sorted = sorted(Field.allies_alive(), key=lambda c: c.fixed_index)
        idx = alive_sorted.index(maintarget)

        targets = [maintarget]
        if idx - 1 >= 0:
            targets.append(alive_sorted[idx-1])
        if idx + 1 < len(alive_sorted):
            targets.append(alive_sorted[idx+1])
        if maintarget is None:
            return

        self.queue_push(anim, None)
        for target in targets:
            if target and target.is_alive:
                self.hit_on_frame(anim, hit_frame, target, dmg)
        self.move_to((ox,oy), duration=0.5)


            
