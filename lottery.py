# -*- coding: UTF-8 -*-
import threading


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
    date = "0000"

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

    def __init__(self, reds, blues):
        super(LotteryData, Lottery.__init__(self, reds, blues))
        self.times = [0, 0, 0, 0, 0, 0]
        # self.lottery = []

    def cal_victory(self, lottery):
        methods = [
            # LotteryCalculate.method_1,
            # LotteryCalculate.method_2,
            # LotteryCalculate.method_3
            # LotteryCalculate.method_4
            # LotteryCalculate.method_5
            LotteryCalculate.method_6
        ]

        for i in xrange(len(methods)):
            if methods[i](self, lottery):
                self.times[i] += 1
                # self.lottery.append(lottery)
                break


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
        p_date = re.compile(r'<td align="center">\d+</td>')
        p_num = re.compile(r'\d+')
        reds = p_reds.findall(text)
        blues = p_blues.findall(text)
        dates = p_date.findall(text)
        for i in xrange(len(blues)):
            lottery = Lottery([
                int(p_num.findall(reds[i * 6])[0]),
                int(p_num.findall(reds[i * 6 + 1])[0]),
                int(p_num.findall(reds[i * 6 + 2])[0]),
                int(p_num.findall(reds[i * 6 + 3])[0]),
                int(p_num.findall(reds[i * 6 + 4])[0]),
                int(p_num.findall(reds[i * 6 + 5])[0])
            ],
                [int(p_num.findall(blues[i])[0])])
            lottery.set_date(p_num.findall(dates[i])[0])
            self.lotteries.append(lottery)


def cal(lotterydata, lottery):
    for item in lottery:
        lotterydata.cal_victory(item)


def generate_thread(start, end):
    lottery = GetLottery.load()
    red_num = 33
    blue_num = 16
    for a in xrange(start, end, 1):
        for b in xrange(a + 1, red_num, 1):
            for c in xrange(b + 1, red_num, 1):
                for d in xrange(c + 1, red_num, 1):
                    for e in xrange(d + 1, red_num, 1):
                        for f in xrange(e + 1, red_num, 1):
                            for g in xrange(blue_num):
                                lotterydata = LotteryData(
                                    [a + 1, b + 1, c + 1, d + 1, e + 1, f + 1], [g + 1])
                                cal(lotterydata, lottery)
                                yield lotterydata


def generate():
    return generate_thread(0, 33)


def thread_print(arg):
    lock.acquire()
    print arg
    lock.release()


def thread_set_min(num):
    global min_num
    lock.acquire()
    min_num = num
    lock.release()


def main_thread(data, num):
    print "start %d" % num
    for i in data:
        if i.times[0] <= min_num:
            thread_set_min(i.times[0])
            thread_print((i.get_name_str(), min_num, "at %d" % num))
    thread_print("done %d." % num)


def main():
    for i in xrange(1, 33, 1):
        t = threading.Thread(target=main_thread, args=(generate_thread(i, i + 1), i + 1))
        t.setDaemon(True)
        t.start()


def main_s():
    data = generate()
    main_thread(data, 0)

if __name__ == "__main__":
    # GetLottery(99).get()
    global lock
    min_num = 999
    lock = threading.Lock()
    main()
    main_thread(generate_thread(0, 1), 0)
    # main_s()
