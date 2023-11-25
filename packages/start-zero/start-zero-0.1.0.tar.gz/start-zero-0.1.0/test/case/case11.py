import numpy as np

from sz import Tensor, clear_tensors


def rosenbrock(_x0, _x1):
    _y = 100 * (_x1 - _x0 ** 2) ** 2 + (_x0 - 1) ** 2
    return _y


x0 = Tensor(np.array(0.0))
x1 = Tensor(np.array(2.0))
lr = 0.001
iters = 50000

for i in range(iters):
    y = rosenbrock(x0, x1)
    clear_tensors(x0, x1)
    y.backward()
    x0 -= lr * x0.grad
    x1 -= lr * x1.grad
    print(x0, x1)
"""
趋向于：Tensor(0.9999999993724021) Tensor(0.999999998742293)
"""
