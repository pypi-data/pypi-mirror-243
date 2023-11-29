from sz.accelerate.cuda import CUDA
from sz.functions.bf import Function

"""
函数类型3：指数对数函数
e为底的指数[exp]、10为底的对数[lg]、e为底的对数[ln]
"""


def exp(x):
    return Exp()(x)


def lg(x):
    return Lg()(x)


def ln(x):
    return Ln()(x)


class Exp(Function):
    """
    e为底的指数类
    """

    def forward(self, x):
        """
        e为底的指数的正向传播
        :param x: 待求e为底的指数的值
        """
        xp = CUDA.to_gpu()
        return xp.exp(x)

    def backward(self, gy):
        """
        e为底的指数的反向传播
        :param gy: 导数值
        :return: e为底的指数反向传播的值
        """
        y = self.outputs[0]()  # 弱引用
        gx = gy * y
        return gx


class Lg(Function):
    """
    10为底的对数类
    """

    def forward(self, x):
        """
        10为底的对数的正向传播
        :param x: 待求10为底的对数的值
        """
        xp = CUDA.to_gpu()
        y = xp.log10(x)
        return y

    def backward(self, gy):
        """
        10为底的对数的反向传播
        :param gy: 导数值
        :return: 10为底的对数反向传播的值
        """
        x = self.inputs[0]
        gx = gy / x
        return gx


class Ln(Function):
    """
    e为底的对数类
    """

    def forward(self, x):
        """
        e为底的对数的正向传播
        :param x: 待求e为底的对数的值
        """
        xp = CUDA.to_gpu()
        y = xp.log(x)
        return y

    def backward(self, gy):
        """
        e为底的对数的反向传播
        :param gy: 导数值
        :return: e为底的对数反向传播的值
        """
        x = self.inputs[0]
        gx = gy / x
        return gx
