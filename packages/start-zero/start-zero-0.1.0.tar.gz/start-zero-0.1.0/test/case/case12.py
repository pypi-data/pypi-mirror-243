import numpy as np

from sz import Tensor

x = Tensor(np.array(2.0))
y = x ** 2
y.backward()
gx = x.grad
print(x.grad)  # Tensor(4.0)
x.clear_tensor()

z = gx ** 3 + y
z.backward()
print(x.grad)  # Tensor(100.0)
