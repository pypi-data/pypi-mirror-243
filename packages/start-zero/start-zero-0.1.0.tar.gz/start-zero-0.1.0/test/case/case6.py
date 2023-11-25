import numpy as np

from sz import Tensor, matmul

t1 = Tensor(np.array([2]))
t2 = Tensor(np.array([4]))

print(t1 + t2)  # Tensor([6])
print(t1 - t2)  # Tensor([-2])
print(t1 * t2)  # Tensor([8])
print(t1 / t2)  # Tensor([0.5])
print(t1 ** 3)  # Tensor([8])
print(-t1)  # Tensor([-2])
print(t1 % t2)  # Tensor([2])

t = (((t1 + t2)**3 - t1) * 2 + (-t2)) % 7
print(t)  # Tensor([4])

x = Tensor(np.array([[1, 2, 3], [4, 5, 6]]))
y = Tensor(np.array([[1, 2], [3, 4], [5, 6]]))
print(matmul(x, y))
"""
Tensor([[22 28]
 [49 64]])
"""
