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
        reds = filter((lambda x: x in lottery.reds), lottery_data.reds)
        blues = filter((lambda x: x in lottery.blues), lottery_data.blues)
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
        self.times = [0, 0, 0, 0, 0, 0]
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
    path = "lottery.pkl"
    lotteries = []

    def __init__(self, pages):
        self.pages = pages

    def get(self):
        import pickle
        for i in xrange(self.pages):
            self.parse_page(self.load_one_page(i + 1))
        with open(self.path, "wb") as file:
            pickle.dump(self.lotteries, file)
            file.close()

    @staticmethod
    def load():
        import pickle
        with open(GetLottery.path, "rb") as file:
            lotteries = pickle.load(file)
            file.close()
        return lotteries

    def load_one_page(self, page):
        name = "data/page" + str(page) + ".html"
        with open(name, "r") as file:
            text = file.read().decode("UTF-8")
        return text

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
        for date in dates:
            red_list = [int(p_num.search(reds.next().group()).group())
                        for i in xrange(RED_NUM)]
            blue_list = [int(p_num.search(blues.next().group()).group())
                         for i in xrange(BLUE_NUM)]
            lottery = Lottery(red_list, blue_list)
            lottery.set_date(p_date_str.search(date.group()).group())
            self.lotteries.append(lottery)


def generate_data():
    from itertools import combinations, product
    lotteries = GetLottery.load()
    reds = combinations(RED_LIST, RED_NUM)
    blues = combinations(BLUE_LIST, BLUE_NUM)
    reds_blues = product(reds, blues)
    for item in reds_blues:
        lotterydata = LotteryData(item[0], item[1])
        lotterydata.cal(lotteries)
        yield lotterydata


def main_run(data):
    import sys
    min_times = sys.maxint
    max_times = 0
    min_value = sys.maxint
    max_value = 0
    for i in data:
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
    print("done.")


def main():
    data = generate_data()
    main_run(data)


def print_s(reds, blues):
    lotteries = GetLottery.load()
    lotterydata = LotteryData(reds, blues)
    lotterydata.cal(lotteries)
    print(lotterydata.times)

if __name__ == "__main__":
    # GetLottery(99).get()
    main()
    # print_s([15, 16, 17, 18, 19, 21], [14])
