import numpy as np

from sz.accelerate.cuda import CUDA
from sz.core.tensor import Tensor
from sz.functions import log_sum_exp
from sz.functions.bf import Function
from sz.functions.ft0 import sum
from sz.functions.ft3 import ln
from sz.functions.ft4 import sigmoid, softmax
from sz.functions.ft6 import clip

"""
函数类型5：损失函数
均方误差[mean_squared_error]、交叉熵损失[softmax_cross_entropy]、交叉熵损失[sigmoid_cross_entropy]、二元交叉熵[binary_cross_entropy]
"""


def mean_squared_error(x0, x1):
    """
    简单实现：
    x0, x1 = Tensor(x0), Tensor(x1)
    diff = x0 - x1
    y = sum(diff ** 2) / len(diff)
    return y
    """
    return MeanSquaredError()(x0, x1)


def softmax_cross_entropy(x, t):
    """
    简单实现
    x, t = Tensor(x), Tensor(t)
    N = x.shape[0]
    p = softmax(x)
    p = clip(p, 1e-15, 1.0)  # 避免log(0)
    log_p = log(p)
    tlog_p = log_p[np.arange(N), t.data]
    y = -1 * sum(tlog_p) / N
    return y
    """
    return SoftmaxCrossEntropy()(x, t)


def sigmoid_cross_entropy(x, t):
    if x.ndim != t.ndim:
        t = t.reshape(*x.shape)
    x, t = (x if isinstance(x, Tensor) else Tensor(x)), (t if isinstance(t, Tensor) else Tensor(t))
    N = len(x)
    p = sigmoid(x)
    p = clip(p, 1e-15, 1.0)
    tlog_p = t * ln(p) + (1 - t) * ln(1 - p)
    y = -1 * sum(tlog_p) / N
    return y


def binary_cross_entropy(p, t):
    if p.ndim != t.ndim:
        t = t.reshape(*p.shape)
    N = len(t)
    p = clip(p, 1e-15, 0.999)
    tlog_p = t * ln(p) + (1 - t) * ln(1 - p)
    y = -1 * sum(tlog_p) / N
    return y


class MeanSquaredError(Function):
    """
    mean_squared_error
    """

    def forward(self, x0, x1):
        """
        mean_squared_error的正向传播
        :param x0: 参数x0
        :param x1: 参数x1
        :return: mean_squared_error函数的计算结果
        """
        diff = x0 - x1
        y = (diff ** 2).sum() / len(diff)
        return y

    def backward(self, gy):
        """
        mean_squared_error的反向传播
        :param gy: 导数值
        :return: mean_squared_error函数的的反向传播的值
        """
        x0, x1 = self.inputs
        diff = x0 - x1
        gx0 = gy * diff * (2. / len(diff))
        gx1 = -gx0
        return gx0, gx1


class SoftmaxCrossEntropy(Function):
    """
    softmax_cross_entropy
    """

    def forward(self, x, t):
        """
        softmax_cross_entropy的正向传播
        :param x: 参数x
        :param t: 参数t
        :return: softmax_cross_entropy函数的计算结果
        """
        xp = CUDA.to_gpu()
        N = x.shape[0]
        log_z = log_sum_exp(xp, x, axis=1)
        log_p = x - log_z
        log_p = log_p[np.arange(N), t.ravel()]
        y = -log_p.sum() / np.float32(N)
        return y

    def backward(self, gy):
        """
        softmax_cross_entropy的反向传播
        :param gy: 导数值
        :return: softmax_cross_entropy函数的的反向传播的值
        """
        x, t = self.inputs
        N, CLS_NUM = x.shape
        gy *= 1 / N
        y = softmax(x)
        xp = CUDA.to_gpu()
        t_onehot = xp.eye(CLS_NUM, dtype=t.dtype)[t.data]
        y = (y - t_onehot) * gy
        return y
