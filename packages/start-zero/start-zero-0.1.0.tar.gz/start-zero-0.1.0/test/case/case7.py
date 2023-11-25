import numpy as np

from sz import Tensor
from sz import sin, cos, tan, tanh
from sz import exp, lg, ln

x = Tensor(np.array([[1, 2, 3], [4, 5, 6]]))
out1 = tanh(tan(cos(sin(x)) + 10) / 2)
print(out1)

y = Tensor(np.array([[1, 2, 3], [4, 5, 6]]))
out2 = ln(lg(exp(y) + 100) * 1024)
print(out2)

print(out1 + out2)
