Cookie 的大小限制和字符限制
===========================


.. author:: default
.. categories:: 技术
.. tags:: 工作、问题
.. comments::


问题重现
--------

今天前端突然跑过来告诉我，登陆后的状态不能保持了。
排查了一下，基本可以确定是前端手动操作 cookie 出了问题，
导致 Django 不能从 cookie 中读取 session 有关的部分。

求道于 Mr.Google，猜测是前端向 cookie 里写入了太多东西，修改之后果然有效。

晚上空下来复查，却发现即使 cookie 长度超过了浏览器的长度，Python 也可以正确解析。
重现问题，发现应该是前端写 cookie 时写入了中文，白天是瞎猫撞上死耗子了。

Cookie 大小的限制
-----------------

浏览器对 cookie 大小的限制
++++++++++++++++++++++++++

虽然 `RFC 2965`_ 认为浏览器等 user agaent 不应该对 cookie 的大小和数量做限制，但是这毕竟是不现实的。
`RFC 2965`_ 在 `5.3 Implementation Limits`_ 中建议了浏览器应该支持的最低标准：

    - 至少支持 300 个 cookie
    - 每个 cookie 至少可以达到 4096 字节
    - 每个域名至少可以存储 20 个 cookie

需要注意，如果你希望你的网站在每个浏览器上可以正常运行的话，尽量不要去卡这个极限。
毕竟这不是一个强制性的要求，你可以通过 `这个网站 <http://browsercookielimits.squawky.net/>`_
做一些有趣的测试。

关于Django
++++++++++

在 `issue 22242 <https://code.djangoproject.com/ticket/22242>`_ 中提到了 cookie 的长度问题，
但是当你试图在 Django 中设置一个长度超过 4096 字节的 cookie 时，Django 并不会引发一个异常，
详见 `Django request <https://docs.djangoproject.com/en/1.9/ref/request-response/>`_ 。

我更好奇的时，如果 *request* 携带的 cookies 超过了 4096 长度，Django 会怎么处理。

| 于是，我尝试发了 cookies 大小超过 4096 字节的请求。

.. code-block:: python

    import requests
    >>> r = requests.get('http://nirvan.360.cn:8005/cookieOverFlow/', cookies={'A': 'a'*5000})
    >>> r
    <Response [200]>

| 此时，根据 log 很直接的可以看出：Python 还是能够正确解析。

.. code-block:: python

    [2015-12-14 23:19:38] INFO[audit.views:40] key: A; value length: 5000

| 所以白天的解决方法应该是瞎猫碰上了死耗子。

问题重现
--------

| 回过头，再来看前端相关的代码。当初写到 cookie 里面的东西，很明显可能存在中文。
  而前端又没做处理，所以我就开始猜测问题会不会出在这里。

.. code-block:: python

    import requests
    >>> cookies = {'A': 'a', 'B': '中文', 'C':'c', 'D': 'd'}
    >>> cookies
    {'A': 'a', 'C': 'c', 'B': '\xe4\xb8\xad\xe6\x96\x87', 'D': 'd'}
    >>> requests.get('http://nirvan.360.cn:8005/cookieOverFlow/', cookies=cookies)
    <Response [200]>

| 参见对应的 log，我们可以看见 Python 并不能正确解析 cookie 中的中文部分，
  并导致 cookie 随后的部分，也不能正确的被解析。

.. code-block:: python

    [2015-12-15 01:09:33] INFO[audit.views:40] key: A; value: a
    [2015-12-15 01:09:33] INFO[audit.views:40] key: C; value: c

溯源
----

StackOverFlow 上的 `这个回答 <http://stackoverflow.com/questions/1969232/allowed-characters-in-cookies>`_
很好的解释了为什么你不应该在 cookie 中写入非 ascii 字符。

| 具体到 Python，参见 `Lib/Cookie.py <https://hg.python.org/cpython/file/2.7/Lib/Cookie.py>`_ 中的相关正则表达式。


.. code-block:: python


    #
    # Pattern for finding cookie
    #
    # This used to be strict parsing based on the RFC2109 and RFC2068
    # specifications.  I have since discovered that MSIE 3.0x doesn't
    # follow the character rules outlined in those specs.  As a
    # result, the parsing rules here are less strict.
    #

    _LegalKeyChars  = r"\w\d!#%&'~_`><@,:/\$\*\+\-\.\^\|\)\(\?\}\{\="
    _LegalValueChars = _LegalKeyChars + r"\[\]"
    _CookiePattern = re.compile(
        r"(?x)"                       # This is a Verbose pattern
        r"\s*"                        # Optional whitespace at start of cookie
        r"(?P<key>"                   # Start of group 'key'
        "["+ _LegalKeyChars +"]+?"     # Any word of at least one letter, nongreedy
        r")"                          # End of group 'key'
        r"("                          # Optional group: there may not be a value.
        r"\s*=\s*"                    # Equal Sign
        r"(?P<val>"                   # Start of group 'val'
        r'"(?:[^\\"]|\\.)*"'            # Any doublequoted string
        r"|"                            # or
        r"\w{3},\s[\s\w\d-]{9,11}\s[\d:]{8}\sGMT" # Special case for "expires" attr
        r"|"                            # or
        "["+ _LegalValueChars +"]*"        # Any word or empty string
        r")"                          # End of group 'val'
        r")?"                         # End of optional value group
        r"\s*"                        # Any number of spaces.
        r"(\s+|;|$)"                  # Ending either at space, semicolon, or EOS.
        )

| 很明显， *_CookiePattern* 并不会匹配任何中文。
  当某个 *KEY* 对应的 *VALUE* 完全由中文组成是，经由 *_CookiePattern* 提取出的 *VALUE* 必然是一个空字符串。

嗯，找了一会没找到 Django 中具体解析 cookie 的地方在哪里，不过调用的也是 *Cookie.SimpleCookie* 。
TODO: 为什么存在中文后，Django 不接卸后续的 KEY=VALUE 对，这和我直接使用 *Cookie* 模块的结果不符。

.. _RFC 2965: http://www.ietf.org/rfc/rfc2965.txt
.. _5.3 Implementation Limits: http://www.ietf.org/rfc/rfc2965.txt
