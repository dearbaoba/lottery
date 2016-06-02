# -*- coding: UTF-8 -*-


class LotteryCalculate(object):

    @staticmethod
    def __method(red, blue, lottery_data, lottery):
        reds = filter((lambda x: x in lottery.reds), lottery_data.reds)
        blues = filter((lambda x: x in lottery.blues), lottery_data.blues)
        return len(reds) == red and len(blues) == blue

    @staticmethod
    def method_1(lottery_data, lottery):
        return LotteryCalculate.__method(6, 1, lottery_data, lottery)

    @staticmethod
    def method_2(lottery_data, lottery):
        return LotteryCalculate.__method(6, 0, lottery_data, lottery)

    @staticmethod
    def method_3(lottery_data, lottery):
        return LotteryCalculate.__method(5, 1, lottery_data, lottery)

    @staticmethod
    def method_4(lottery_data, lottery):
        return LotteryCalculate.__method(5, 0, lottery_data, lottery) \
            or LotteryCalculate.__method(4, 1, lottery_data, lottery)

    @staticmethod
    def method_5(lottery_data, lottery):
        return LotteryCalculate.__method(4, 0, lottery_data, lottery) \
            or LotteryCalculate.__method(3, 1, lottery_data, lottery)

    @staticmethod
    def method_6(lottery_data, lottery):
        return LotteryCalculate.__method(2, 1, lottery_data, lottery) \
            or LotteryCalculate.__method(1, 1, lottery_data, lottery) \
            or LotteryCalculate.__method(0, 1, lottery_data, lottery)


class Lottery(object):

    def __init__(self, reds, blues):
        self.reds = reds
        self.blues = blues

    def get_name_str(self):
        str_red = "-".join(str(i) for i in self.reds)
        str_blue = "-".join(str(i) for i in self.blues)
        return str_red + ":" + str_blue


class LotteryData(Lottery):
    __default_values = [5000000, 180000, 3000, 200, 10, 5]
    times = [0, 0, 0, 0, 0, 0]
    values = [0, 0, 0, 0, 0, 0]

    def cal_victory(self, lottery):
        methods = [
            LotteryCalculate.method_1,
            LotteryCalculate.method_2,
            LotteryCalculate.method_3,
            LotteryCalculate.method_4,
            LotteryCalculate.method_5,
            LotteryCalculate.method_6
        ]

        for i in range(len(methods)):
            if methods[i](self, lottery):
                self.times[i] += 1
                self.values[i] += self.__default_values[i]


class FetchHTML(object):

    url = "http://kaijiang.zhcw.com/zhcw/html/ssq/list_%d.html"

    def fetch_html(self, pages):
        for i in range(pages):
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


class CreateLottery():
    lotteries = []

    def __init__(self, pages):
        self.pages = pages

    def create(self):
        for i in range(self.pages):
            self.parse_page(self.load_one_page(i + 1))
        return self.lotteries

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
        p_num = re.compile(r'\d+')
        reds = p_reds.findall(text)
        blues = p_blues.findall(text)
        for i in range(len(blues)):
            lottery = Lottery([
                int(p_num.findall(reds[i * 6])[0]),
                int(p_num.findall(reds[i * 6 + 1])[0]),
                int(p_num.findall(reds[i * 6 + 2])[0]),
                int(p_num.findall(reds[i * 6 + 3])[0]),
                int(p_num.findall(reds[i * 6 + 4])[0]),
                int(p_num.findall(reds[i * 6 + 5])[0])
            ],
                [int(p_num.findall(blues[i])[0])])
            self.lotteries.append(lottery)

if __name__ == "__main__":
    win_lotteries = CreateLottery(99).create()
