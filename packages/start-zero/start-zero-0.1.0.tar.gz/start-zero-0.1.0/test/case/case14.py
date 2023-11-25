import numpy as np
import matplotlib.pyplot as plt

from sz import Tensor, clear_tensors
from sz import linear, sigmoid, mean_squared_error

np.random.seed(0)
x = np.random.rand(100, 1)  # 100行1列
y = np.sin(2 * np.pi * x) + np.random.rand(100, 1)  # 100行1列

I, H, O = 1, 10, 1
W1 = Tensor(0.01 * np.random.randn(I, H))
b1 = Tensor(np.zeros(H))
W2 = Tensor(0.01 * np.random.randn(H, O))
b2 = Tensor(np.zeros(O))


def predict(X):
    Y = linear(X, W1, b1)
    Y = sigmoid(Y)
    Y = linear(Y, W2, b2)
    return Y


lr = 0.2
epoch = 10000

for i in range(epoch):

    y_grad = predict(x)
    loss = mean_squared_error(y, y_grad)
    # W1.clear_tensor()
    # b1.clear_tensor()
    # W2.clear_tensor()
    # b2.clear_tensor()
    clear_tensors(W1, b1, W2, b2)
    loss.backward()

    W1.data -= lr * W1.grad.data
    b1.data -= lr * b1.grad.data
    W2.data -= lr * W2.grad.data
    b2.data -= lr * b2.grad.data
    if i % 1000 == 0:
        print(loss)

# Plot
plt.scatter(x, y, s=10)
plt.xlabel('x')
plt.ylabel('y')
t = np.arange(0, 1, .01)[:, np.newaxis]
y_pred = predict(t)
plt.plot(t, y_pred.data, color='r')
plt.show()
"""
Tensor(0.8473695850105871)
Tensor(0.2514286285183607)
Tensor(0.24759485466749878)
Tensor(0.23786120447054832)
Tensor(0.21222231333102953)
Tensor(0.16742181117834223)
Tensor(0.0968193261999272)
Tensor(0.07849528290602335)
Tensor(0.07749729552991157)
Tensor(0.07722132399559317)
"""
