Python Variable Scope
=====================

.. author:: default
.. categories:: 技术
.. tags:: Python, 拾人牙慧
.. comments::

LEGB
----

`Learning Pythong <http://shop.oreilly.com/product/0636920028154.do>`_ 中将
Python 变量的作用域划分为四个级别：LEGB。

    - Location. Names assigned in any way within a function (def or lambda),
      and not declared global in that function.
    - Enclosing function locals. Name in the local scope of any and all 
      enclosing functions (def or lambda), from inner to outer.
    - Global(module). Names assigned at the top-level of a module file,
      or declared global in a def within the file.
    - Built-in(Python). Names preassigned in th built-in names modul.

举个具体的例子的话，就是这样的。

.. code-block:: python

    >>> gloabl_var = "I'm gloable"
    >>> def outer_func():
    ...     enclosing_var = "I'm enclosing"
    ...     def inner_func():
    ...         local_var = "I'm local"
    ...
    >>> sys # It's bulit-in

需要注意的 LEGB 针对的是 **变量** ，并不包括属性。

对于一个变量我们可以“读”，也可以“写”（创建，修改，删除）。

- 对于“读”，Python遵循这样的规则：

    | 对于一个具体的变量，按如下顺序来搜索变量名
    |    local namespace --> enclosing namespace --> global namespace --> built-in namnsapce
    | 如果在所有的namespace中都找不到，那么就会导致 *NameError* 。

- 对于“写”，Python遵循这样的规则：

    | 在“写”变量的时候，总是创建一个新的本地变量。

所以，我们可以在函数内部读一个global变量。

.. code-block:: python

    >>> x = 'global_var'
    >>> def func():
    ...     print x
    ...
    >>> func()
    ... global_var

当然，首先被搜索的会是local namespace。

.. code-block:: python

    >>> x = 'global_var' 
    >>> def func(): 
    ...     x = 'local_var' 
    ...     print x 
    ...  
    >>> func() 
    local_var

同时，我们在函数内部也不能够修改global变量

.. code-block:: python

    >>> x = 'global_var' 
    >>> def func(): 
    ...     x = 'local_var' 
    ...     print x 
    ...  
    >>> func() 
    local_var
    >>> print x 
    global_var

有一点需要注意的是：Python的数据分mutable和immutable，我们在函数内不能修改的是
immutable+global，而mutable+global是可以被修改。

.. code-block:: python

    >>> a = [0, 1, 2] 
    >>> def func(): 
    ...     a[0] = 2 
    ...  
    >>> func() 
    >>> print a 
    [2, 1, 2]

具体的原因在这儿暂时不说，免得离题一万里 :)。

*global* & *nonlocal*
---------------------
| Python用关键字 *global* 来声明一个变量是global。
| Python用关键字 *nonlocal* 来声明一个变量既不是global也不是local，而是enclosing。

    | 不过 *nonlocal* 这个关键字是在Python 3中才加入的，所以不能在Python 2中使用。

当使用了 *global* 或者 *nonlocal* 我们就可以在函数内
对global变量或者enclosing变量进行修改了。

.. code-block:: python

    >>> x = 'global_var' 
    >>> def func(): 
    ...     global x 
    ...     x = 'modify in func' 
    ...  
    >>> func() 
    >>> print x 
    modify in func

奇怪的行为
----------
如果不使用关键字 *global* ，我们可以在函数在访问全局变量，
但是不能修改。但是如果我这么做了呢？于是我进行了一下的尝试。

.. code-block:: python

    >>> x = 'global_var' 
    >>> def func(): 
    ...     print x 
    ...     x = 'modify' 
    ...  
    >>> func() 
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in func
    UnboundLocalError: local variable 'x' referenced before assignment

令人惊奇的是，居然导致了一个 *UnboundLocalError* 。
官方解释是：当你在某个作用域中给一个变量赋值时，Python会在当前作用域创建这个变量，
随后任何outer作用域中的同名变量就不在可以访问了 [3]_。

不过我还是很好奇：Python会预先知道有赋值这个操作？怎么知道的？没有找到答案，先TODO！

.. [#] http://stackoverflow.com/questions/291978/short-description-of-python-scoping-rules
.. [#] http://sebastianraschka.com/Articles/2014_python_scope_and_namespaces.html#solutions
.. [#] https://docs.python.org/2.7/faq/programming.html#what-are-the-rules-for-local-and-global-variables-in-python
