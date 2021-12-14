from p01 import p01
from p02 import p02
from p03 import p03
from p04 import p04
from p05 import p05
from p06 import p06
from p07 import p07
from p08 import p08
from p09 import p09
from p10 import p10
from p11 import p11
from p12 import p12

day_script_dict = {
    # 1: p01(),
    # 2: p02(),
    # 3: p03(),
    # 4: p04(),
    # 5: p05(),
    # 6: p06(),
    # 7: p07(),
    # 8: p08(),
    # 9: p09(),
    # 10: p10(),
    # 11: p11(),
    12: p12(),
}

if __name__ == '__main__':
    start, end = 12, 12
    for day in range(start, end+1):
        if day not in day_script_dict:
            raise KeyError("Day must be imported and added to day_script_dict before calling.")
        print(f"Day {day}: {day_script_dict[day]}")
