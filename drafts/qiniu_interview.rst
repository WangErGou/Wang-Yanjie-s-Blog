排列和希尔排序
==============

.. author:: default
.. categories:: 技术
.. tags:: 技术, 总结
.. comments::


写点轻松的，，期间被问道两个问题，都是属于以前知道但却不记得了。

排列问题
--------

.. code-block:: python

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


希尔排序
--------

当时听到这个词的时候是一种完全回忆不起来这几个字指什么。
回来之后在 wiki 上看到这张图，才反映过来，妈蛋，这我会啊。

.. image:: f9616f6892819e579a2d4ab10256a732.gif

| 不多说，先写一遍，忆一下往昔峥嵘岁月。

.. code-block:: python

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

复杂度
------

在 wiki 上看到这样一句话：
    用这样步长序列的希尔排序比插入排序和堆排序都要快，甚至在小数组中比快速排序还快，
    但是在涉及大量数据时希尔排序还是比快速排序慢。


#. https://zh.wikipedia.org/wiki/%E5%B8%8C%E5%B0%94%E6%8E%92%E5%BA%8F
#. http://faculty.simpson.edu/lydia.sinapova/www/cmsc250/LN250_Weiss/L12-ShellSort.htm#increments
#. http://www.iti.fh-flensburg.de/lang/algorithmen/sortieren/shell/shellen.htm
