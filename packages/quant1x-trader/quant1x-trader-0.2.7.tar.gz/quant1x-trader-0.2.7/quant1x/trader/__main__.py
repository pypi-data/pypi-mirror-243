# -*- coding: UTF-8 -*-

import os
import sys


quant1x_parent_path = __file__.split('quant1x')[0]
rootPath = os.path.abspath(quant1x_parent_path)
sys.path.insert(0, rootPath)

from quant1x.trader.auto import auto_trader


if __name__ == '__main__':
    sys.exit(auto_trader())
