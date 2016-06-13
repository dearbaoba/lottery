# -*- coding: UTF-8 -*-
from lottery_process import *


class LotteryMethod2(LotteryMethod):
    METHODS = [
        [(3, 0), (1, 2), (2, 1), (0, 2)],
        [(4, 0), (3, 1), (2, 2)],
        [(4, 1), (3, 2)],
        [(5, 0), (4, 2)],
        [(5, 1)],
        [(5, 2)]
    ]


class Lottery2(Lottery):
    RED_TOTAL = 35
    BLUE_TOTAL = 12
    RED_NUM = 5
    BLUE_NUM = 2


class LotteryData2(LotteryData):
    default_value = [14, 156, 2915, 99193, 1071285, 21425712]


class FetchHTML2(FetchHTML):
    URL = "http://www.lottery.gov.cn/lottery/dlt/History.aspx?p=%d"
    TARGET = "data2/page%d.html"
    PAGES = 30


class LotteryLoader2(LotteryLoader):
    TARGET = "data2/page%d.html"
    PAGES = 30
    RED_NUM = 5
    BLUE_NUM = 2

    def parse_page(self, text):
        import re
        p_reds = re.compile(
            r'<FONT class=\'FontRed\'>.*</FONT> +')
        p_blues = re.compile(
            r'<FONT class=\'FontBlue\'>.*</FONT>')
        p_date = re.compile(r'\d{4}-\d{2}-\d{2}')
        p_num = re.compile(r'\d{2}')
        reds = p_reds.finditer(text)
        blues = p_blues.finditer(text)
        dates = p_date.finditer(text)
        groups = zip(list(reds), list(blues), list(dates))
        item_list = []
        for (red, blue, date) in groups:
            red_list = [int(i.group()) for i in p_num.finditer(red.group())]
            blue_list = [int(i.group()) for i in p_num.finditer(blue.group())]
            item_list.append((red_list, blue_list, date.group()))
        return item_list


class LotteryProcess2(LotteryProcess):
    LotteryClass = Lottery2
    LotteryDataClass = LotteryData2
    LotteryMethodClass = LotteryMethod2
    LotteryFetchClass = FetchHTML2
    LotteryLoadClass = LotteryLoader2


if __name__ == "__main__":
    # FetchHTML2().fetch_html()
    main = LotteryProcess2()
    main.main(1)

    print("main down.")
