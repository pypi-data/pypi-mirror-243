from sz.core.model import Model
from sz.functions.ft4 import sigmoid
from sz.layers.linear import Linear as LinearLayer


class MLP(Model):
    """
    多层感知器
    """

    def __init__(self, out_sizes: tuple, activation=sigmoid):
        super().__init__()
        self.activation = activation
        self.layers = []

        for i in range(0, len(out_sizes)):
            layer = LinearLayer(out_sizes[i])
            setattr(self, 'l' + str(i), layer)
            self.layers.append(layer)

    def forward(self, x):
        # 假设数组为：[1, 2, 3, 4, 5]，这里取除最后一个外的所有，即：[1, 2, 3, 4]
        for l in self.layers[:-1]:
            linear = l(x)  # 仿射
            x = self.activation(linear)  # 激活
        # 返回最后一个，即：[5]
        return self.layers[-1](x)
