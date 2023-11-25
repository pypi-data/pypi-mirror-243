import numpy as np

# ------------------------------ 基础、核心 ------------------------------ #
from sz.accelerate.cuda import CUDA
from sz.core.config import Config
from sz.core.tensor import Tensor
from sz.core.tensor import Parameter
from sz.functions.bf import Function
from sz.core.numericaldiff import NumericalDiff
# ------------------------------ 数据结构 ------------------------------ #
from sz.ds.queue import PriorityQueue
from sz.ds.stack import Stack
# ------------------------------ 函数方法 ------------------------------ #
from sz.functions.ft0 import sum_to, broadcast_to, sum, average, matmul, transpose, reshape, linear, get_item, get_item_grad
from sz.functions.ft0 import SumTo, BroadcastTo, Sum, MatMul, Transpose, Reshape, Linear, GetItem, GetItemGrad
from sz.functions.ft1 import setup_tensor
from sz.functions.ft1 import add, sub, mul, div, power, neg, mod
from sz.functions.ft1 import Add, Sub, Mul, Div, Power, Neg, Mod
from sz.functions.ft2 import sin, cos, tan, tanh
from sz.functions.ft2 import Sin, Cos, Tan, Tanh
from sz.functions.ft3 import exp, lg, ln
from sz.functions.ft3 import Exp, Lg, Ln
from sz.functions.ft4 import sigmoid, relu, softmax, log_softmax, leaky_relu, step
from sz.functions.ft4 import Sigmoid, ReLU, Softmax, LogSoftmax, LeakyReLU
from sz.functions.ft5 import mean_squared_error, softmax_cross_entropy, sigmoid_cross_entropy, binary_cross_entropy
from sz.functions.ft5 import MeanSquaredError, SoftmaxCrossEntropy
from sz.functions.ft6 import max, min, clip, batch_norm
from sz.functions.ft6 import Max, Min, Clip, BatchNorm
from sz.functions.ft7 import accuracy, dropout, embed_id
# ----------------------------- 层 ------------------------------ #
from sz.core.layer import Layer  # 层父类
from sz.layers.linear import Linear as LinearLayer  # 线性层
# ------------------------------ 模型 ------------------------------ #
from sz.core.model import Model  # 模型父类（继承Layer）
from sz.models.mlp import MLP  # 多层感知器模型
# ------------------------------ 优化器 ------------------------------ #
from sz.core.optimizer import Optimizer  # 优化器父类
from sz.optimizers.sgd import SGD, MomentumSGD, AdaGrad, AdaDelta, Adam  # 随机梯度下降、动量梯度下降、梯度下降法的改进、梯度下降法的改进、梯度下降法的改进

setup_tensor()


def is_tensor(obj):
    """
    判断对象是不是Tensor对象
    :param obj: 要判断的对象
    :return: True：是Tensor对象；False：不是Tensor对象
    """
    return isinstance(obj, Tensor)


def is_parameter(obj):
    """
    判断对象是不是Parameter对象
    :param obj: 要判断的对象
    :return: True：是Parameter对象；False：不是Parameter对象
    """
    return isinstance(obj, Parameter)


def as_nparray(obj):
    """
    将对象转化为numpy的数组
    为什么需要转化：
    x = np.array(0.5)
    y = np.array([0.5])
    x = x + 1
    y = y + 1
    print(np.isscalar(x))  # True
    print(np.isscalar(y))  # False
    ----------
    a = np.array(10)
    b = np.array([4])
    c = 10
    print(np.isscalar(a), np.isscalar(b), np.isscalar(c))  # False False True
    :param obj: 要转化的对象
    :return: 转化后的对象
    """
    if np.isscalar(obj):
        return np.array(obj)
    return obj


def to_tensor(obj):
    """
    将对象转化为Tensor对象
    :param obj: 要转化的对象
    :return: 转化后的对象
    """
    obj = as_nparray(obj)
    if not is_tensor(obj):
        obj = Tensor(obj)
    return obj


def clear_tensors(*tensors):
    for tensor in tensors:
        tensor.clear_tensor()


def clear_layers_tensors(*layers):
    for layer in layers:
        layer.clear_tensors()


def dropout_way(x, dropout_ratio=0.5):
    """ 权重衰减法 """
    mask = np.random.rand(*x.shape) > dropout_ratio
    scale = np.array(1.0 - dropout_ratio).astype(x.dtype)
    y = x * mask / scale
    return y
