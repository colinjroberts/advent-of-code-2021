from p01 import p01
from p02 import p02
from p03 import p03
from p04 import p04
from p05 import p05

day_script_dict = {
    1: p01(),
    2: p02(),
    3: p03(),
    4: p04(),
    5: p05(),
}
#
if __name__ == '__main__':
    for day in range(5, 6):
        if day not in day_script_dict:
            raise KeyError("Day must be imported and added to day_script_dict before calling.")
        print(f"Day {day}: {day_script_dict[day]}")

