import numpy as np

from sz import Tensor

t = Tensor(np.random.randn(3, 2, 4))
print(len(t))  # 3
print(t)
print(t.shape)  # (3, 2, 1)
print(t.size)  # 6
print(t.ndim)  # 3
print(t.dtype)  # float64
print(t.T)
print(t.transpose())
print(t.transpose((1, 0, 2)))
print(t.reshape((12, 1, 2)))
