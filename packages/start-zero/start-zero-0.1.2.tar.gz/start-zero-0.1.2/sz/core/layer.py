import weakref

from sz.core.tensor import Parameter


class Layer:
    """
    说明：
    x = np.array([[1, 2], [3, 4]])  # (2, 2)
    l = Layer() => 调用init方法
    ①y = l(x) => 调用__call__方法 => 调用forward方法 => 由于没有实现，所以报错
    ②只添加Parameter或Layer的实例
    l = Layer()
    l.l1 = Parameter(np.array(10))
    l.l2 = Parameter(np.array(11))
    l.l3 = 12
    l.l4 = Layer()
    """

    def __init__(self):
        self._params = set()

    def __setattr__(self, name, value):
        # 只有Parameter或Layer的实例才会被加入处理
        if isinstance(value, (Parameter, Layer)):
            self._params.add(name)
        super().__setattr__(name, value)

    def __call__(self, *inputs):
        outputs = self.forward(*inputs)
        if not isinstance(outputs, tuple):
            outputs = (outputs,)
        self.inputs = [weakref.ref(x) for x in inputs]
        self.outputs = [weakref.ref(y) for y in outputs]
        return outputs if len(outputs) > 1 else outputs[0]

    def forward(self, inputs):
        raise NotImplementedError()

    def params(self):
        for name in self._params:
            obj = self.__dict__[name]
            if isinstance(obj, Layer):
                yield from obj.params()
            else:
                yield obj

    def clear_tensors(self):
        for param in self.params():
            param.clear_tensor()

    """
    def get_params(self):
        for name in self._params:
            print(self.__dict__[name].W.shape)
    """
