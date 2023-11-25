import numpy as np

from sz import MLP, SGD, MomentumSGD, AdaGrad, AdaDelta, Adam
from sz import mean_squared_error

np.random.seed(0)
x = np.random.rand(100, 1)  # 100行1列
y = np.sin(2 * np.pi * x) + np.random.rand(100, 1)  # 100行1列

lr = 0.1
epoch = 100000

model = MLP((30, 40, 50, 40, 30, 1))
optimizer = MomentumSGD(lr).setup(model)

for i in range(epoch):
    y_grad = model(x)
    loss = mean_squared_error(y, y_grad)
    model.clear_tensors()
    loss.backward()
    optimizer.update()
    if i % 10000 == 0:
        print(loss)
"""
Tensor(0.6983994697470247)
Tensor(0.07147807999363118)
Tensor(0.06686731420676502)
Tensor(0.06457327696768171)
Tensor(0.06346820184233602)
Tensor(0.06303657281191644)
Tensor(0.0630364437176761)
Tensor(0.05864909933182604)
Tensor(0.054803001013300136)
Tensor(0.05439496584281861)
"""
