# -*- coding: UTF-8 -*-

RED_NUM = 6
RED_TOTAL = 33
RED_LIST = [i + 1 for i in xrange(RED_TOTAL)]
BLUE_NUM = 1
BLUE_TOTAL = 16
BLUE_LIST = [i + 1 for i in xrange(BLUE_TOTAL)]
METHOD_NUM = 6
METHODS = [
    [(2, 1), (1, 1), (0, 1)],
    [(4, 0), (3, 1)],
    [(5, 0), (4, 1)],
    [(5, 1)],
    [(6, 0)],
    [(6, 1)]
]
MAX_COMB = 17721088


class LotteryCalculate(object):

    @staticmethod
    def __method(red, blue, lottery_data, lottery):
        reds = set(lottery_data.reds) & set(lottery.reds)
        blues = set(lottery_data.blues) & set(lottery.blues)
        return len(reds) is red and len(blues) is blue

    @staticmethod
    def method_generate(lottery_data, lottery):
        for i, method in enumerate(METHODS):
            for item in method:
                if LotteryCalculate.__method(
                        item[0], item[1], lottery_data, lottery):
                    return True, i
        return False, 0


class Lottery(object):

    def __init__(self, reds, blues):
        self.reds = reds
        self.blues = blues

    def set_date(self, date):
        self.date = date

    def get_name_str(self):
        str_red = "-".join(str(i) for i in self.reds)
        str_blue = "-".join(str(i) for i in self.blues)
        return str_red + ":" + str_blue


class LotteryData(Lottery):
    __default_value = [1, 9, 171, 8269, 83728, 1339650]

    def __init__(self, reds, blues):
        super(LotteryData, Lottery.__init__(self, reds, blues))
        self.times = [0 for i in xrange(METHOD_NUM)]
        self.value = 0
        # self.lottery = []

    def cal_victory(self, lottery):
        methods, i = LotteryCalculate.method_generate(self, lottery)
        if methods:
            self.times[i] += 1
            self.value += self.__default_value[i]
            # self.lottery.append(lottery)

    def cal(self, lotteries):
        map(self.cal_victory, [item for item in lotteries])


class FetchHTML(object):

    url = "http://kaijiang.zhcw.com/zhcw/html/ssq/list_%d.html"

    def fetch_html(self, pages):
        for i in xrange(pages):
            self.write_one_page(i + 1, self.fetch_one_page(i + 1))

    def fetch_one_page(self, page):
        import requests
        resp = requests.get(self.url % page)
        return resp.text

    def write_one_page(self, page, text):
        name = "data/page" + str(page) + ".html"
        with open(name, "w") as file:
            file.write(text.encode("UTF-8"))
            file.close()
        print "finished page %d" % page


class GetLottery():

    @staticmethod
    def get(pages):
        return reduce(lambda x, y: x + y,
                      [GetLottery.parse_page(GetLottery.load_one_page(i + 1))
                       for i in xrange(pages)])

    @staticmethod
    def load_one_page(page):
        name = "data/page" + str(page) + ".html"
        with open(name, "r") as file:
            text = file.read().decode("UTF-8")
        return text

    @staticmethod
    def parse_page(text):
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
        lotteries = []
        for date in dates:
            red_list = [int(p_num.search(reds.next().group()).group())
                        for i in xrange(RED_NUM)]
            blue_list = [int(p_num.search(blues.next().group()).group())
                         for i in xrange(BLUE_NUM)]
            lottery = Lottery(red_list, blue_list)
            lottery.set_date(p_date_str.search(date.group()).group())
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
    print("build process %d with %d comb : " % (index, end - start), total, num, start, end)
    return lotterydata[start: end], end - start


def main_run(data, tID, lotteries):
    import time
    import sys

    min_times = sys.maxint
    max_times = 0
    min_value = sys.maxint
    max_value = 0
    curr_num = 0

    start_time = time.time()
    total_num = data[1]
    for index, item in enumerate(data[0]):
        i = LotteryData(item[0], item[1])
        i.cal(lotteries)
        curr_num += 1
        per = curr_num * 100 / total_num
        if i.value <= min_value:
            min_value = i.value
            print((i.get_name_str(), i.times, min_value, "min value ID:%d(%d) in %d/%d" %
                   (tID, per, curr_num, total_num)))
        if i.value >= max_value:
            max_value = i.value
            print((i.get_name_str(), i.times, max_value, "max value ID:%d(%d) in %d/%d" %
                   (tID, per, curr_num, total_num)))
        if sum(i.times) <= min_times:
            min_times = sum(i.times)
            print((i.get_name_str(), i.times, sum(i.times), "min times ID:%d(%d) in %d/%d" %
                   (tID, per, curr_num, total_num)))
        if sum(i.times) >= max_times:
            max_times = sum(i.times)
            print((i.get_name_str(), i.times, sum(i.times), "max times ID:%d(%d) in %d/%d" %
                   (tID, per, curr_num, total_num)))
    end_time = time.time()
    print("process %d done. %f" % (tID, end_time - start_time))


def main(total_process, index, lotteries):
    main_run(get_limit_comb(total_process, index), index, lotteries)


def main_process(n, lotteries):
    import multiprocessing

    processes = []
    for i in xrange(n):
        process = multiprocessing.Process(target=main, args=(n, i, lotteries))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()


def print_s(reds, blues):
    lotteries = GetLottery.get(99)
    lotterydata = LotteryData(reds, blues)
    lotterydata.cal(lotteries)
    print(lotterydata.get_name_str(), lotterydata.times, lotterydata.value)

if __name__ == "__main__":

    lotteries = GetLottery.get(99)
    main_process(60, lotteries)

    print "main down."

    # print_s([15, 23, 24, 28, 31, 33], [4])
    # print_s([1, 14, 17, 18, 22, 26], [9])
