# -*- coding: UTF-8 -*-

RED_NUM = 6
RED_TOTAL = 33
RED_LIST = [i + 1 for i in xrange(RED_TOTAL)]
BLUE_NUM = 1
BLUE_TOTAL = 16
BLUE_LIST = [i + 1 for i in xrange(BLUE_TOTAL)]
METHOD_NUM = 6
METHODS = [
    [(6, 1)],
    [(6, 0)],
    [(5, 1)],
    [(5, 0), (4, 1)],
    [(4, 0), (3, 1)],
    [(2, 1), (1, 1), (0, 1)]
]


class LotteryCalculate(object):

    @staticmethod
    def __method(red, blue, lottery_data, lottery):
        reds = list(set(lottery.reds) & set(lottery_data.reds))
        blues = list(set(lottery.blues) & set(lottery_data.blues))
        return len(reds) == red and len(blues) == blue

    @staticmethod
    def method_generate(lottery_data, lottery):
        for method in METHODS:
            yield reduce(lambda x, y: x or y, [LotteryCalculate.__method(
                item[0], item[1], lottery_data, lottery) for item in method])


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
    __default_value = [1339650, 83728, 8269, 171, 9, 1]

    def __init__(self, reds, blues):
        super(LotteryData, Lottery.__init__(self, reds, blues))
        self.times = [0 for i in xrange(METHOD_NUM)]
        self.value = 0
        # self.lottery = []

    def cal_victory(self, lottery):
        methods = LotteryCalculate.method_generate(self, lottery)
        for i, method in enumerate(methods):
            if method:
                self.times[i] += 1
                self.value += self.__default_value[i]
                # self.lottery.append(lottery)
                break

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


def generate_data_comb(start):
    from itertools import combinations
    RED_LIST_T = [i for i in xrange(start + 1, RED_TOTAL + 1, 1)]
    return combinations(RED_LIST_T, RED_NUM - 1)


def generate_data(threads, index):
    from itertools import combinations, product
    import math

    num = math.ceil(float(RED_TOTAL - RED_NUM + 1) / float(threads))
    start = int(index * num)
    end = int(min((index + 1) * num, RED_TOTAL - RED_NUM + 1))
    num_list = [i + 1 for i in xrange(start, end, 1)]
    blues = combinations(BLUE_LIST, BLUE_NUM)
    print("build thread %d : " % index, num_list, start, end, num)
    for num in num_list:
        reds = generate_data_comb(num)
        reds_blues = product([num], reds, blues)
        for item in reds_blues:
            yield LotteryData((item[0], ) + item[1], item[2])


def inc_percent():
    global percent_num
    lock.acquire()
    percent_num += 1
    lock.release()


def percent_max():
    from itertools import combinations, product

    reds = combinations([i + 1 for i in xrange(33)], 6)
    blues = [i + 1 for i in xrange(16)]
    group = product(reds, blues)
    num = 0
    for i in group:
        num += 1
    return num


def percent():
    __per = 100
    per = int(float(percent_num) / float(MAX_COMB) * __per) + 1
    if per > __per:
        per = __per
    string = ""
    for i in xrange(per):
        string += "="
    for i in xrange(__per - per):
        string += "-"
    print("[" + string + " " + str(percent_num) + "/" + str(MAX_COMB) + "]")
    return percent_num >= MAX_COMB


def main_run(data, tID, lotteries):
    import time

    global min_times
    global max_times
    global min_value
    global max_value

    start_time = time.time()
    for index, i in enumerate(data):
        inc_percent()
        i.cal(lotteries)
        if i.value <= min_value:
            min_value = i.value
            print((i.get_name_str(), i.times, min_value, " min value"))
        if i.value >= max_value:
            max_value = i.value
            print((i.get_name_str(), i.times, max_value, "max value"))
        if sum(i.times) <= min_times:
            min_times = sum(i.times)
            print((i.get_name_str(), i.times, sum(i.times), "min times"))
        if sum(i.times) >= max_times:
            max_times = sum(i.times)
            print((i.get_name_str(), i.times, sum(i.times), "max times"))
        # if index >= 99:
        #     break
    end_time = time.time()
    print("thread %d done. %f" % (tID, (end_time - start_time)))


def main(threads, index, lotteries):
    main_run(generate_data(threads, index), index, lotteries)


def main_thread(n, lotteries):
    import threading
    for i in xrange(n):
        t = threading.Thread(target=main, args=(n, i, lotteries))
        t.setDaemon(True)
        t.start()


def print_s(reds, blues):
    lotteries = GetLottery.get(99)
    lotterydata = LotteryData(reds, blues)
    lotterydata.cal(lotteries)
    print(lotterydata.times)

if __name__ == "__main__":
    import sys
    import time
    import threading
    global lock
    lock = threading.Lock()
    global MAX_COMB
    MAX_COMB = percent_max()

    min_times = sys.maxint
    max_times = 0
    min_value = sys.maxint
    max_value = 0
    percent_num = 0

    lotteries = GetLottery.get(99)
    main_thread(1, lotteries)

    # print_s([15, 16, 17, 18, 19, 21], [14])

    while not percent():
        time.sleep(1)
