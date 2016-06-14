# -*- coding: UTF-8 -*-
from lottery1 import LotteryLoader1


dict_red = {}
dict_blue = {}


def add_to_dict(keyword, dictionary):
    if dictionary.get(keyword) is None:
        dictionary[keyword] = 1
    else:
        dictionary[keyword] += 1


def loop_to_dict(keywords, dictionary):
    for i in keywords:
        add_to_dict(i, dictionary)


def sort_dict(dictionary):
    return sorted(dictionary.items(),
                  cmp=lambda x, y: x - y,
                  key=lambda e: e[1],
                  reverse=True)


def print_dict(dictionary):
    for i in dictionary:
        print i


for i in LotteryLoader1().load():
    loop_to_dict(i[0], dict_red)
    loop_to_dict(i[1], dict_blue)


dict_red = sort_dict(dict_red)
dict_blue = sort_dict(dict_blue)

print "==== red ===="
print_dict(dict_red)
print "==== blue ===="
print_dict(dict_blue)
