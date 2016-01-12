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

协程与生成器
------------


名称解释
--------

四个方法，对 yield expression, excuated code, return to caller


用例
----



.. [1] `PEP 255 -- Simple Generators <https://www.python.org/dev/peps/pep-0255/>`_
