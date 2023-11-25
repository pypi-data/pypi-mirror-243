from sz.accelerate.cuda import CUDA
from sz.functions import log_sum_exp
from sz.functions.bf import Function
from sz.functions.ft3 import exp

"""
函数类型4：激活函数
S型生长曲线[sigmoid]、线性整流函数[relu]、归一化指数函数[softmax]、归一化指数函数[log_softmax]、线性整流函数[leaky_relu]、阶跃函数[step]
"""


def sigmoid(x):
    return Sigmoid()(x)


def relu(x):
    return ReLU()(x)


def softmax(x, axis=1):
    """
    简单实现：
    x = as_variable(x)
    y = exp(x)
    sum_y = sum(y, axis=axis, keepdims=True)
    return y / sum_y
    """
    return Softmax(axis)(x)


def log_softmax(x, axis=1):
    return LogSoftmax(axis)(x)


def leaky_relu(x, slope=0.2):
    return LeakyReLU(slope)(x)


def step(x):
    y = x > 0
    return y.astype(int)


class Sigmoid(Function):
    """
    sigmoid
    """

    def forward(self, x):
        """
        sigmoid的正向传播
        :param x: 参数x
        :return: sigmoid函数的计算结果
        """
        xp = CUDA.to_gpu()
        # y = 1 / (1 + xp.exp(-x))
        y = xp.tanh(x * 0.5) * 0.5 + 0.5  # 更好的实现方式
        return y

    def backward(self, gy):
        """
        sigmoid的反向传播
        :param gy: 导数值
        :return: sigmoid函数的的反向传播的值
        """
        y = self.outputs[0]()
        # 为什么sigmoid(y1)的导数反而是(1-y2)*y2？因为sigmoid(y1)的导数等于sigmoid(y1)*(1-sigmoid(y1))，而y2=sigmoid(y1)，所以替换后就是(1-y2)*y2
        gx = gy * y * (1 - y)
        return gx


class ReLU(Function):
    """
    ReLU
    """

    def forward(self, x):
        """
        ReLU的正向传播
        :param x: 参数x
        :return: ReLU函数的计算结果
        """
        xp = CUDA.to_gpu()
        y = xp.maximum(x, 0.0)
        return y

    def backward(self, gy):
        """
        ReLU的反向传播
        :param gy: 导数值
        :return: ReLU函数的的反向传播的值
        """
        x, = self.inputs
        mask = x.data > 0
        # mask：True=1、False=0
        gx = gy * mask
        return gx


class Softmax(Function):
    """
    softmax
    """

    def __init__(self, axis=1):
        """
        初始化
        :param axis: 参数axis
        """
        self.axis = axis

    def forward(self, x):
        """
        softmax的正向传播
        :param x: 参数x
        :return: Softmax函数的计算结果
        """
        xp = CUDA.to_gpu()
        y = x - x.max(axis=self.axis, keepdims=True)
        y = xp.exp(y)
        y /= y.sum(axis=self.axis, keepdims=True)
        return y

    def backward(self, gy):
        """
        softmax的反向传播
        :param gy: 导数值
        :return: softmax函数的的反向传播的值
        """
        y = self.outputs[0]()
        gx = y * gy
        sum_dx = gx.sum(axis=self.axis, keepdims=True)
        gx -= y * sum_dx
        return gx


class LogSoftmax(Function):
    """
    log_softmax
    """

    def __init__(self, axis=1):
        """
        初始化
        :param axis: 参数axis
        """
        self.axis = axis

    def forward(self, x):
        """
        log_softmax的正向传播
        :param x: 参数x
        :return: log_softmax函数的计算结果
        """
        xp = CUDA.to_gpu()
        log_z = log_sum_exp(xp, x, self.axis)
        y = x - log_z
        return y

    def backward(self, gy):
        """
        log_softmax的反向传播
        :param gy: 导数值
        :return: log_softmax函数的的反向传播的值
        """
        y = self.outputs[0]()
        gx = gy - exp(y) * gy.sum(axis=self.axis, keepdims=True)
        return gx


class LeakyReLU(Function):
    """
    leaky_relu
    """

    def __init__(self, slope):
        """
        初始化
        :param slope: 参数slope
        """
        self.slope = slope

    def forward(self, x):
        """
        leaky_relu的正向传播
        :param x: 参数x
        :return: leaky_relu函数的计算结果
        """
        y = x.copy()
        y[x <= 0] *= self.slope
        return y

    def backward(self, gy):
        """
        leaky_relu的反向传播
        :param gy: 导数值
        :return: leaky_relu函数的的反向传播的值
        """
        x, = self.inputs
        mask = (x.data > 0).astype(gy.dtype)
        mask[mask <= 0] = self.slope
        gx = gy * mask
        return gx
