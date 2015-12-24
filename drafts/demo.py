# -*- coding: utf-8 -*-

import random


def insert_sort_with_step(data, start=0, step=1):
    '''
    只考虑该考虑的元素
    数组被分成已排序和未排序两部分
    遍历数组，保证：
        - 当前元素左边的元素都是有序的
        - 当前元素及右边的元素是无序的
    对于当前遍历的元素：
        - 如果这个元素大于已排序元素中的最大值，pass
        - 如果这个元素小于已排序元素中的最大值，
          将其移到合适的位置
    '''
    if len(data) < step:
        return data
    for i in range(start+step, len(data), step):
        j = i - step   # 已排序元素中的最大值
        if data[i] > data[j]:
            continue
        else:
            for k in range(j, start-step, -step):
                if data[k] < data[i]:
                    data[k+step], data[k+2*step:i+step:step] = \
                        data[i], data[k+step:i:step]
                    break
            else:
                data[start], data[start+step:i+step:step] = \
                    data[i], data[start:i:step]
    return data


def shell_sort(data):
    '''
    希尔排序
    '''
    if len(data) < 2:
        return data
    step = len(data) / 2
    while step:
        for row in range(step):
            insert_sort_with_step(data, row, step)
        step /= 2
    return data


def test_sort():
    data = []
    for _ in range(random.randint(1, 30)):
        data.append(random.randint(-30, 30))
    print 'before sort: {0}'.format(' '.join(map(str, data)))
    data = shell_sort(data)
    print 'after  sort: {0}'.format(' '.join(map(str, data)))


import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def draw():
    quick_complex = []
    shell_complex = []
    for x in range(1, 100000):
        quick_complex.append(x * math.log(x, 2))
        shell_complex.append(math.pow(x, 1.25))
    x = range(1, 100000)
    plt.plot(x, quick_complex, label='Quick Sort')
    plt.plot(x, shell_complex, 'r', label='Shell Sort')
    plt.savefig('draw.png')


def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


if __name__ == '__main__':
    import pdb
    pdb.set_trace()
    for _ in permutations(range(10)):
        pass
