import concurrent.futures
import logging
import multiprocessing
from time import time
from multiprocessing import cpu_count

multiprocessing.set_start_method('spawn')
logging.basicConfig(level=logging.DEBUG, format='%(msecs)d %(threadName)s %(message)s %(lineno)d')

test_list = [128, 255, 99999, 10651060]

print(f'Cores are available in amount of: {cpu_count()}')


def factorize(x: int) -> set:
    match_set = set()
    y = 1
    while y <= x:
        if x % y == 0:
            match_set.add(y)
        y += 1
    # print(match_set)
    return match_set


timer = time()

with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count()) as executor:
    results = executor.map(factorize, test_list)

output = set()
for particle in results:
    output |= particle

list_unsorted = list(output)
list_sorted = list_unsorted.sort()

print(list_unsorted)

logging.debug(f'Done {time() - timer}')

# a, b, c, d  = factorize(128, 255, 99999, 10651060)

# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
