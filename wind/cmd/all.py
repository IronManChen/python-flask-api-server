#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

import os
import sys
from wind.base.server import run


possible_topdir = os.path.normpath(os.path.join(os.path.abspath(__file__),
                                 os.pardir,
                                 os.pardir,
                                 os.pardir))
if os.path.exists(os.path.join(possible_topdir,
                              "wind"
                              "__init__.py")):
   sys.path.insert(0, possible_topdir)

def main():
   run(possible_topdir)
