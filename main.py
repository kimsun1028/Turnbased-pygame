# Main.py
import time

import Field
from Knight import Knight
from Archer import Archer
from Priest import Priest
from Slime import Slime
import Dungeon


def select_party():
    print("직업 목록:\n1. 나이트 | 2. 아처 | 3. 프리스트")

    jobs = [Knight, Archer, Priest]
    chosen = []

    # 아군 3명 선택
    while len(chosen) < 3:
        print(f"{len(chosen)+1}번째 캐릭터 선택:")
        try:
            idx = int(input().strip()) - 1
            if 0 <= idx < 3:
                chosen.append(jobs[idx]())
                print(f"{chosen[-1].job} 배치 완료.")
            else:
                print("잘못된 번호입니다.")
        except ValueError:
            print("숫자를 입력하세요.")

    # Field에 배치
    Field.allies = chosen[:]


def setup_first_floor():
    Field.enemies = [
        Slime("슬라임1"),
        Slime("슬라임2"),
        Slime("슬라임3"),
    ]


def main():
    print("===== 파이썬 콘솔 턴제 RPG =====")
    select_party()
    setup_first_floor()

    print("던전 1층에 입장합니다...")
    time.sleep(1)

    Dungeon.first_floor()


if __name__ == "__main__":
    main()
