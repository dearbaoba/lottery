# -*- coding: UTF-8 -*-
from lottery_process import *


class LotteryMethod1(LotteryMethod):
    METHODS = [
        [(1, 1), (0, 1), (2, 1)],
        [(4, 0), (3, 1)],
        [(4, 1), (5, 0)],
        [(5, 1)],
        [(6, 0)],
        [(6, 1)]
    ]


class Lottery1(Lottery):
    RED_TOTAL = 33
    BLUE_TOTAL = 16
    RED_NUM = 6
    BLUE_NUM = 1


class LotteryData1(LotteryData):
    default_value = [17, 124, 2255, 109389, 1107568, 17721088]


class FetchHTML1(FetchHTML):
    URL = "http://kaijiang.zhcw.com/zhcw/html/ssq/list_%d.html"
    TARGET = "data/page%d.html"
    PAGES = 101


class LotteryLoader1(LotteryLoader):
    TARGET = "data/page%d.html"
    PAGES = 101
    RED_NUM = 6
    BLUE_NUM = 1

    def parse_page(self, text):
        import re
        p_reds = re.compile(
            r'<em class="rr">.*</em>')
        p_blues = re.compile(
            r'<em>.*</em>')
        p_date = re.compile(r'<td align="center">\d+-\d+-\d+</td>')
        p_num = re.compile(r'\d+')
        p_date_str = re.compile(r'\d+-\d+-\d+')
        reds = p_reds.finditer(text)
        blues = p_blues.finditer(text)
        dates = p_date.finditer(text)
        item_list = []
        for date in dates:
            red_list = [int(p_num.search(reds.next().group()).group())
                        for i in range(self.RED_NUM)]
            blue_list = [int(p_num.search(blues.next().group()).group())
                         for i in range(self.BLUE_NUM)]
            date = p_date_str.search(date.group()).group()
            item_list.append((red_list, blue_list, date))
        return item_list


class LotteryProcess1(LotteryProcess):
    LotteryClass = Lottery1
    LotteryDataClass = LotteryData1
    LotteryMethodClass = LotteryMethod1
    LotteryFetchClass = FetchHTML1
    LotteryLoadClass = LotteryLoader1


if __name__ == "__main__":
    FetchHTML1().fetch_html()
    #main = LotteryProcess1()
    #main.main(1)

    #print("main down.")
