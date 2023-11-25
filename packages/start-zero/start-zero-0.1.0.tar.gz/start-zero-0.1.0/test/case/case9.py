import numpy as np

from sz import Tensor
from sz import max, min, clip

x1 = Tensor(np.array([[1, 2, 3], [2, 2, 3], [1, 1, 1]]))
y1 = max(x1)
y1.backward()
print(x1.grad)

x2 = Tensor(np.array([[1, 2, 3], [2, 2, 3], [1, 1, 1]]))
y2 = min(x2)
y2.backward()
print(x2.grad)

x3 = Tensor(np.array([[11, 2, 3], [2, 2, 3], [1, 1, 1]]))
y3 = clip(x3, 2, 3)
print(y3)
y3.backward()
print(x3.grad)
