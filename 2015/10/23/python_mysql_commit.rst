出人意料的 `SELECT`
===================

.. author:: default
.. categories:: 技术
.. tags:: Python, MySQL
.. comments::

问题重现
--------

首先打开一个窗口A，运行 MySQL 客户端，创建一张测试表，并插入一行数据。

.. code-block:: mysql

      mysql> CREATE TABLE `test_table` (
          -> `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
          -> `user_name` varchar(128) NOT NULL
          -> );
      Query OK, 0 rows affected (0.02 sec)

      mysql> INSERT INTO `test_table`(`user_name`) VALUES('user_01');
      Query OK, 1 row affected (0.00 sec)

随后，再打开一个窗口A，运行 Python Shell ，查询测试表中的数据。

.. code-block:: python

   >>> from contextlib import closing
   >>> import MySQLdb
   >>> conn = MySQLdb.connect(user='user', passwd='passwd', db='db')
   >>> with closing(conn.cursor()) as cur:
   ...     cur.execute('SELECT * FROM test_table')
   ...     id, user_name = cur.fetchone()
   ...     print 'id: {id}, user: {user}'.format(id=id, user=user_name)
   ...
   1L
   id: 1, user: user_01

回到窗口A，插入一行新值。

.. code-block:: mysql

   mysql> INSERT INTO `test_table`(`user_name`) VALUES('user_02');
   Query OK, 1 row affected (0.00 sec)

现在，来到最后一步：回到窗口B，查询现在测试表中的数据，出人意料的事情发生了：
Python 并没有查询到最新的数据！

.. code-block:: python

   >>> with closing(conn.cursor()) as cur:
   ...     cur.execute('SELECT * FROM test_table')
   ...     id, user_name = cur.fetchone()
   ...     print 'id: {id}, user: {user}'.format(id=id, user=user_name)
   ...
   1L
   id: 1, user: user_01

难道是刚才的 `INSERT` 没有生效？

.. code-block:: mysql

   mysql> SELECT * FROM `test_table`;
   +----+-----------+
   | id | user_name |
   +----+-----------+
   |  1 | user_01   |
   |  2 | user_02   |
   +----+-----------+
   2 rows in set (0.00 sec)

问题总结
--------
Shit！在 Python 中，查询到数据库数据竟然不是最新的？不是实时变化的？

问题原因
--------
直接的原因是
    + MySQL 默认的事务隔离级别是 **REPEATABLE READ** ，
      这意味着在同一个事务期间内读取的所有数据都来自同一个 snapshot ——建立在事务期间的第一次读操作。

    + Python 默认关闭自动提交(AUTOCOMMIT)模式，导致只有显示的调用 `COMMIT` 才会结束当前事务。
而出人意料的原因在于我不知道
    + 在 MySQL 中，如果不是显式的开始一个事务，
      则 **每个操作都被当作一个事务执行** 。

    + MySQL 默认打开自动提交模式。也就是说，如果不是显式地开始一个事务，
      MySQL 自动提交每个操作。

我们可以尝试关闭 MySQL 的自动提交模式，然后来验证上述几点。

.. code-block:: mysql

    # 窗口C                                     # 窗口D

    mysql> SELECT @@AUTOCOMMIT;                 mysql> SELECT @@AUTOCOMMIT;
    +--------------+                            +--------------+
    | @@AUTOCOMMIT |                            | @@AUTOCOMMIT |
    +--------------+                            +--------------+
    |            1 |                            |            1 |
    +--------------+                            +--------------+
    1 row in set (0.00 sec)                     1 row in set (0.00 sec)

    mysql> SET @@AUTOCOMMIT=0;                  mysql> SET @@AUTOCOMMIT=0;
    Query OK, 0 rows affected (0.01 sec)        Query OK, 0 rows affected (0.01 sec)

    mysql> SELECT COUNT(*) FROM test_table;
    +----------+
    | COUNT(*) |
    +----------+
    |        2 |
    +----------+
    1 row in set (0.00 sec)

                                                mysql> INSERT INTO test_table(user_name)
                                                    -> VALUES('user_03');
                                                Query OK, 1 row affected (0.00 sec)

    mysql> SELECT COUNT(*) FROM test_table;
    +----------+
    | COUNT(*) |
    +----------+
    |        2 |
    +----------+
    1 row in set (0.00 sec)

                                                mysql> COMMIT;
                                                Query OK, 0 rows affected (0.00 sec)

    mysql> SELECT COUNT(*) FROM test_table; 
    +----------+
    | COUNT(*) |
    +----------+
    |        2 |
    +----------+
    1 row in set (0.00 sec)

    mysql> COMMIT; 
    Query OK, 0 rows affected (0.00 sec)

    mysql> SELECT COUNT(*) FROM test_table; 
    +----------+
    | COUNT(*) |
    +----------+
    |        3 |
    +----------+
    1 row in set (0.00 sec)


追根溯源 [#]_
-------------
事务
++++
事务就是一组原子性的SQL查询，或者说一个独立的工作单元。
一个运行良好的事务处理系统，应该支持ACID这四个特性。

.. glossary::

    *原子性 (atomicity)*
        一个事务必须被视为一个不可分割的最小工作单元，整个事务中的所有操作要么全部提交成功，要么全部失败回滚，
        对于一个事务来说，不可能只执行其中的一部分操作，这就是事务。

    *一致性 (consistency)*
        数据库总是从一个一致性的状态转换到另外一个一致性的状态。

    *隔离性 (isolation)*
        通常来说，一个事务所做的修改在最终提交以前，对其他事务是不可见的。

    *持久性 (durability)*
        一旦事务提交，则其所做的修改就会永久的保存到数据库中。

隔离级别
++++++++
在 SQL 标准中定义了四种隔离级别，每一种隔离级别都规定了在一个事务中所做的修改，哪些是在事务内和事务间可见的，哪些是不可见的。
较低级别的隔离通常可以执行更高的并发，系统的开销也更低。

首先介绍一下不同隔离级别中可能会出现的3种问题。

.. glossary::

    *脏读*
        事务可以读取未提交的数据。

    *不可重复读*
        两次执行同样的查询，可能得到不同的结果。

    *幻读*
        当某个事务在读取某个范围内的记录时，另外一个事务又在该范围内插入了新的记录，
        当之前的事务再次读取该范围的记录时，会产生幻行。

四种隔离级别

.. glossary::

    *Read Uncommitted*
        在 Read Uncommitted 中，事务中的修改，即使没有提交，对其他事务也都是可见的。

    *Read Committed*
        在 Read Committed 中，一个事务从开始到提交之前，所做的修改对其他事务是不可见的。

    *Repetable Read*
        Repetable Read 保证了在同一个事务中多次读取的记录结果是一致的。

    *Serializable*
        Serializable 强制事务串行执行。

以及四种隔离级别中可能出现的问题

+-----------------+-------------+------------------+-------------+
|隔离级别         |脏读可能性   |不可重复读可能性  | 幻读可能性  |
+-----------------+-------------+------------------+-------------+
|Read Uncommitted |Yes          |Yes               |Yes          |
+-----------------+-------------+------------------+-------------+
|Read Committed   |No           |Yes               |Yes          |
+-----------------+-------------+------------------+-------------+
|Repetable Read   |No           |No                |Yes [#]_     |
+-----------------+-------------+------------------+-------------+
|Serializable     |No           |No                |No           |
+-----------------+-------------+------------------+-------------+

|

|

|

.. [#] 大部分内容摘抄自 <<高性能MySQL>> 。
.. [#] InnoDB 通过 `MVCC <https://dev.mysql.com/doc/refman/5.0/en/innodb-multi-versioning.html>`_ 来避免幻读的可能性。
