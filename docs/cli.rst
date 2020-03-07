Command Line Tool
=================

Lazylab ships with a very simple cli tool so you can use lazylab straight from your favorite the terminal.
You can use ``--help`` flag to see help page.

You can mostly do three things:

1. Deploy lab you want with ``deploy`` argument, for example:
``lazylab deploy test_all`` - wich will deploy lab named 'test_all'.

2. Delete lab you want with ``delete`` argument, for example:
``lazylab delete test_all`` - wich will delete lab named 'test_all'

3. Save lab you want with ``save`` and ``as`` arguments, for example:
``lazylab save test_all as test_all_v2`` - wich will save lab named 'test_all' as 'test_all_v2'


Debug
--------------------------

You can use:

- ``-v`` flag to get WARNING level logs

- ``-vv`` flag to get INFO level logs

- ``-vvv`` flag to get DEBUG level logs
