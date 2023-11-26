r"""This module defines the squared logarithmic error (SLE) metric."""

from __future__ import annotations

__all__ = ["SquaredAsinhError", "SquaredLogError", "SquaredSymlogError"]

import logging

from torch import Tensor

from gravitorch.models.metrics.base_epoch import BaseStateEpochMetric
from gravitorch.models.metrics.state import BaseState, ErrorState
from gravitorch.nn.functional import asinh_mse_loss, msle_loss, symlog_mse_loss

logger = logging.getLogger(__name__)


class SquaredLogError(BaseStateEpochMetric):
    r"""Implements the squared logarithmic error (SLE) metric.

    This metric is best to use when targets having exponential growth,
    such as population counts, average sales of a commodity over a
    span of years etc. Note that this metric penalizes an
    under-predicted estimate greater than an over-predicted estimate.

    Note: this metric only works with positive value (0 included).

    Args:
    ----
        mode (str): Specifies the mode (e.g. train or eval).
        name (str, optional): Specifies the name of the metric. The
            name is used to log the metric results.
            Default: ``'sq_log_err'``
        state (``BaseState`` or dict, optional): Specifies the metric
            state or its configuration. If ``None``, ``ErrorState`` is
            instantiated. Default: ``None``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics import SquaredLogError
        >>> metric = SquaredLogError("eval")
        >>> metric
        SquaredLogError(
          (mode): eval
          (name): sq_log_err
          (state): ErrorState(num_predictions=0)
        )
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'eval/sq_log_err_mean': 0.0,
         'eval/sq_log_err_min': 0.0,
         'eval/sq_log_err_max': 0.0,
         'eval/sq_log_err_sum': 0.0,
         'eval/sq_log_err_num_predictions': 8}
        >>> metric(torch.eye(2), torch.ones(2, 2))
        >>> metric.value()
        {'eval/sq_log_err_mean': 0.080075...,
         'eval/sq_log_err_min': 0.0,
         'eval/sq_log_err_max': 0.480453...,
         'eval/sq_log_err_sum': 0.960906...,
         'eval/sq_log_err_num_predictions': 12}
        >>> metric.reset()
        >>> metric(torch.eye(2), torch.ones(2, 2))
        >>> metric.value()
        {'eval/sq_log_err_mean': 0.240226...,
         'eval/sq_log_err_min': 0.0,
         'eval/sq_log_err_max': 0.480453...,
         'eval/sq_log_err_sum': 0.960906...,
         'eval/sq_log_err_num_predictions': 4}
    """

    def __init__(
        self,
        mode: str,
        name: str = "sq_log_err",
        state: BaseState | dict | None = None,
    ) -> None:
        super().__init__(mode=mode, name=name, state=state or ErrorState())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Updates the squared logarithmic error metric given a mini-
        batch of examples.

        Args:
        ----
            prediction (``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long):
                Specifies the predictions.
            target (``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long):
                Specifies the target tensor.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics import SquaredLogError
            >>> metric = SquaredLogError("eval")
            >>> metric(torch.ones(2, 4), torch.ones(2, 4))
            >>> metric.value()
            {'eval/sq_log_err_mean': 0.0,
             'eval/sq_log_err_min': 0.0,
             'eval/sq_log_err_max': 0.0,
             'eval/sq_log_err_sum': 0.0,
             'eval/sq_log_err_num_predictions': 8}
        """
        self._state.update(msle_loss(prediction, target, reduction="none"))


class SquaredSymlogError(BaseStateEpochMetric):
    r"""Implements a metric to compute the squared error on the symlog
    transformed predictions and targets.

    It is a generalization of mean squared logarithmic error (MSLE)
    that works for real values. The ``symlog`` transformation is used
    instead of ``log1p`` because ``symlog`` works on negative values.

    Args:
    ----
        mode (str): Specifies the mode (e.g. train or eval).
        name (str, optional): Specifies the name of the metric. The
            name is used to log the metric results.
            Default: ``'sq_symlog_err'``
        state (``BaseState`` or dict, optional): Specifies the metric
            state or its configuration. If ``None``, ``ErrorState`` is
            instantiated. Default: ``None``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics import SquaredSymlogError
        >>> metric = SquaredSymlogError("eval")
        >>> metric
        SquaredSymlogError(
          (mode): eval
          (name): sq_symlog_err
          (state): ErrorState(num_predictions=0)
        )
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'eval/sq_symlog_err_mean': 0.0,
         'eval/sq_symlog_err_min': 0.0,
         'eval/sq_symlog_err_max': 0.0,
         'eval/sq_symlog_err_sum': 0.0,
         'eval/sq_symlog_err_num_predictions': 8}
        >>> metric(torch.eye(2), torch.ones(2, 2))
        >>> metric.value()
        {'eval/sq_symlog_err_mean': 0.080075...,
         'eval/sq_symlog_err_min': 0.0,
         'eval/sq_symlog_err_max': 0.480453...,
         'eval/sq_symlog_err_sum': 0.960906...,
         'eval/sq_symlog_err_num_predictions': 12}
        >>> metric.reset()
        >>> metric(torch.eye(2), torch.ones(2, 2))
        >>> metric.value()
        {'eval/sq_symlog_err_mean': 0.240226...,
         'eval/sq_symlog_err_min': 0.0,
         'eval/sq_symlog_err_max': 0.480453...,
         'eval/sq_symlog_err_sum': 0.960906...,
         'eval/sq_symlog_err_num_predictions': 4}
    """

    def __init__(
        self,
        mode: str,
        name: str = "sq_symlog_err",
        state: BaseState | dict | None = None,
    ) -> None:
        super().__init__(mode=mode, name=name, state=state or ErrorState())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Updates the squared error on the symlog transformed
        predictions and targets given a mini-batch of examples.

        Args:
        ----
            prediction (``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long):
                Specifies the predictions.
            target (``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long):
                Specifies the target tensor.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics import SquaredSymlogError
            >>> metric = SquaredSymlogError("eval")
            >>> metric(torch.ones(2, 4), torch.ones(2, 4))
            >>> metric.value()
            {'eval/sq_symlog_err_mean': 0.0,
             'eval/sq_symlog_err_min': 0.0,
             'eval/sq_symlog_err_max': 0.0,
             'eval/sq_symlog_err_sum': 0.0,
             'eval/sq_symlog_err_num_predictions': 8}
        """
        self._state.update(symlog_mse_loss(prediction, target, reduction="none"))


class SquaredAsinhError(BaseStateEpochMetric):
    r"""Implements a metric to compute the squared error on the inverse
    hyperbolic sine (arcsinh) transformed predictions and targets.

    Args:
    ----
        mode (str): Specifies the mode (e.g. train or eval).
        name (str, optional): Specifies the name of the metric. The
            name is used to log the metric results.
            Default: ``'sq_asinh_err'``
        state (``BaseState`` or dict, optional): Specifies the metric
            state or its configuration. If ``None``, ``ErrorState`` is
            instantiated. Default: ``None``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics import SquaredAsinhError
        >>> metric = SquaredAsinhError("eval")
        >>> metric
        SquaredAsinhError(
          (mode): eval
          (name): sq_asinh_err
          (state): ErrorState(num_predictions=0)
        )
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'eval/sq_asinh_err_mean': 0.0,
         'eval/sq_asinh_err_min': 0.0,
         'eval/sq_asinh_err_max': 0.0,
         'eval/sq_asinh_err_sum': 0.0,
         'eval/sq_asinh_err_num_predictions': 8}
        >>> metric(torch.eye(2), torch.ones(2, 2))
        >>> metric.value()
        {'eval/sq_asinh_err_mean': 0.129469...,
         'eval/sq_asinh_err_min': 0.0,
         'eval/sq_asinh_err_max': 0.776819...,
         'eval/sq_asinh_err_sum': 1.553638...,
         'eval/sq_asinh_err_num_predictions': 12}
        >>> metric.reset()
        >>> metric(torch.eye(2), torch.ones(2, 2))
        >>> metric.value()
        {'eval/sq_asinh_err_mean': 0.388409...,
         'eval/sq_asinh_err_min': 0.0,
         'eval/sq_asinh_err_max': 0.776819...,
         'eval/sq_asinh_err_sum': 1.553638...,
         'eval/sq_asinh_err_num_predictions': 4}
    """

    def __init__(
        self,
        mode: str,
        name: str = "sq_asinh_err",
        state: BaseState | dict | None = None,
    ) -> None:
        super().__init__(mode=mode, name=name, state=state or ErrorState())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Updates the squared error on the inverse hyperbolic sine
        (arcsinh) transformed predictions and targets given a mini-batch
        of examples.

        Args:
        ----
            prediction (``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long):
                Specifies the predictions.
            target (``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long):
                Specifies the target tensor.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics import SquaredAsinhError
            >>> metric = SquaredAsinhError("eval")
            >>> metric(torch.ones(2, 4), torch.ones(2, 4))
            >>> metric.value()
            {'eval/sq_asinh_err_mean': 0.0,
             'eval/sq_asinh_err_min': 0.0,
             'eval/sq_asinh_err_max': 0.0,
             'eval/sq_asinh_err_sum': 0.0,
             'eval/sq_asinh_err_num_predictions': 8}
        """
        self._state.update(asinh_mse_loss(prediction, target, reduction="none"))
