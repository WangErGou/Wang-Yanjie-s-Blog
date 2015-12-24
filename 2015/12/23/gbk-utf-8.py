# -*- coding:utf-8 -*-

import chardet


if __name__ == '__main__':
    s = 'жпнд'
    print s, chardet.detect(s)
