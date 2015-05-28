#!/usr/bin/env python3
try:
    import g.one.main
except ImportError:
    from os.path import dirname, abspath
    from sys import path
    path.append(dirname(dirname(abspath(__file__))))
    import g.one.main

g.one.main.main()
