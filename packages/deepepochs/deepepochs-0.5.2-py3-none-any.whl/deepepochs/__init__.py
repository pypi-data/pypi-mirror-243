"""
@author: hitlic
TODO:
    - Accelerate下利用tensorboard日志记录指标
    - 在Notebook中启动Accelerate程序
    - 混合精度训练测试
"""
__version__ = '0.5.2'

from .loops import *
from .trainer import Trainer, TrainerBase, EpochTask
from .tools import *
from .callbacks import *
from .optimizer import Optimizer, Optimizers
from .patches import PatchBase, ValuePatch, TensorPatch, MeanPatch, ConfusionPatch
