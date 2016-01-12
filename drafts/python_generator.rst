未定
====

.. author:: default
.. categories:: 技术
.. tags:: Python
.. comments::


前言
----

先来看一段代码，直接能懂的话，后面的内容看下去的意义也就不大了。

.. code-block:: python

    def consume():
        while True:
            q = yield
            while len(q) > 0:
                product = q.pop(0)
                print 'consume {0}'.format(product)


    def produce(consumer):
        q = []
        consumer.send(None)
        while True:
            while len(q) < 3:
                product = random.randint(30, 100)
                q.append(product)
                print 'produce {0}'.format(product)
            yield consumer.send(q)


    def main():
        consumer = consume()
        producer = produce(consumer)

        producer.next()
        for i in range(10):
            print 'TIME: {0}'.format(i)
            producer.next()


    if __name__ == '__main__':
        main()

协程
----

普通的子程序（subroutine）只有一个程序的入口，当退出子程序后，子程序就真正的结束了。
当再次执行子程序时，就是彻底的重新执行一次。
而协程（coroutine）不同之处在于：它有多个重入点（re-entry point）。
当从重入点离开时，协程会被暂停 —— 协程当前的状态和变量都会被保存下来。
当从重入点再次进入是，协程会恢复之前暂停的状态，继续执行，直到遇到下个重入点或者退出。

而一个协程调用另外一个协程的操作就叫做“yielding”。

我们可以通过一个简单的生产者和消费者问题来看看协程的使用 [1]_ ::
    var q := new queue 

    coroutine produce
    loop
        while q is not full
            create some new items
            add the items to q
        yield to consume

    coroutine consume
    loop
        while q is not empty
            remove some items from q
            use the items
        yield to produce


生成器
------

Generator 的概念在 Python 2.2 中由 `PEP 255 -- Simple Generators <https://www.python.org/dev/peps/pep-0255/>`_ 引入，
在 Python 2.5 中由 `PEP 342 -- Coroutines via Enhanced Generators <https://www.python.org/dev/peps/pep-0342/>`_ 加强，
具备了大部分协程的功能。


名词解释
++++++++

``yield`` 是 Python 的关键字，只可以用在 ``generator function`` 的定义中。

``generator function`` 与普通函数的区别在于：

    - 定义中使用了 ``yield`` 关键字。
    - 被调用后并不会直接执行，而是返回一个 ``generator iterator`` 对象。

``generator expression`` 在语法上类似 ``for comprehension`` ，
返回一个 ``generator iterabtor`` 对象。

``generator iterator`` 主要的方法有 ``next()`` ， ``send()`` ， ``throw(type[, value[, tracebakc]])`` 和 ``close()`` 。


.. _my_iterator:

Iterators
+++++++++

从 ``generator`` 这个名字上我们就可以看出 ``generator``
初始目的应该是用来简化 ``iterator`` 。

| 以实现斐波那契数列为例来说明 ``yield`` 和 ``generator function`` 的作用：

.. code-block:: python

    def F():
        a, b = 0, 1
        yield a
        yield b
        while True:
            a, b = b, a+b
            yield b

而大多数时候，使用 ``generator`` 代替 ``iterator`` 的原因也确实在于：
``generator`` 写起来比 ``iterator`` 更简单。
以如下两段相同功能的代码为例：

| 使用 ``generator function``

.. code-block:: python

    def squares(start, stop):
        for i in xrange(start, stop):
            yield i * i

    generator = squares(a, b)

| 使用 ``iterator``

.. code-block:: python

    class Squares(object):
        def __init__(self, start, stop):
           self.start = start
           self.stop = stop
        def __iter__(self): return self
        def next(self):
           if self.start >= self.stop:
               raise StopIteration
           current = self.start * self.start
           self.start += 1
           return current

    iterator = Squares(a, b)


Coroutine
+++++++++

不幸的一件事是：我有很长一段时间不了解协程这个概念，也不知道 ``generator iterator`` 的
``send()`` ， ``throw()`` 和 ``close()`` 方法。
当我初次遇到 ``yield`` 这个关键词，我还没有直接看文档的习惯，
而网上的大部分内容讲的都和我在 :ref:`my_iterator`_ 中讲的相似。
所以，我有很长的一段时间简单的认为 ``generator`` 只是 Python 的一个小把戏。


.. [1] `Coroutine <https://en.wikipedia.org/wiki/Coroutine>`_
