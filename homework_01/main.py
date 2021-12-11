"""
Домашнее задание №1
Функции и структуры данных
"""


def power_numbers(*args):
    return [x * x for x in list(args)]


# filter types
ODD = "odd"
EVEN = "even"
PRIME = "prime"


def is_prime(number):
    if number == 2:
        return True
    if number < 2:
        return False
    for d in range(2, number // 2 + 1):
        if number % d == 0:
            return False
    return True


def filter_numbers(arr, filter_type):
    if filter_type == ODD:
        return list(filter(lambda x: x % 2 != 0, arr))
    if filter_type == EVEN:
        return list(filter(lambda x: x % 2 == 0, arr))
    if filter_type == PRIME:
        return list(filter(is_prime, arr))
