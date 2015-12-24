python_function_argument
========================

.. author:: default
.. categories:: 技术
.. tags:: Python, 拾人牙慧
.. comments::

区分parameter与argument [1]_
----------------------------
简单的说，当函数定义的时候，参数名应该被称作parameter；
当函数被实际调用的时候，参数名应该被称作argument。
举例来说的话：

.. code-block:: python

    def func(boo, bar=None, **kwargs):
        pass

此时的boo，bar，**kwargs被称作parameter。

.. code-block:: python
    
    func(42, bar=314, extra=somevar)

当函数被调用，值41，314和somevar被称作argument。


两种argument [2]_
-----------------
再次重申：当你将一个值传递给一个函数时，我们称这个值为argument。
Python定义了两种类型的argument。
    - keyword argument
      an argument preceded by an identifier (e.g. name=) in a function call
      or passed as a value in a dictionary preceded by .
      举例来说：

.. code-block:: python

    complex(real=3, img=5)
    complex(**{'real': 3, 'img': 5})

    - positional argument
      搜有不是keyword argument的argument。
      positional argument可以直接出现在参数列表的前列，
      也可以be passed as elements of an iterable preceded by *。
需要注意的一点是：如果同时存在keyword argument和positional argument，
那么所有的positional argument必须在所有的keyword argument之前。

.. code-block:: python

    >>> complex(real=3,5) 
      File "<stdin>", line 1
    SyntaxError: non-keyword arg after keyword arg


四种parameter [3]_
------------------
Python划分了四种类型的paramter

    - positional-or-keyword
      调用函数时，parameter既可以当做positional argument来传递
      也可以当做keyword argument来传递
    - positional-only
      调用函数时，可以通过posiional argument来传递。
      Python并没有语法来支持positional-only parameter，
      但是在一些内置函数中，有使用positional-only parameter，
      比如说 `abs() <https://docs.python.org/2/library/functions.html#abs>`_
    - var-positional
      调用函数时，可以传递随意长度的postional argument来构造parameter。
    - var-keyword
      调用函数时，可以传递随意多个keyword argument来构造paramter。


调用函数式参数转化的顺序
------------------------
- a list of unfilled slots is created for the formal parameters
- If there are N positional arguments, they are placed in the first N slots
- for each keyword argument, the identifier is used to determine the corresponding slot
  + If the slot is already filled, a TypeError exception is raised.
  + Otherwise, the value of the argument is placed in the slot, filling it.
- When all arguments have been processed,
  the slots that are still unfilled are filled with the corresponding default value
  from the function definition. 
- If there are any unfilled slots for which no default value is specified,
  a TypeError exception is raised.

*\\** 操作符和 *\\*\\** 操作符
------------------------------
在Python中 *\\** 操作符可以用在两个地方
    - 在函数定义时，表明一个parameter是var-positional
    - 在函数调用时，unpacking一个iterable作为多个positional argument
同样， *\\*\\** 操作符也只能用在这两个地方
    - 在函数定义是，表明一个parameater是var-keyword
    - 在函数调用时，unpacking一个iterable作为多个keyword argument

.. [#] https://docs.python.org/2/faq/programming.html#faq-argument-vs-parameter
.. [#] https://docs.python.org/2/glossary.html#term-argument
.. [#] https://docs.python.org/2/glossary.html#term-parameter
.. [#] https://www.python.org/dev/peps/pep-0457/
