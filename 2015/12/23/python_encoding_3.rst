Python字符串编码问题
====================

.. author:: default
.. categories:: 技术
.. tags:: Python, 总结
.. comments::

这是第三次整理有关和 Python 字符串编码相关的知识，前两次整理、理解完后写的测试都没有能按照预想的执行。
今天终于能把自己的理解走通，所以整理与此。有些想法没有想到验证的方法，所以 **不敢保证绝对正确** 。

相关概念
--------

character && code point
+++++++++++++++++++++++

- character 字符, 比如说 `A` 。
- code point 字符码，代表字符的数字。

| 在一套字符集中，字符和字符码必然是一一对应的。
| 不同字符集中，相同字符的字符码 **可能** 不同。
| 比如说，在字符集 Unicode 中字符 `木` 对应的字符码是 `230156168` 。
| 在字符集 GBK 中字符 `木` 对应的字符码是 `196189` 。

character set && encoding
+++++++++++++++++++++++++

- character set 字符集，包括了大量的 **字符** 和对应的 **字符码** 。
- encoding 编码格式，一种规则，规定了我们怎么在硬盘上存储某字符集。

具体而言，Unicode，GBK 之类是字符集，它们规定了集合中包括的 **字符** 和每个字符对应 **字符码** 。
UTF-8，UTF-16 是编码方式，它们决定了 Unicode 字符集怎么存储。

| 举个例子的话， 字符 `木` 在Unicode 字符集中对应的字符码是 `230156168` 。
| 当按 UTF-8 编码时，该字符在硬盘上占据了三个字节，存储的内容是： `11100110 10011100 10101000` 。
| 当按 UTF-16 编码时，该字符在硬盘上占据两个字节，存储的内容是： `01100111 00101000`

encode && decode
++++++++++++++++

- encode 编码，在 Python 2.x 中值将 `unicode` 转换成 `str` 。
- decode 解码，在 Python 2.x 中指将 `str` 转换成 `unicode` 。

`u` && `U` && `\u` && `\U` && `x`
---------------------------------

Python 中，通过在一个字符串的最前面加上 `u` 或者 `U`
可以声明这个字符串 `unicode` 。在 `unicode` 中，你可以通过 `\u` 或者 `\U`
来转义字符， `\u` 可以转义随后的 4 个十六进制字符，而 `\U`
可以转义随后的 8 个十六进制字符。无论是 `unicode` 还是 `str` 中，都可以通过 `\x` 来转义随后的 2 个十六进制字符。

`coding:<encoding>`
-------------------

之前写的两篇文章中，一直都困惑于这句声明，现在也不敢保证自己的理解一定正确，有想法的或者愿意指正我错误的请留言。

.. _python_parse:

源文件的解析
++++++++++++

Python 解析源文件需要经过 5 个步骤：

   1. read the file

   2. decode it into Unicode assuming a fixed per-file encoding

   3. convert it into a UTF-8 byte string

   4. tokenize the UTF-8 content

   5. compile it, creating Unicode objects from the given Unicode data
      and creating string objects from the Unicode literal data
      by first reencoding the UTF-8 data into 8-bit string data
      using the given file encoding


`coding:<encoding>` 的作用
++++++++++++++++++++++++++

首先引用下 `PEP 0326 <https://www.python.org/dev/peps/pep-0263/>`_ 中的原文：

    The encoding information is then used by the Python parser to interpret the file using the given encoding.

我的理解是：

    我们通过 `coding:<encoding>` 告诉 Python 文件的编码格式是 encoding。随后，Python 在 decode it into Unicode 时就会使用这条信息。

为了验证这一点，我准备了如下四个文件。

.. code-block:: python
    :caption: gbk-gbk.py （文件编码格式为 GBK）

    # -*- coding:gbk -*-

    import chardet


    if __name__ == '__main__':
        s = '中文'
        print s, chardet.detect(s)
        try:
            print s.decode('gbk').encode('utf-8')
        except UnicodeDecodeError as e:
            print e

.. code-block:: python
    :caption: gbk-euc.py （文件编码格式为 GBK）

    # -*- coding:euc-jp -*-

    import chardet


    if __name__ == '__main__':
        s = '中文'
        print s, chardet.detect(s)
        try:
            print s.decode('gbk').encode('utf-8')
        except UnicodeDecodeError as e:
            print e
        try:
            print s.decode('euc-jp').encode('utf-8')
        except UnicodeDecodeError as e:
            print e

.. code-block:: python
    :caption: euc-euc.py （文件编码格式为 EUC-JP）

    # -*- coding: euc-jp -*-

    import chardet


    if __name__ == '__main__':
        s = '中国の'
        print s, chardet.detect(s)
        try:
            print s.decode('euc-jp').encode('utf-8')
        except UnicodeDecodeError as e:
            print e

.. code-block:: python
    :caption: euc-gbk.py （文件编码格式为 EUC-JP）

    # -*- coding: gbk -*-

    import chardet


    if __name__ == '__main__':
        s = '中国の'
        print s, chardet.detect(s)
        try:
            print s.decode('euc-jp').encode('utf-8')
        except UnicodeDecodeError as e:
            print e
        try:
            print s.decode('gbk').encode('utf-8')
        except UnicodeDecodeError as e:
            print e

| 依次执行这四个文件（当前系统的 LANG 设置为 en_US.UTF-8）,结果如下（注意每个文件的编码格式）。

.. code-block:: console

    [root@iZ25012hd8kZ myblog]# python gbk-gbk.py 
    אτ {'confidence': 0.99, 'encoding': 'GB2312'}
    中文
    [root@iZ25012hd8kZ myblog]# python gbk-euc.py 
    אτ {'confidence': 0.99, 'encoding': 'GB2312'}
    中文
    嶄猟
    [root@iZ25012hd8kZ myblog]# python euc-euc.py 
    Ħ¹匠{'confidence': 0.99, 'encoding': 'EUC-JP'}
    中国の
    [root@iZ25012hd8kZ myblog]# python euc-gbk.py 
    Ħ¹匠{'confidence': 0.99, 'encoding': 'EUC-JP'}
    中国の
    面柜の

我们依次来分析三句 print 的效果：

    #. print s
        打印的内容和 s 的内容是不相符的，这是因为文件的编码格式和系统的设置不相符。
    #. print s.decode(FILE_ENCODING).encode('utf-8')
    #. print s.decode(CODING_ENCODING).encode('utf-8')
        将 s 以文件编码格式编码后在解码成 utf-8，随后打印就会输出正确的内容，而将 s
        以 `-*- coding:<encoding> -*-` 中声明的格式编码时，打印的却是错误的内容。这说明文件中的字符串 s 确实是按文件的编码格式编码。

为什么我说是错误的，Python 确不报错呢？我觉得这一点正是 Python 中编解码问题容易酿成大错的主要原因。

以文件 gbk-euc.py 为例。通过 Linux 命令 `xxd` 我们可以以二进制的形式查看文件。

.. code-block:: console

    0000000: 2320 2d2a 2d20 636f 6469 6e67 3a20 6575  # -*- coding: eu
    0000010: 632d 6a70 202d 2a2d 0a0a 696d 706f 7274  c-jp -*-..import
    0000020: 2063 6861 7264 6574 0a0a 0a69 6620 5f5f   chardet...if __
    0000030: 6e61 6d65 5f5f 203d 3d20 275f 5f6d 6169  name__ == '__mai
    0000040: 6e5f 5f27 3a0a 2020 2020 7320 3d20 27d6  n__':.    s = '.
    0000050: d0ce c427 0a20 2020 2070 7269 6e74 2073  ...'.    print s
    0000060: 2c20 6368 6172 6465 742e 6465 7465 6374  , chardet.detect
    0000070: 2873 290a 2020 2020 7472 793a 0a20 2020  (s).    try:.   
    0000080: 2020 2020 2070 7269 6e74 2073 2e64 6563       print s.dec
    0000090: 6f64 6528 2767 626b 2729 2e65 6e63 6f64  ode('gbk').encod
    00000a0: 6528 2775 7466 2d38 2729 0a20 2020 2065  e('utf-8').    e
    00000b0: 7863 6570 7420 556e 6963 6f64 6544 6563  xcept UnicodeDec
    00000c0: 6f64 6545 7272 6f72 2061 7320 653a 0a20  odeError as e:. 
    00000d0: 2020 2020 2020 2070 7269 6e74 2065 0a20         print e. 
    00000e0: 2020 2074 7279 3a0a 2020 2020 2020 2020     try:.        
    00000f0: 7072 696e 7420 732e 6465 636f 6465 2827  print s.decode('
    0000100: 6575 632d 6a70 2729 2e65 6e63 6f64 6528  euc-jp').encode(
    0000110: 2775 7466 2d38 2729 0a20 2020 2065 7863  'utf-8').    exc
    0000120: 6570 7420 556e 6963 6f64 6544 6563 6f64  ept UnicodeDecod
    0000130: 6545 7272 6f72 2061 7320 653a 0a20 2020  eError as e:.   
    0000140: 2020 2020 2070 7269 6e74 2065 0a              print e.

很容易找到字符 `中` 和 `文` ，被编码成 `d6 d0 ce c4` 。查看 `ECU wiki <https://en.wikipedia.org/wiki/Extended_Unix_Code>`_
上介绍的 ECU-JP 的编码规则，可以发现 `d6 d0 ce c4` 在 ECU-JP 中代表了两个合法的字符码， 对应的字符分别是： `嶄` 和 `鳴`
。既然如此，当 Python 按 ecu-jp 来解码字符串 s 时，自然不过报错，只不过错误的理解了其意义。

可以精心构造一个会报错的例子。

.. code-block:: python
    :caption: gbk-euc.py

    # -*- coding: euc-jp -*-

    import chardet


    if __name__ == '__main__':
        s = '相'
        print s, chardet.detect(s)
        try:
            print s.decode('gbk').encode('utf-8')
        except UnicodeDecodeError as e:
            print e
        try:
            print s.decode('euc-jp').encode('utf-8')
        except UnicodeDecodeError as e:
            print e

| 此时再执行

.. code-block:: console

    [root@iZ25012hd8kZ myblog]# python gbk-euc.py 
      File "gbk-euc.py", line 7
      SyntaxError: 'euc_jp' codec can't decode bytes in position 9-10: illegal multibyte sequence

一个猜想
++++++++

**我猜测** ：如果我们声明一个文件的编码格式为 utf-8 ，Python 在解析这个文件时会省略 :ref:`python_parse`
中提到的第二和第三步。

| 看如下这样的一个例子。

.. code-block:: python
    :caption: gbk-utf-8.py

    # -*- coding:utf-8 -*-

    import chardet


    if __name__ == '__main__':
        s = '中文'
        print s, chardet.detect(s)

| 执行

.. code-block:: console

    [root@iZ25012hd8kZ myblog]# python gbk-utf-8.py 
    אτ {'confidence': 0.99, 'encoding': 'GB2312'}

文件中的字符 `中` 和 `文` 被按 GBK 编码后保存在硬盘的内容是： `d6 d0 ce c4` 。而根据 `UTF-8 编码规则 <https://zh.wikipedia.org/wiki/UTF-8>`_
这几字节的内容是不合法的，所以程序应该会引发异常。而现在却没有，说明 Python 并没有将这个文件的内容转化为 Unicode。

| 更令我我好奇的是，当我讲文件修改如下：

.. code-block:: python
    :caption: gbk-utf8.py

    # -*- coding:utf8 -*-

    import chardet


    if __name__ == '__main__':
        s = '中文'
        print s, chardet.detect(s)

.. code-block:: console

    [root@iZ25012hd8kZ myblog]# python gbk-utf8.py 
      File "gbk-utf8.py", line 2
      SyntaxError: 'utf8' codec can't decode byte 0xd6 in position 0: invalid continuation byte

难道 Python 在解析源文件的时候没有将 utf-8 和 utf8 等价？

2015-12-28 补充
---------------

根据 Python Bug Tracker 上的 `issue25937 <http://bugs.python.org/issue25937>`_ 应该可以看出我的猜测是正确的。

    - 当通过 `coding:<encoding>` 声明文件的编码格式为 utf-8 是， :ref:`python_parse` 中的第二和第三步被省略了。
    - cpython 并没有把 utf-8 和 utf8 等价。

参考
----

#. `What's the difference between unicode and utf8? <http://stackoverflow.com/questions/3951722/whats-the-difference-between-unicode-and-utf8>`_
#. `Unicode HOWTO <https://docs.python.org/2/howto/unicode.html>`_
#. `PEP 0263 -- Defining Python Source Code Encodings <https://www.python.org/dev/peps/pep-0263/>`_
