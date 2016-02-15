# -*- coding:utf-8 -*-

import random


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


def F():
    a, b = 0, 1
    yield a
    yield b
    while True:
        a, b = b, a+b
        yield b


if __name__ == '__main__':
    for i, e in enumerate(F()):
        print i, e
        if i == 10:
            break
