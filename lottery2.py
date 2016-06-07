# -*- coding: UTF-8 -*-

RED_NUM = 5
RED_TOTAL = 35
RED_LIST = [i + 1 for i in range(RED_TOTAL)]
BLUE_NUM = 2
BLUE_TOTAL = 12
BLUE_LIST = [i + 1 for i in range(BLUE_TOTAL)]
METHOD_NUM = 6
METHODS = [
    [(3, 0), (1, 2), (2, 1), (0, 2)],
    [(4, 0), (3, 1), (2, 2)],
    [(4, 1), (3, 2)],
    [(5, 0), (4, 2)],
    [(5, 1)],
    [(5, 2)]
]
PAGES = 30


class LotteryCalculate(object):

    @staticmethod
    def __method(red, blue, lottery_data, lottery):
        reds = lottery_data.reds & lottery.reds
        blues = lottery_data.blues & lottery.blues
        return len(reds) is red and len(blues) is blue

    @staticmethod
    def method_generate(lottery_data, lottery):
        for i, method in enumerate(METHODS):
            for item in method:
                if LotteryCalculate.__method(item[0], item[1], lottery_data, lottery):
                    return True, i
        return False, 0


class Lottery(object):

    def __init__(self, reds, blues):
        self.reds = set(reds)
        self.blues = set(blues)

    def set_date(self, date):
        self.date = date

    def get_name_str(self):
        str_red = "-".join(str(i) for i in self.reds)
        str_blue = "-".join(str(i) for i in self.blues)
        return str_red + ":" + str_blue


class LotteryData(Lottery):
    __default_value = [14, 156, 2915, 99193, 1071285, 21425712]

    def __init__(self, reds, blues):
        super(LotteryData, Lottery.__init__(self, reds, blues))
        self.times = [0 for i in range(METHOD_NUM)]
        self.value = 0
        # self.lottery = []

    def cal_victory(self, lottery):
        def __set_self(i):
            self.times[i] += 1
            self.value += self.__default_value[i]
            # self.lottery.append(lottery)

        methods, index = LotteryCalculate.method_generate(self, lottery)
        if methods:
            __set_self(index)

    def cal(self, lotteries):
        map(self.cal_victory, iter(item for item in lotteries))


class FetchHTML(object):

    url = "http://www.lottery.gov.cn/lottery/dlt/History.aspx?p=%d"

    def fetch_html(self, pages):
        for i in range(pages):
            self.write_one_page(i + 1, self.fetch_one_page(i + 1))

    def fetch_one_page(self, page):
        import requests
        resp = requests.get(self.url % page)
        return resp.text

    def write_one_page(self, page, text):
        name = "data2/page" + str(page) + ".html"
        with open(name, "w") as file:
            file.write(text.encode("UTF-8"))
            file.close()
        print("finished page %d" % page)


class GetLottery():

    @staticmethod
    def get(pages):
        return reduce(lambda x, y: x + y,
                      iter(GetLottery.parse_page(GetLottery.load_one_page(i + 1))
                           for i in range(pages)))

    @staticmethod
    def load_one_page(page):
        name = "data2/page" + str(page) + ".html"
        with open(name, "r") as file:
            text = file.read().decode("UTF-8")
        return text

    @staticmethod
    def parse_page(text):
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
        lotteries = []
        for (red, blue, date) in groups:
            red_list = [int(i.group()) for i in p_num.finditer(red.group())]
            blue_list = [int(i.group()) for i in p_num.finditer(blue.group())]
            lottery = Lottery(red_list, blue_list)
            lottery.set_date(date.group())
            lotteries.append(lottery)
        return lotteries


def get_all_comb():
    from itertools import combinations, product
    reds = combinations(RED_LIST, RED_NUM)
    blues = combinations(BLUE_LIST, BLUE_NUM)
    reds_blues = product(reds, blues)
    lotterydata = []
    for item in reds_blues:
        lotterydata.append((item[0], item[1]))
    return lotterydata, len(lotterydata)


def get_limit_comb(total_split, index):
    import math

    lotterydata, total = get_all_comb()
    num = int(math.ceil(float(total) / float(total_split)))
    start = int(index * num)
    end = int(min((index + 1) * num, total))
    print("build process %d with %d comb : " %
          (index, end - start), total, num, start, end)
    return lotterydata[start: end], end - start


def main_run(data, tID, lotteries):
    import time
    # import sys

    # min_times = sys.maxint
    # max_times = 0
    # min_value = sys.maxint
    # max_value = 0
    # curr_num = 0
    # total_num = data[1]

    start_time = time.time()
    for index, item in enumerate(data[0]):
        # curr_num += 1
        # per = curr_num * 100 / total_num

        i = LotteryData(item[0], item[1])
        i.cal(lotteries)
        # if i.value <= min_value:
        #     min_value = i.value
        #     print((i.get_name_str(), i.times, min_value, "min value ID:%d(%d) in %d/%d" %
        #            (tID, per, curr_num, total_num)))
        # if i.value >= max_value:
        #     max_value = i.value
        #     print((i.get_name_str(), i.times, max_value, "max value ID:%d(%d) in %d/%d" %
        #            (tID, per, curr_num, total_num)))
        # if sum(i.times) <= min_times:
        #     min_times = sum(i.times)
        #     print((i.get_name_str(), i.times, sum(i.times), "min times ID:%d(%d) in %d/%d" %
        #            (tID, per, curr_num, total_num)))
        # if sum(i.times) >= max_times:
        #     max_times = sum(i.times)
        #     print((i.get_name_str(), i.times, sum(i.times), "max times ID:%d(%d) in %d/%d" %
        #            (tID, per, curr_num, total_num)))
        print((i.get_name_str(), sum(i.times), i.value))
    end_time = time.time()
    print("process %d done. %f" % (tID, end_time - start_time))


def main(total_process, index, lotteries):
    main_run(get_limit_comb(total_process, index), index, lotteries)


def main_process(n, lotteries):
    import multiprocessing

    processes = []
    for i in range(n):
        process = multiprocessing.Process(target=main, args=(n, i, lotteries))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()


def print_s(reds, blues):
    lotteries = GetLottery.get(PAGES)
    lotterydata = LotteryData(reds, blues)
    lotterydata.cal(lotteries)
    print(lotterydata.get_name_str(), lotterydata.times, lotterydata.value)

if __name__ == "__main__":
    lotteries = GetLottery.get(PAGES)
    main_process(1, lotteries)

    print("main down.")
