# -*- coding: gbk -*-

import chardet


if __name__ == '__main__':
    s = '中文'
    print s, chardet.detect(s)
    try:
        print s.decode('gbk').encode('utf-8')
    except UnicodeDecodeError as e:
        print e
