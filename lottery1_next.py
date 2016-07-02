# -*- coding: UTF-8 -*-
from lottery1 import Lottery1
from lottery1 import LotteryData1
from lottery1 import LotteryMethod1


class LotteryDataNext(LotteryData1):
    default_value = [5, 10, 200, 3000, 194987, 8650159]


def load_txt(path):
    with open(path, "r") as file:
        text = file.read()
        file.close()
    return text


def get_comb():
    import re

    def to_int(nums):
        return [int(i) for i in nums]

    path = "min_times_all.txt"

    p_num = re.compile(r'\d+-\d+-\d+-\d+-\d+-\d+:\d+')
    num_list = p_num.finditer(load_txt(path))
    for item in num_list:
        red_blue = item.group().split(":")
        yield to_int(red_blue[0].split("-")), to_int(red_blue[1])


lottery = Lottery1([9, 13, 18, 20, 27, 31], [4])
out_ = 0
in_ = 0
for i, item in enumerate(get_comb()):
    out_ += 2
    lottery_data = LotteryDataNext(item[0], item[1])
    lottery_data.method = LotteryMethod1()
    lottery_data.cal([lottery])
    in_ += lottery_data.value
    print(i + 1, lottery_data.get_name_str(), lottery_data.times, lottery_data.value)
print("out: %d, in: %d" % (out_, in_))
