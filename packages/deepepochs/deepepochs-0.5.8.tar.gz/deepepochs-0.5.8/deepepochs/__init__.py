"""
@author: hitlic
TODO:
    - 在Notebook中启动Accelerate程序
"""
__version__ = '0.5.8'

from .loops import *
from .trainer import Trainer, TrainerBase, EpochTask
from .tools import *
from .callbacks import *
from .optimizer import Optimizer, Optimizers
from .patches import PatchBase, ValuePatch, TensorPatch, MeanPatch, ConfusionPatch
