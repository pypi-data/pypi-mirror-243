from sz.core.tensor import Tensor


class NumericalDiff:
    """
    数值微分：差分近似
    """

    @staticmethod
    def center_numerical_diff(function, x: Tensor, eps=1e-4):
        """
        中心差分近似
        """
        v1 = Tensor(x.data + eps)
        v2 = Tensor(x.data - eps)
        y1 = function(v1)
        y2 = function(v2)
        return (y1.data - y2.data) / (2 * eps)

    @staticmethod
    def forward_numerical_diff(function, x: Tensor, eps=1e-4):
        """
        前向差分近似
        """
        v1 = Tensor(x.data + eps)
        v2 = Tensor(x.data)
        y1 = function(v1)
        y2 = function(v2)
        return (y1.data - y2.data) / eps
