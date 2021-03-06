import math


def c(a, b):
    return math.factorial(a) / math.factorial(a - b) / math.factorial(b)

print(1, 1)
print(2, c(16, 1))
print(3, c(6, 5) * c(27, 1))
print(4, c(6, 5) * c(16, 1) +
      c(6, 4) * c(27, 2))
print(5, c(6, 4) * c(27, 2) * c(16, 1) +
      c(6, 3) * c(27, 3))
print(6, c(6, 2) * c(27, 4) +
      c(6, 1) * c(27, 5) +
      c(27, 6))
print("all", c(33, 6) * c(16, 1))

# (1, 1)
# (2, 16)
# (3, 162)
# (4, 5361)
# (5, 142740)
# (6, 1043640)
# ('all', 17721088)

print("=================")

print(1, 1)
print(2, c(2, 1) * c(10, 1))
print(3, c(12, 2) +
      c(5, 4) * c(30, 1))
print(4, c(5, 4) * c(30, 1) * c(2, 1) * c(10, 1) +
      c(5, 3) * c(30, 2))
print(5, c(5, 4) * c(30, 1) * c(12, 2) +
      c(5, 3) * c(30, 2) * c(2, 1) * c(10, 1) +
      c(5, 2) * c(30, 3))
print(6, c(5, 3) * c(30, 2) * c(12, 2) +
      c(5, 1) * c(30, 4) +
      c(5, 2) * c(30, 3) * c(2, 1) * c(10, 1) +
      c(35, 5))
print("all", c(35, 5) * c(12, 2))

# (1, 1)
# (2, 20)
# (3, 216)
# (4, 7350)
# (5, 137500)
# (6, 1560757)
# ('all', 21425712)
