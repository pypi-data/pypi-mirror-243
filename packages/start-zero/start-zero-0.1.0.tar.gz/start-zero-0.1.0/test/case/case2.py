from sz import Config, CUDA

Config.ENABLE_GPU = True
xp = CUDA.to_gpu()
print(Config.ENABLE_GPU, CUDA.is_available(), Config.ENABLE_GPU and CUDA.is_available())
x = xp.array([1.2, 2.2, 3.2])
y = xp.sin(x)
z = y + xp.array(10) + 1
z = z * 10 + xp.cos(.2)
print(z, type(z))
