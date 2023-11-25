import numpy as np

from sz import Tensor
from sz import sum, sum_to
from sz import SumTo, BroadcastTo, Sum, average, MatMul, Transpose, Reshape, Linear

test_array = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])

_sum_to = SumTo((1, 4))
out = _sum_to.forward(test_array)
print(out)

broadcast_to = BroadcastTo((4, 4))
out = broadcast_to.forward(np.array([1, 2, 3, 4]))
print(out)

_sum = Sum((0, 1), keepdims=False)
out = _sum.forward(test_array)
print(out)

out = average(test_array, axis=0, keepdims=False)
print(out)

x_23 = np.array([[1, 2, 3], [4, 5, 6]])
x_32 = np.array([[1, 2], [3, 4], [5, 6]])
matmul = MatMul()
out = matmul.forward(x_23, x_32)
print(out)

transpose = Transpose(axes=(1, 0))
out = transpose.forward(test_array)
print(out)

reshape = Reshape((8, 2))
out = reshape.forward(test_array)
print(out)

x = np.array([1, 2, 3])
W = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
b = 1000
linear = Linear()
out = linear.forward(x, W, b)
print(out)

x = Tensor(np.array([[1, 2, 3], [4, 5, 6]]))
y = sum(x, axis=0)
y.backward()
print(y)
print(x.grad)

x = Tensor(np.random.randn(2, 3, 4, 5))
y = sum(x, keepdims=True)
print(y.shape)

x = Tensor(np.array([[1, 2, 3], [4, 5, 6]]))
y = sum_to(x, (1, 3))
print(y)

y = sum_to(x, (2, 1))
print(y)

x0 = Tensor(np.array([1, 2, 3]))
x1 = Tensor(np.array([10]))
y = x0 + x1
print(y)
y.backward()
print(x1.grad)
"""
[[28 32 36 40]]
[[1 2 3 4]
 [1 2 3 4]
 [1 2 3 4]
 [1 2 3 4]]
136
Tensor([ 7.  8.  9. 10.])
[[22 28]
 [49 64]]
[[ 1  5  9 13]
 [ 2  6 10 14]
 [ 3  7 11 15]
 [ 4  8 12 16]]
[[ 1  2]
 [ 3  4]
 [ 5  6]
 [ 7  8]
 [ 9 10]
 [11 12]
 [13 14]
 [15 16]]
[1006 1006 1006]
Tensor([5 7 9])
Tensor([[1 1 1]
 [1 1 1]])
(1, 1, 1, 1)
Tensor([[5 7 9]])
Tensor([[ 6]
 [15]])
Tensor([11 12 13])
Tensor([1 1 1])
"""
