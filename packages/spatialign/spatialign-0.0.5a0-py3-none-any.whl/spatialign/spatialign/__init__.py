#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/12/23 9:50 AM
# @Author  : zhangchao
# @File    : __init__.py.py
# @Email   : zhangchao5@genomics.cn
from .model import DGIAlignment
from .trainer import Spatialign

import torch
import numpy as np
import random

seed = 42

torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
np.random.seed(seed)
random.seed(seed)

