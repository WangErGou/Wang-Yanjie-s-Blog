# -*- coding: euc-jp -*-

import chardet


if __name__ == '__main__':
    s = '��'
    print s, chardet.detect(s)
    try:
        print s.decode('gbk').encode('utf-8')
    except UnicodeDecodeError as e:
        print e
    try:
        print s.decode('euc-jp').encode('utf-8')
    except UnicodeDecodeError as e:
        print e
