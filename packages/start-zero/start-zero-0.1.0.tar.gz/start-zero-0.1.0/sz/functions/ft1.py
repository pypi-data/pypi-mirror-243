import numpy as np

from sz.core.tensor import Tensor
from sz.functions.bf import Function
from sz.functions.ft0 import sum_to


def setup_tensor():
    Tensor.__add__ = add
    Tensor.__radd__ = add
    Tensor.__sub__ = sub
    Tensor.__rsub__ = rsub
    Tensor.__mul__ = mul
    Tensor.__rmul__ = rmul
    Tensor.__truediv__ = div
    Tensor.__rtruediv__ = rdiv
    Tensor.__pow__ = power
    Tensor.__neg__ = neg
    Tensor.__mod__ = mod
    Tensor.__rmod__ = rmod


"""
函数类型1：基本函数
加[+]、减[-]、乘[*]、除[/]、幂[**]、负数[-]、模[%]
"""


def add(x0, x1):
    return Add()(x0, x1)


def sub(x0, x1):
    return Sub()(x0, x1)


def rsub(x0, x1):
    return Sub()(x1, x0)


def mul(x0, x1):
    return Mul()(x0, x1)


def rmul(x0, x1):
    return Mul()(x0, x1)


def div(x0, x1):
    return Div()(x0, x1)


def rdiv(x0, x1):
    return Div()(x1, x0)


def power(x, c):
    return Power(c)(x)


def neg(x):
    return Neg()(x)


def mod(x0, x1):
    return Mod()(x0, x1)


def rmod(x0, x1):
    return Mod()(x1, x0)


class Add(Function):
    """
    加法类
    """

    def __init__(self):
        """
        初始化
        """
        self.x0_shape = None
        self.x1_shape = None

    def forward(self, x0, x1):
        """
        加法的正向传播
        :param x0: 加法的一个值
        :param x1: 加法的另一个值
        :return: 一个值与另一个值相加的结果
        """
        return x0 + x1

    def backward(self, gy):
        """
        加法的反向传播
        :param gy: 导数值
        :return: 加法反向传播的值
        """
        gx0, gx1 = gy, gy
        # 为了处理如数组(2,3)反向传播更新梯度为(1,3)之类的情况
        if self.x0_shape != self.x1_shape:
            gx0 = sum_to(gx0, self.x0_shape)
            gx1 = sum_to(gx1, self.x1_shape)
        return gx0, gx1


class Sub(Function):
    """
    减法类
    """

    def __init__(self):
        self.x0_shape = None
        self.x1_shape = None

    def forward(self, x0, x1):
        """
        减法的正向传播
        :param x0: 被减数
        :param x1: 减数
        :return: 差值
        """
        return x0 - x1

    def backward(self, gy):
        """
        减法的反向传播
        :param gy: 导数值
        :return: 减法反向传播的值
        """
        gx0, gx1 = gy, -gy
        # 为了处理如数组(2,3)反向传播更新梯度为(1,3)之类的情况
        if self.x0_shape != self.x1_shape:
            gx0 = sum_to(gx0, self.x0_shape)
            gx1 = sum_to(gx1, self.x1_shape)
        return gx0, gx1


class Mul(Function):
    """
    乘法类
    """

    def forward(self, x0, x1):
        """
        乘法的正向传播
        :param x0: 一个乘数
        :param x1: 另一个乘数
        :return: 乘积值
        """
        return x0 * x1

    def backward(self, gy):
        """
        乘法的反向传播
        :param gy: 导数值
        :return: 乘法反向传播的值
        """
        x0, x1 = self.inputs
        gx0, gx1 = gy * x1, gy * x0
        # 为了处理如数组(2,3)反向传播更新梯度为(1,3)之类的情况
        if x0.shape != x1.shape:
            gx0 = sum_to(gx0, x0.shape)
            gx1 = sum_to(gx1, x1.shape)
        return gx0, gx1


class Div(Function):
    """
    除法类
    """

    def forward(self, x0, x1):
        """
        除法的正向传播
        :param x0: 被除数
        :param x1: 除数
        :return: 相除的结果
        """
        return x0 / x1

    def backward(self, gy):
        """
        除法的反向传播
        :param gy: 导数值
        :return: 除法反向传播的值
        """
        x0, x1 = self.inputs
        gx0, gx1 = gy / x1, gy * (-x0 / x1 ** 2)
        # 为了处理如数组(2,3)反向传播更新梯度为(1,3)之类的情况
        if x0.shape != x1.shape:
            gx0 = sum_to(gx0, x0.shape)
            gx1 = sum_to(gx1, x1.shape)
        return gx0, gx1


class Power(Function):
    """
    幂类
    """

    def __init__(self, c):
        """
        初始化
        :param c: 常数
        """
        self.c = c

    def forward(self, x):
        """
        幂的正向传播
        :param x: 底数
        :return: 幂值
        """
        """ 异常处理：Integers to negative integer powers are not allowed """
        if (x.dtype == 'int32') and (self.c < 0):
            x = np.array(x, dtype=np.float32)
        return x ** self.c

    def backward(self, gy):
        """
        幂的反向传播
        :param gy: 导数值
        :return: 幂反向传播的值
        """
        x = self.inputs[0]
        c = self.c
        gx = c * (x ** (c - 1)) * gy
        return gx


class Neg(Function):
    """
    负数类
    """

    def forward(self, x):
        """
        负数的正向传播
        :param x: 需要变负的数
        :return: 负值
        """
        return -x

    def backward(self, gy):
        """
        负数的反向传播
        :param gy: 导数值
        :return: 负数反向传播的值
        """
        return -gy


class Mod(Function):
    """
    模类
    """

    def forward(self, x0, x1):
        """
        减法的正向传播
        :param x0: 被取模数
        :param x1: 模数
        :return: 模值
        """
        return x0 % x1

    def backward(self, gy):
        """
        模的反向传播
        简单参考：
        x = 17
        c = 12
        while x > c:
            x = x - c
        print(x, x%c)  # 5 5
        :param gy: 导数值
        :return: 模反向传播的值
        """
        return gy, 0
