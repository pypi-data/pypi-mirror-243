# -*- coding: UTF-8 -*-

import os
import sys

quant1x_parent_path = __file__.split('quant1x')[0]
rootPath = os.path.abspath(quant1x_parent_path)
# print(rootPath)
sys.path.insert(0, rootPath)
# print(sys.path)