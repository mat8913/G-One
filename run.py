#!/usr/bin/env python3
try:
 import g.one.main
except ImportError:
 import os, sys
 sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 import g.one.main

g.one.main.main()
