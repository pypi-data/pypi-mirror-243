import numpy as np

from sz import Tensor
from sz import Power, Exp
from sz import NumericalDiff

x = Tensor(np.array(2.0))
f = Power(2)
fnd1 = NumericalDiff.center_numerical_diff(f, x)
print(fnd1)  # 4.000000000004
fnd2 = NumericalDiff.forward_numerical_diff(f, x)
print(fnd2)  # 4.0001000000078335


def new_f(_x):
    A = Power(2)
    B = Exp()
    C = Power(2)
    return C(B(A(_x)))


x = Tensor(np.array(0.5))
y = NumericalDiff.center_numerical_diff(new_f, x)
print(y)  # 3.2974426293330694
