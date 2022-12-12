import logging
from time import time

logging.basicConfig(level=logging.DEBUG, format='%(msecs)d %(threadName)s %(message)s %(lineno)d')

test_list = [128, 255, 99999, 10651060]


def factorize(input_nums: list[int]) -> list:
    timer = time()
    match_set = set()

    for x in input_nums:
        y = 1
        while y <= x:
            if x % y == 0:
                match_set.add(y)
            y += 1

    match_list = list(match_set)
    match_list.sort()
    print(match_list)
    logging.debug(f'Done {time() - timer}')

    return match_list


factorize(test_list)

# a, b, c, d  = factorize(128, 255, 99999, 10651060)

# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
