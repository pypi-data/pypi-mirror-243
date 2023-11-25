import numpy as np

from sz import Tensor

x = Tensor(np.array([2]))
y = (x**3+x)*5
print(y)
y.backward()
print(x.grad)
z = x.grad
x.clear_tensor()
z.backward()
print(x.grad)
z = x.grad
x.clear_tensor()
z.backward()
print(x.grad)
"""
Tensor([50])
Tensor([65])
Tensor([60])
Tensor([30])
"""
