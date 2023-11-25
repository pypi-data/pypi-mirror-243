import numpy as np

from sz.accelerate.cuda import CUDA
from sz.core.tensor import Tensor
from sz.core.config import Config

"""
函数类型5：其它函数2
准确度[accuracy]、退出[dropout]、嵌入ID[embed_id]
"""


def accuracy(y, t):
    """
    不可微
    """
    y, t = (y if isinstance(y, Tensor) else Tensor(y)), (t if isinstance(t, Tensor) else Tensor(t))
    _y = y.data.argmax(axis=1)
    _t = t.data.argmax(axis=1)
    return np.sum(_y == _t) / float(_y.shape[0])


def dropout(x, dropout_ratio=0.5):
    if not isinstance(x, Tensor):
        x = Tensor(x)
    if Config.TRAIN:
        xp = CUDA.to_gpu()
        mask = xp.random.rand(*x.shape) > dropout_ratio
        scale = xp.array(1.0 - dropout_ratio).astype(x.dtype)
        y = x * mask / scale
        return y
    else:
        return x


def embed_id(x, W):
    return W[x]
