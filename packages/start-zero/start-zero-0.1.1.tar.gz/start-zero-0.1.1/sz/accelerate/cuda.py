import numpy as np

from sz.core.config import Config

cupy_is_available = False
try:
    """
    Windows下安装cupy支持GPU运算：   
    1、N卡支持下载：https://developer.nvidia.com/cuda-downloads   
    2、pip install cupy-cuda12x
    """
    import cupy as cp

    cupy_is_available = True
except ModuleNotFoundError:
    pass


class CUDA:

    @staticmethod
    def is_available():
        """
        是否能使用N卡的GPU加速
        :return: True：可以；False：不可以
        """
        return cupy_is_available

    @staticmethod
    def to_gpu():
        """
        CPU转GPU
        :return: 转换后的模式
        """
        """
        import numpy as np
        import cupy as cp
        A = np.zeros((4,4))
        B = cp.asarray(A)  # numpy -> cupy
        C = cp.asnumpy(B)  # cupy -> numpy
        print(type(A), type(B), type(C))
        """
        return cp if (Config.ENABLE_GPU and cupy_is_available) else np

    @staticmethod
    def to_cpu():
        """
        转CPU
        :return: 转换后的模式
        """
        return np
