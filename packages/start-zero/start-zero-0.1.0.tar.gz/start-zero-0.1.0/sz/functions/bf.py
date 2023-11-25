import weakref

import sz
from sz.core.config import Config
from sz.core.tensor import Tensor


class Function:
    """
    所有函数的父类（基类）
    """

    def __call__(self, *inputs):
        self.inputs = [sz.to_tensor(each) for each in inputs]  # 函数的输入值（对输入值进行类型转换处理）
        xs = [each.data for each in self.inputs]
        ys = self.forward(*xs)  # 前向传播的计算值
        if not isinstance(ys, tuple):  # 例如[1,2,3]+[1,2,3]=[2,4,6]，[2,4,6]应将其当做一个值而不是一个列表包含三个值
            ys = (ys,)
        outputs = [Tensor(each) for each in ys]  # 前向传播的计算值为数值或ndarray类型，最终需要在将其封装为Tensor对象
        if Config.ENABLE_BACKPROP:  # 只有需要进行反向传播时才会进行处理
            generation = max([each.generation for each in self.inputs])
            for each in outputs:
                each.creator = self
                each.generation = generation + 1
            self.outputs = [weakref.ref(output) for output in outputs]  # 保存输出信息（弱引用）
        # print('输入：', self.inputs, '参与运算的函数名称：', self.__class__.__name__, '输出：', outputs)
        return outputs if len(outputs) > 1 else outputs[0]  # 函数的输出值

    def forward(self, *xs):
        """
        正向传播
        """
        raise NotImplementedError()

    def backward(self, *gys):
        """
        反向传播
        """
        raise NotImplementedError()
