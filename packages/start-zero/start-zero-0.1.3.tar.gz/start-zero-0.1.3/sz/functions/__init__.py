def reshape_sum_backward(gy, x_shape, axis, keepdims):
    ndim = len(x_shape)
    tupled_axis = axis
    if axis is None:
        tupled_axis = None
    elif not isinstance(axis, tuple):
        tupled_axis = (axis,)
    if not (ndim == 0 or tupled_axis is None or keepdims):
        actual_axis = [a if a >= 0 else a + ndim for a in tupled_axis]
        shape = list(gy.shape)
        for a in sorted(actual_axis):
            shape.insert(a, 1)
    else:
        shape = gy.shape
    gy = gy.reshape(shape)  # reshape
    return gy


def log_sum_exp(xp, x, axis=1):
    m = x.max(axis=axis, keepdims=True)
    y = x - m
    # xp.exp(y, out=y)
    y = xp.exp(y)
    s = y.sum(axis=axis, keepdims=True)
    # xp.log(s, out=s)
    s = xp.log(s)
    # m += s
    m = m + s
    return m


def max_backward_shape(x, axis):
    if axis is None:
        axis = range(x.ndim)
    elif isinstance(axis, int):
        axis = (axis,)
    else:
        axis = axis
    shape = [s if ax not in axis else 1 for ax, s in enumerate(x.shape)]
    return shape
