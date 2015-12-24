Python 装饰器
=============


.. author:: default
.. categories:: 技术
.. tags:: Python
.. comments::


前言
----
之前一直不知道正式的写点东西的意义何在，直到我写完 `出人意料的SELECT </2015/10/23/python_mysql_commit.html>`_ 
和这一篇文章，突然明白写出来对我的意义何在。 **一种压力，一种确保正确的压力。**
不管是在总结平常工作上遇到的问题还是归类一些知识的知识，因为可能会被人看到，
而产生的一种压力去驱使我去确保说出来的内容都是正确。而在这个确保正确的过程中，我或发现了一些自以为是的错误，
或对原有知识有了一个更深的理解。

我会尽量在这儿写两类文章：

- 记录工作中的遇到的有意义的错误及其原因和解决方案
- 总结(摘抄？)某个方面的知识


装饰器
------
官方对装饰器的解释是
    一种特殊的 Python 语法，允许我们在不修改函数、方法的定义代码的情况下动态的修改函数、方法的功能。

Python 中的装饰器和函数式编程部分是我日常使用中最喜欢的部分。在使用它的过程中，我经常会困惑与以下几点。

装饰器的等效语句
++++++++++++++++
刚刚接触装饰器的时候，我一直好奇装饰器的功能是怎么实现的？
当我明白了怎么不用装饰器来实现装饰器的功能的时候，
我也就真的明白了装饰器真的只是一种特殊的 Python 语法。

所以来看两段等效的代码。

-  装饰器不带参数

.. code-block:: python

    @dec                                           def func(arg1, arg2):
    def func(arg1, arg2):                              pass
        pass                                       func = dec(func)

-  装饰器带参数

.. code-block:: python

   @dec_args(d_arg1, d_arg2):                      def func(arg1, arg2):
   def func(arg1, arg2):                               pass
       pass                                        func = dec_args(d_arg1, d_arg2)(func)

对于第二段代码中的 `dec_args(d_arg1, d_arg2)(func)` ，也许会令人产生一点困惑。
首先 `dec_args(d_arg1, d_arg2)` 会首先被执行并返回一个可调用对象，
然后 `func` 被当做参数传递给这个可调用对象。
如果 `dec_args(d_arg1, d_arg2)` 返回的不是一个可调用对象，
那么 Python 就会抛出异常 `TypeError`

多个装饰器的执行顺序
++++++++++++++++++++
当同时有多个装饰器被使用时，执行顺寻 **自上至下** 。

.. code-block:: python

    @dec1
    @dec2
    def func():
        pass

等效于

.. code-block:: python

    def func():
        pass
    func = dec1(dec2(func))

`functools.wraps` 的作用
++++++++++++++++++++++++

首先来看，如果不使用 `functools.wraps` 会怎么样。

.. code-block:: python

    >>> def dec(func): 
    ...     def wrapper(*args, **kwargs): 
    ...         '''this is wrapper''' 
    ...         return func(*args, **kwargs) 
    ...     return wrapper 
    ...  
    >>> @dec 
    ... def func(): 
    ...     '''this is func''' 
    ...     pass 
    ...  
    >>> func.__name__ 
    'wrapper'
    >>> func.__doc__ 
    'this is wrapper'

当未使用 `functools.wraps` 或者等效的方法，那么被装饰后的函数的
`__module__` , `__name__` , `__doc__` , `__dict__` 这四个属性反射的就是装饰器的对应
属性，而不是原函数的对应属性，这显然不是我们需要的。

`functools.wraps` 是怎么实现这种效果的，
请参看 `<https://docs.python.org/2/library/functools.html>`_ 。

脑洞时刻
++++++++

写着写着我突然好奇：装饰器是什么时候起作用的呢？是在函数定义时，还是在函数调用时呢？
我猜是再调用时，压一根辣条。

.. code-block:: python

    >>> def dec(func): 
    ...     @functools.wraps(func) 
    ...     def wrapper(*args, **kwargs): 
    ...         print 'lose' 
    ...         return func(*args, **kwargs) 
    ...     return wrapper 
    ...  
    >>> @dec 
    ... def func(): 
    ...     pass 
    ...  
    >>> def dec(func): 
    ...     @functools.wraps(func) 
    ...     def wrapper(*args, **kwargs): 
    ...         print 'win' 
    ...         return func(*args, **kwargs) 
    ...     return wrapper 
    ...  
    >>> func() 
    lose

一个实例
++++++++
参阅 Django 实现的 `lru_cache <https://github.com/django/django/blob/master/django/utils/lru_cache.py>`_ 。
