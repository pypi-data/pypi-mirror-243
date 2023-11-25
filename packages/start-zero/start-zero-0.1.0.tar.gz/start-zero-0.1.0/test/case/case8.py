import numpy as np

from sz import Tensor
from sz import sigmoid, relu, softmax, log_softmax, leaky_relu
from sz import mean_squared_error, softmax_cross_entropy, sigmoid_cross_entropy, binary_cross_entropy

x = Tensor(np.array([[1., 2., 3.], [4., 5., 6.]]))
out1 = leaky_relu(log_softmax(softmax(sigmoid(x) + relu(x)) + 10) * (-1))
print(out1)

y1 = Tensor(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
y2 = Tensor(np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]]))

out2 = mean_squared_error(y1, y2)
print(out2)

y1 = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3], [1, 1, 1], [2, 2, 2], [3, 3, 3], [1, 1, 1], [2, 2, 2], [3, 3, 3]])
y2 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1])

out3 = softmax_cross_entropy(y1, y2)
print(out3)

y1 = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3], [1, 1, 1], [2, 2, 2], [3, 3, 3], [1, 1, 1], [2, 2, 2], [3, 3, 3]])
y2 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3])
out2 = sigmoid_cross_entropy(y1, y2)
print(out2)

y1 = np.array([[1, 2], [4, 5], [7, 8]])
y2 = np.array([[9, 8], [6, 5], [3, 2]])
out2 = binary_cross_entropy(y1, y2)
print(out2)
