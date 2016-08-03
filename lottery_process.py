# -*- coding: UTF-8 -*-


class LotteryMethod(object):
    METHODS = []

    def method(self, red, blue, lottery1, lottery2):
        reds = lottery1.reds & lottery2.reds
        blues = lottery1.blues & lottery2.blues
        return len(reds) is red and len(blues) is blue

    def method_generate(self, lottery1, lottery2):
        for i, method in enumerate(self.METHODS):
            for item in method:
                if self.method(item[0], item[1], lottery1, lottery2):
                    return True, i
        return False, 0


class Lottery(object):
    RED_TOTAL = 0
    BLUE_TOTAL = 0
    RED_NUM = 0
    BLUE_NUM = 0

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
    default_value = []
    method = None

    def __init__(self, reds, blues):
        super(LotteryData, Lottery.__init__(self, reds, blues))
        self.times = [0 for i in range(len(self.default_value))]
        self.value = 0

    def cal_victory(self, lottery):
        def __set_self(i):
            self.times[i] += 1
            self.value += self.default_value[i]
        methods, index = self.method.method_generate(self, lottery)
        if methods:
            __set_self(index)

    def cal(self, lotteries):
        map(self.cal_victory, iter(item for item in lotteries))


class FetchHTML(object):
    URL = "%d"
    TARGET = "%d"
    PAGES = 0

    def fetch_html(self):
        for i in range(self.PAGES):
            self.write_one_page(i + 1, self.fetch_one_page(i + 1))

    def fetch_one_page(self, page):
        import requests
        resp = requests.get(self.URL % page, timeout=30)
        return resp.text

    def write_one_page(self, page, text):
        with open(self.TARGET % page, "w") as file:
            file.write(text.encode("UTF-8"))
            file.close()
        print("finished page %d" % page)


class LotteryLoader():
    TARGET = "%d"
    PAGES = 0
    RED_NUM = 0
    BLUE_NUM = 0

    def load(self):
        return reduce(lambda x, y: x + y,
                      iter(self.parse_page(self.load_one_page(i + 1))
                           for i in range(self.PAGES)))

    def load_one_page(self, page):
        with open(self.TARGET % page, "r") as file:
            text = file.read().decode("UTF-8")
        return text

    def parse_page(self, text):
        return []


class LotteryProcess(object):
    LotteryClass = Lottery
    LotteryDataClass = LotteryData
    LotteryMethodClass = LotteryMethod
    LotteryFetchClass = FetchHTML
    LotteryLoadClass = LotteryLoader

    def __init__(self):
        self.method = self.LotteryMethodClass()
        self.fetcher = self.LotteryMethodClass()
        self.loader = self.LotteryLoadClass()

    def get_all_comb(self, red_num, blue_num, red_list, blue_list):
        from itertools import combinations, product
        reds = combinations(red_list, red_num)
        blues = combinations(blue_list, blue_num)
        reds_blues = product(reds, blues)
        comb_list = []
        for item in reds_blues:
            comb_list.append((item[0], item[1]))
        return comb_list, len(comb_list)

    def get_limit_comb(self, total_split, index, comb, total):
        import math
        num = int(math.ceil(float(total) / float(total_split)))
        start = int(index * num)
        end = int(min((index + 1) * num, total))
        print("build process %d with %d comb : " % (index, end - start), total, num, start, end)
        return comb[start: end], end - start

    def prepare_for(self):
        def __setup_lottery(reds, blues, date):
            lottery = self.LotteryClass(reds, blues)
            lottery.date = date
            return lottery
        item_list = self.loader.load()
        lotteries = [__setup_lottery(i[0], i[1], i[2]) for i in item_list]
        red_list = [i + 1 for i in range(self.LotteryClass.RED_TOTAL)]
        blue_list = [i + 1 for i in range(self.LotteryClass.BLUE_TOTAL)]
        comb, total = self.get_all_comb(self.LotteryClass.RED_NUM,
                                        self.LotteryClass.BLUE_NUM, red_list, blue_list)
        return lotteries, comb, total

    def main_run(self, data, tID, lotteries):
        import time
        import sys

        min_times = sys.maxint
        max_times = 0
        min_value = sys.maxint
        max_value = 0
        curr_num = 0
        total_num = data[1]

        start_time = time.time()
        for index, item in enumerate(data[0]):
            curr_num += 1
            per = curr_num * 100 / total_num

            i = self.LotteryDataClass(item[0], item[1])
            i.method = self.method
            i.cal(lotteries)

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

    def main_process(self, total_process, index, lotteries, comb, total):
        self.main_run(self.get_limit_comb(total_process, index, comb, total), index, lotteries)

    def main(self, n):
        lotteries, comb, total = self.prepare_for()
        if n == 1:
            self.main_process(1, 0, lotteries, comb, total)
        else:
            import multiprocessing
            processes = []
            for i in range(n):
                process = multiprocessing.Process(target=self.main_process,
                                                  args=(n, i, lotteries, comb, total))
                process.start()
                processes.append(process)
            for process in processes:
                process.join()

    def print_s(self, reds, blues):
        lotteries = self.loader.load()
        lotterydata = self.LotteryDataClass(reds, blues)
        lotterydata.method = self.method
        lotterydata.cal(lotteries)
        print(lotterydata.get_name_str(), lotterydata.times, lotterydata.value)
