import numpy as np
from sz.core.config import Config

from sz.accelerate.cuda import CUDA
from sz.functions import reshape_sum_backward
from sz.functions.bf import Function

"""
函数类型0：辅助函数
合并求和[sum_to]、广播[broadcast_to]、求和[sum]、平均数[average]、矩阵相乘[matmul]、矩阵转置[transpose]、重塑形状[reshape]、线性回归[linear]、切片[get_item]、切片（梯度）[get_item_grad]
"""


def sum_to(x, shape):
    if x.shape == shape:
        return x
    return SumTo(shape)(x)


def broadcast_to(x, shape):
    if x.shape == shape:
        return x
    return BroadcastTo(shape)(x)


def sum(x, axis=None, keepdims=False):
    return Sum(axis, keepdims)(x)


def average(x, axis=None, keepdims=False):
    y = sum(x, axis, keepdims)
    return y * (y.size / x.size)


def matmul(x0, x1):
    return MatMul()(x0, x1)


def transpose(x, axes=None):
    return Transpose(axes)(x)


def reshape(x, shape):
    return Reshape(shape)(x)


def linear(x, W, b=None):
    return Linear()(x, W, b)


def get_item(x, slices):
    return GetItem(slices)(x)


def get_item_grad(x, slices, in_shape):
    return GetItemGrad(slices, in_shape)(x)


class SumTo(Function):
    """
    合并求和
    """

    def __init__(self, to_shape: tuple):
        """
        初始化
        :param to_shape: 合并求和后的数组形状
        """
        self.to_shape = to_shape  # 合并求和后的数组形状
        self.from_shape = None  # 待合并求和的数组形状

    def forward(self, x):
        """
        合并求和的正向传播
        :param x: 待合并求和的值
        """
        self.from_shape = x.shape  # 待合并求和的数组形状
        ndim = len(self.to_shape)  # 合并求和后的数组长度
        lead = x.ndim - ndim  # 待合并求和的数组长度与合并求和后的数组长度差，如(1, 5, 3, 4)->(1, 1)，则差为2
        lead_axis = tuple(range(lead))  # 创造差值的元祖，如差为2，则差值元祖为：(0, 1)；如果差<=0，则差值元祖为：()
        """
        这是一个用于定位下标的编程技巧，参考：
        temp = ["a", "b", "c", "d"]
        out = tuple([index for index, value in enumerate(temp) if (value == 'a' or value == 'd')])
        print(out)  # (0, 3)
        为什么要筛出value==1？因为只有求和归一的维度才需要合并，比如(4, 4)，只有(1, 4)、(1, 1)、(4, 1)合并求和才有意义
        参考：
        x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])  # x：(4, 3)
        print(x.sum((0, 1), keepdims=True))  # (1, 1)
        print(x.sum((0, ), keepdims=True))  # (1, 3)
        print(x.sum((1, ), keepdims=True))  # (4, 1)
        # print(x.sum((0, 1, 2), keepdims=True))  # 报错
        # print(x.sum((2, 2), keepdims=True))  # 报错
        对(1, 1)来说，两个值都是1，因此下标0和1都要被选中；对(1, 3)来说，只有下标为0的才会被选中
        """
        axis = tuple([index + lead for index, value in enumerate(self.to_shape) if value == 1])
        """
        (1, 5, 3, 4)->(1, 1)会先扩充为(0, 1, 1, 1)
        (0, 1, 1, 1)其中前2位(0, 1)来自lead_axis，后2位来自axis
        lead_axis+axis的处理参考元祖相加：(1, 2) + (3, 4) = (1, 2, 3, 4)
        转换成(0, 1, 1, 1)后就可以调用numpy.sum函数了，至于为什么要转换成类似(0, 1, 2, 3)形式，感兴趣的可以研究下[numpy.sum]函数说明
        """
        y = x.sum(lead_axis + axis, keepdims=True)
        if lead > 0:
            """
            如(1, 5, 3, 4)->(1, 1)，会先扩充为(0, 1, 1, 1)，但是实际只要(1, 1)，因此需要移除扩充的维度，感兴趣的可以研究下[numpy.squeeze]函数说明
            """
            y = y.squeeze(lead_axis)
        return y

    def backward(self, gy):
        """
        合并求和的反向传播
        :param gy: 导数值
        :return: 合并求和反向传播的值
        """
        gx = broadcast_to(gy, self.from_shape)
        return gx


class BroadcastTo(Function):
    """
    矩阵广播
    """

    def __init__(self, to_shape: tuple):
        """
        初始化
        :param to_shape: 广播后的数组形状
        """
        self.to_shape = to_shape
        self.from_shape = None

    def forward(self, x):
        """
        广播的正向传播
        :param x: 待合并求和的值
        """
        self.from_shape = x.shape
        xp = CUDA.to_gpu()
        """
        参考：
        import numpy as np
        from numpy import broadcast_to
        x = np.array([[1, 2]])
        y = broadcast_to(x, (4, 2))
        print(y)
        # [[1 2]
        #  [1 2]
        #  [1 2]
        #  [1 2]]
        """
        y = xp.broadcast_to(x, self.to_shape)
        return y

    def backward(self, gy):
        """
        广播的反向传播
        :param gy: 导数值
        :return: 广播的反向传播的值
        """
        gx = sum_to(gy, self.from_shape)
        return gx


class Sum(Function):
    """
    求和
    """

    def __init__(self, axis, keepdims):
        """
        初始化
        :param axis: 要求和的数组的形状
        :param keepdims: 是否保留维度（True：保留维度；False：不保留维度）
        """
        self.axis = axis
        self.keepdims = keepdims
        self.x_shape = None

    def forward(self, x):
        """
        求和的正向传播
        :param x: 待求和的值
        """
        self.x_shape = x.shape
        return x.sum(axis=self.axis, keepdims=self.keepdims)

    def backward(self, gy):
        """
        求和的反向传播
        :param gy: 导数值
        :return: 求和的反向传播的值
        """
        gy = reshape_sum_backward(gy, self.x_shape, self.axis, self.keepdims)
        gx = broadcast_to(gy, self.x_shape)
        return gx


class MatMul(Function):
    """
    矩阵相乘
    """

    def forward(self, x0, x1):
        """
        矩阵相乘的正向传播
        :param x0: 一个乘数
        :param x1: 另一个乘数
        """
        return x0.dot(x1)

    def backward(self, gy):
        """
        矩阵相乘的反向传播
        :param gy: 导数值
        :return: 矩阵相乘的反向传播的值
        """
        x0, x1 = self.inputs
        # (3,4)dot(4,2)=(3,2)，对(3,4)的值求导就是(3,2)dot(4,2)的转置矩阵
        gx0 = matmul(gy, x1.T)
        # (3,4)dot(4,2)=(3,2)，对(4,2)的值求导就是(3,4)的转置矩阵dot(3,2)
        gx1 = matmul(x0.T, gy)
        return gx0, gx1


class Transpose(Function):
    """
    矩阵转置
    """

    def __init__(self, axes=None):
        """
        初始化
        :param axes: 轴
        """
        self.axes = axes

    def forward(self, x):
        """
        矩阵转置的正向传播
        :param x: 所要转置的矩阵
        """
        return x.transpose(self.axes)

    def backward(self, gy):
        """
        矩阵转置的反向传播
        :param gy: 导数值
        :return: 矩阵转置的反向传播的值
        """
        if self.axes is None:
            return transpose(gy)
        axes_len = len(self.axes)
        inv_axes = tuple(np.argsort([ax % axes_len for ax in self.axes]))
        return transpose(gy, inv_axes)


class Reshape(Function):
    """
    重塑形状
    """

    def __init__(self, shape):
        """
        初始化
        :param shape: 所要重塑的形状
        """
        self.shape = shape
        self.x_shape = None

    def forward(self, x):
        """
        重塑形状的正向传播
        :param x: 所要转置的矩阵
        """
        self.x_shape = x.shape
        y = x.reshape(self.shape)
        return y

    def backward(self, gy):
        """
        重塑形状的反向传播
        :param gy: 导数值
        :return: 重塑形状的反向传播的值
        """
        return reshape(gy, self.x_shape)


class Linear(Function):
    """
    线性回归：w*x+b
    """

    def forward(self, x, W, b):
        """
        线性回归的正向传播
        :param x: 参数x
        :param W: 参数W
        :param b: 参数b
        :return: 线性回归的计算结果
        """
        y = x.dot(W)
        if b is not None:
            y += b
        return y

    def backward(self, gy):
        """
        线性回归的反向传播
        :param gy: 导数值
        :return: 线性回归的反向传播的值
        """
        x, W, b = self.inputs
        gb = None if b.data is None else sum_to(gy, b.shape)
        gx = matmul(gy, W.T)
        gW = matmul(x.T, gy)
        return gx, gW, gb


class GetItem(Function):

    def __init__(self, slices):
        self.slices = slices

    def forward(self, x):
        y = x[self.slices]
        return y

    def backward(self, gy):
        x, = self.inputs
        f = GetItemGrad(self.slices, x.shape)
        return f(gy)


class GetItemGrad(Function):

    def __init__(self, slices, in_shape):
        self.slices = slices
        self.in_shape = in_shape

    def forward(self, gy):
        xp = CUDA.to_gpu()
        gx = xp.zeros(self.in_shape, dtype=gy.dtype)
        if Config.ENABLE_GPU and CUDA.is_available():
            xp.scatter_add(gx, self.slices, gy)
        else:
            np.add.at(gx, self.slices, gy)
        return gx

    def backward(self, ggx):
        return get_item(ggx, self.slices)
