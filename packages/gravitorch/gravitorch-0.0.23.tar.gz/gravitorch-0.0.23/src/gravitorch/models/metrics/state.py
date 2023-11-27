from __future__ import annotations

__all__ = [
    "AccuracyState",
    "BaseState",
    "ErrorState",
    "ExtendedAccuracyState",
    "ExtendedErrorState",
    "MeanErrorState",
    "RootMeanErrorState",
    "setup_state",
]

import logging
import math
from abc import ABC, abstractmethod

from coola.utils import str_indent, str_mapping
from objectory import AbstractFactory
from torch import Tensor

from gravitorch.models.metrics.base import EmptyMetricError
from gravitorch.utils.format import str_scalar, str_target_object
from gravitorch.utils.history import BaseHistory, MaxScalarHistory, MinScalarHistory
from gravitorch.utils.meters import MeanTensorMeter, TensorMeter, TensorMeter2
from gravitorch.utils.tensor import to_tensor

logger = logging.getLogger(__name__)


class BaseState(ABC, metaclass=AbstractFactory):
    r"""Defines a base class to implement a metric state.

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics.state import ErrorState
        >>> state = ErrorState()
        >>> state
        ErrorState(
          (meter): TensorMeter
              count   : 0
              sum     : N/A (empty)
              average : N/A (empty)
              min     : N/A (empty)
              max     : N/A (empty)
        )
        >>> state.get_histories("error_")
        (MinScalarHistory(name=error_mean, max_size=10, history=()),
         MinScalarHistory(name=error_min, max_size=10, history=()),
         MinScalarHistory(name=error_max, max_size=10, history=()),
         MinScalarHistory(name=error_sum, max_size=10, history=()))
        >>> state.update(torch.arange(6))
        >>> state.value("error_")
        {'error_mean': 2.5,
         'error_min': 0.0,
         'error_max': 5.0,
         'error_sum': 15.0,
         'error_num_predictions': 6}
    """

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(num_predictions={self.num_predictions:,})"

    @property
    @abstractmethod
    def num_predictions(self) -> int:
        r"""``int``: The number of predictions."""

    @abstractmethod
    def get_histories(self, prefix: str = "", suffix: str = "") -> tuple[BaseHistory, ...]:
        r"""Gets the history trackers for the metric values associated to
        the current state.

        Args:
        ----
            prefix (str, optional): Specifies the key prefix in the
                history tracker names. Default: ``''``
            suffix (str, optional): Specifies the key suffix in the
                history tracker names. Default: ``''``

        Returns:
        -------
            tuple: The history trackers.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import ErrorState
            >>> state = ErrorState()
            >>> state.get_histories("error_")
            (MinScalarHistory(name=error_mean, max_size=10, history=()),
             MinScalarHistory(name=error_min, max_size=10, history=()),
             MinScalarHistory(name=error_max, max_size=10, history=()),
             MinScalarHistory(name=error_sum, max_size=10, history=()))
        """

    @abstractmethod
    def reset(self) -> None:
        r"""Resets the state.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import ErrorState
            >>> state = ErrorState()
            >>> state.update(torch.arange(6))
            >>> state
            ErrorState(
              (meter): TensorMeter
                  count   : 6
                  sum     : 15.0
                  average : 2.5
                  min     : 0.0
                  max     : 5.0
            )
            >>> state.reset()
            >>> state
            ErrorState(
              (meter): TensorMeter
                  count   : 0
                  sum     : N/A (empty)
                  average : N/A (empty)
                  min     : N/A (empty)
                  max     : N/A (empty)
            )
        """

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        r"""Updates the metric state.

        Args:
        ----
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import ErrorState
            >>> state = ErrorState()
            >>> state.update(torch.arange(6))
            >>> state
            ErrorState(
              (meter): TensorMeter
                  count   : 6
                  sum     : 15.0
                  average : 2.5
                  min     : 0.0
                  max     : 5.0
            )
        """

    @abstractmethod
    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        r"""Computes the metric values given the current state.

        Args:
        ----
            prefix (str, optional): Specifies the key prefix in the
                returned dictionary. Default: ``''``
            suffix (str, optional): Specifies the key suffix in the
                returned dictionary. Default: ``''``

        Returns:
        -------
            dict: The metric values.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import ErrorState
            >>> state = ErrorState()
            >>> state.update(torch.arange(6))
            >>> state.value("error_")
            {'error_mean': 2.5,
             'error_min': 0.0,
             'error_max': 5.0,
             'error_sum': 15.0,
             'error_num_predictions': 6}
        """


class MeanErrorState(BaseState):
    r"""Implements a metric state to capture the mean error value.

    This state has a constant space complexity.

    Args:
    ----
        track_num_predictions (bool, optional): If ``True``, the state
            tracks and returns the number of predictions.
            Default: ``True``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics.state import MeanErrorState
        >>> state = MeanErrorState()
        >>> state
        MeanErrorState(
          (meter): MeanTensorMeter(count=0, total=0)
          (track_num_predictions): True
        )
        >>> state.get_histories("error_")
        (MinScalarHistory(name=error_mean, max_size=10, history=()),)
        >>> state.update(torch.arange(6))
        >>> state.value("error_")
        {'error_mean': 2.5, 'error_num_predictions': 6}
    """

    def __init__(self, track_num_predictions: bool = True) -> None:
        self._meter = MeanTensorMeter()
        self._track_num_predictions = bool(track_num_predictions)

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping(
                {"meter": self._meter, "track_num_predictions": self._track_num_predictions}
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def num_predictions(self) -> int:
        return self._meter.count

    def get_histories(self, prefix: str = "", suffix: str = "") -> tuple[BaseHistory, ...]:
        return (MinScalarHistory(name=f"{prefix}mean{suffix}"),)

    def reset(self) -> None:
        self._meter.reset()

    def update(self, error: Tensor) -> None:
        r"""Updates the metric state with a new tensor of errors.

        Args:
        ----
            error (```torch.Tensor``): A tensor of errors.


        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import MeanErrorState
            >>> state = MeanErrorState()
            >>> state.update(torch.arange(6))
            >>> state.value("error_")
            {'error_mean': 2.5, 'error_num_predictions': 6}
        """
        self._meter.update(error.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        meter = self._meter.all_reduce()
        if not meter.count:
            raise EmptyMetricError(f"{self.__class__.__qualname__} is empty")

        results = {f"{prefix}mean{suffix}": self._meter.mean()}
        if self._track_num_predictions:
            results[f"{prefix}num_predictions{suffix}"] = meter.count

        for name, value in results.items():
            logger.info(f"{name}: {str_scalar(value)}")
        return results


class RootMeanErrorState(BaseState):
    r"""Implements a metric state to capture the root mean error value.

    This state has a constant space complexity.

    Args:
    ----
        track_num_predictions (bool, optional): If ``True``, the state
            tracks and returns the number of predictions.
            Default: ``True``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics.state import RootMeanErrorState
        >>> state = RootMeanErrorState()
        >>> state
        RootMeanErrorState(
          (meter): MeanTensorMeter(count=0, total=0)
          (track_num_predictions): True
        )
        >>> state.get_histories("error_")
        (MinScalarHistory(name=error_root_mean, max_size=10, history=()),)
        >>> state.update(torch.arange(6))
        >>> state.value("error_")
        {'error_root_mean': 1.5811388300841898, 'error_num_predictions': 6}
    """

    def __init__(self, track_num_predictions: bool = True) -> None:
        self._meter = MeanTensorMeter()
        self._track_num_predictions = bool(track_num_predictions)

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping(
                {"meter": self._meter, "track_num_predictions": self._track_num_predictions}
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def num_predictions(self) -> int:
        return self._meter.count

    def get_histories(self, prefix: str = "", suffix: str = "") -> tuple[BaseHistory, ...]:
        return (MinScalarHistory(name=f"{prefix}root_mean{suffix}"),)

    def reset(self) -> None:
        self._meter.reset()

    def update(self, error: Tensor) -> None:
        r"""Updates the metric state with a new tensor of errors.

        Args:
        ----
            error (```torch.Tensor``): A tensor of errors.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import RootMeanErrorState
            >>> state = RootMeanErrorState()
            >>> state.update(torch.arange(6))
            >>> state.value("error_")
            {'error_root_mean': 1.5811388300841898, 'error_num_predictions': 6}
        """
        self._meter.update(error.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        meter = self._meter.all_reduce()
        if not meter.count:
            raise EmptyMetricError(f"{self.__class__.__qualname__} is empty")

        results = {f"{prefix}root_mean{suffix}": math.sqrt(self._meter.mean())}
        if self._track_num_predictions:
            results[f"{prefix}num_predictions{suffix}"] = meter.count

        for name, value in results.items():
            logger.info(f"{name}: {str_scalar(value)}")
        return results


class ErrorState(BaseState):
    r"""Implements a metric state to capture some metrics about the
    errors.

    This state has a constant space complexity.

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics.state import ErrorState
        >>> state = ErrorState()
        >>> state
        ErrorState(
          (meter): TensorMeter
              count   : 0
              sum     : N/A (empty)
              average : N/A (empty)
              min     : N/A (empty)
              max     : N/A (empty)
        )
        >>> state.get_histories("error_")
        (MinScalarHistory(name=error_mean, max_size=10, history=()),
         MinScalarHistory(name=error_min, max_size=10, history=()),
         MinScalarHistory(name=error_max, max_size=10, history=()),
         MinScalarHistory(name=error_sum, max_size=10, history=()))
        >>> state.update(torch.arange(6))
        >>> state.value("error_")
        {'error_mean': 2.5,
         'error_min': 0.0,
         'error_max': 5.0,
         'error_sum': 15.0,
         'error_num_predictions': 6}
    """

    def __init__(self) -> None:
        self._meter = TensorMeter()

    def __repr__(self) -> str:
        args = str_indent(str_mapping({"meter": self._meter}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def num_predictions(self) -> int:
        return self._meter.count

    def get_histories(self, prefix: str = "", suffix: str = "") -> tuple[BaseHistory, ...]:
        return (
            MinScalarHistory(name=f"{prefix}mean{suffix}"),
            MinScalarHistory(name=f"{prefix}min{suffix}"),
            MinScalarHistory(name=f"{prefix}max{suffix}"),
            MinScalarHistory(name=f"{prefix}sum{suffix}"),
        )

    def reset(self) -> None:
        self._meter.reset()

    def update(self, error: Tensor) -> None:
        r"""Updates the metric state with a new tensor of errors.

        Args:
        ----
            error (```torch.Tensor``): A tensor of errors.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import ErrorState
            >>> state = ErrorState()
            >>> state.update(torch.arange(6))
            >>> state.value("error_")
            {'error_mean': 2.5,
             'error_min': 0.0,
             'error_max': 5.0,
             'error_sum': 15.0,
             'error_num_predictions': 6}
        """
        self._meter.update(error.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        meter = self._meter.all_reduce()
        if not meter.count:
            raise EmptyMetricError(f"{self.__class__.__qualname__} is empty")

        results = {
            f"{prefix}mean{suffix}": self._meter.mean(),
            f"{prefix}min{suffix}": self._meter.min(),
            f"{prefix}max{suffix}": self._meter.max(),
            f"{prefix}sum{suffix}": self._meter.sum(),
            f"{prefix}num_predictions{suffix}": meter.count,
        }
        for name, value in results.items():
            logger.info(f"{name}: {str_scalar(value)}")
        return results


class ExtendedErrorState(BaseState):
    r"""Implements a metric state to capture some metrics about the
    errors.

    This state stores all the error values, so it may not scale to large
    datasets. This state has a linear space complexity.

    Args:
    ----
        quantiles (``torch.Tensor`` or list or tuple, optional):
            Specifies the quantile values to evaluate.
            Default: ``tuple()``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics.state import ExtendedErrorState
        >>> state = ExtendedErrorState(quantiles=[0.5, 0.9])
        >>> state
        ExtendedErrorState(
          (meter): TensorMeter2(count=0)
          (quantiles): tensor([0.5000, 0.9000])
        )
        >>> state.get_histories("error_")
        (MinScalarHistory(name=error_mean, max_size=10, history=()),
         MinScalarHistory(name=error_median, max_size=10, history=()),
         MinScalarHistory(name=error_min, max_size=10, history=()),
         MinScalarHistory(name=error_max, max_size=10, history=()),
         MinScalarHistory(name=error_sum, max_size=10, history=()),
         MinScalarHistory(name=error_quantile_0.5, max_size=10, history=()),
         MinScalarHistory(name=error_quantile_0.9, max_size=10, history=()))
        >>> state.update(torch.arange(11))
        >>> state.value("error_")
        {'error_mean': 5.0,
         'error_median': 5,
         'error_min': 0,
         'error_max': 10,
         'error_sum': 55,
         'error_std': 3.316624879837036,
         'error_quantile_0.5': 5.0,
         'error_quantile_0.9': 9.0,
         'error_num_predictions': 11}
    """

    def __init__(self, quantiles: Tensor | tuple[float, ...] | list[float] = ()) -> None:
        self._meter = TensorMeter2()
        self._quantiles = to_tensor(quantiles)

    def __repr__(self) -> str:
        args = str_indent(str_mapping({"meter": self._meter, "quantiles": self._quantiles}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def num_predictions(self) -> int:
        return self._meter.count

    def get_histories(self, prefix: str = "", suffix: str = "") -> tuple[BaseHistory, ...]:
        trackers = [
            MinScalarHistory(name=f"{prefix}mean{suffix}"),
            MinScalarHistory(name=f"{prefix}median{suffix}"),
            MinScalarHistory(name=f"{prefix}min{suffix}"),
            MinScalarHistory(name=f"{prefix}max{suffix}"),
            MinScalarHistory(name=f"{prefix}sum{suffix}"),
        ]
        for q in self._quantiles:
            trackers.append(
                MinScalarHistory(name=f"{prefix}quantile_{q:g}{suffix}"),
            )
        return tuple(trackers)

    def reset(self) -> None:
        self._meter.reset()

    def update(self, error: Tensor) -> None:
        r"""Updates the metric state with a new tensor of errors.

        Args:
        ----
            error (```torch.Tensor``): A tensor of errors.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import ExtendedErrorState
            >>> state = ExtendedErrorState(quantiles=[0.5, 0.9])
            >>> state.update(torch.arange(11))
            >>> state.value("error_")
            {'error_mean': 5.0,
             'error_median': 5,
             'error_min': 0,
             'error_max': 10,
             'error_sum': 55,
             'error_std': 3.316624879837036,
             'error_quantile_0.5': 5.0,
             'error_quantile_0.9': 9.0,
             'error_num_predictions': 11}
        """
        self._meter.update(error.detach().cpu())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        meter = self._meter.all_reduce()
        if not meter.count:
            raise EmptyMetricError(f"{self.__class__.__qualname__} is empty")

        results = {
            f"{prefix}mean{suffix}": self._meter.mean(),
            f"{prefix}median{suffix}": self._meter.median(),
            f"{prefix}min{suffix}": self._meter.min(),
            f"{prefix}max{suffix}": self._meter.max(),
            f"{prefix}sum{suffix}": self._meter.sum(),
            f"{prefix}std{suffix}": self._meter.std(),
        }
        if self._quantiles.numel() > 0:
            values = self._meter.quantile(self._quantiles)
            for q, v in zip(self._quantiles, values):
                results[f"{prefix}quantile_{q:g}{suffix}"] = v.item()
        results[f"{prefix}num_predictions{suffix}"] = meter.count
        for name, value in results.items():
            logger.info(f"{name}: {str_scalar(value)}")
        return results


class AccuracyState(BaseState):
    r"""Implements a metric state to compute the accuracy.

    This state has a constant space complexity.

    Args:
    ----
        track_num_predictions (bool, optional): If ``True``, the state
            tracks and returns the number of predictions.
            Default: ``True``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics.state import AccuracyState
        >>> state = AccuracyState()
        >>> state
        AccuracyState(
          (meter): MeanTensorMeter(count=0, total=0)
        )
        >>> state.get_histories()
        (MaxScalarHistory(name=accuracy, max_size=10, history=()),)
        >>> state.update(torch.eye(4))
        >>> state.value()
        {'accuracy': 0.25, 'num_predictions': 16}
    """

    def __init__(self, track_num_predictions: bool = True) -> None:
        self._meter = MeanTensorMeter()
        self._track_num_predictions = bool(track_num_predictions)

    def __repr__(self) -> str:
        args = str_indent(str_mapping({"meter": self._meter}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def num_predictions(self) -> int:
        return self._meter.count

    def get_histories(self, prefix: str = "", suffix: str = "") -> tuple[BaseHistory, ...]:
        return (MaxScalarHistory(name=f"{prefix}accuracy{suffix}"),)

    def reset(self) -> None:
        self._meter.reset()

    def update(self, correct: Tensor) -> None:
        r"""Updates the metric state with a new tensor of errors.

        Args:
        ----
            correct (```torch.Tensor``): A tensor that indicates the
                correct predictions. ``1`` indicates a correct
                prediction and ``0`` indicates a bad prediction.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import AccuracyState
            >>> state = AccuracyState()
            >>> state.update(torch.eye(4))
            >>> state.value()
            {'accuracy': 0.25, 'num_predictions': 16}
        """
        self._meter.update(correct.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        meter = self._meter.all_reduce()
        if not meter.count:
            raise EmptyMetricError(f"{self.__class__.__qualname__} is empty")

        results = {f"{prefix}accuracy{suffix}": meter.mean()}
        if self._track_num_predictions:
            results[f"{prefix}num_predictions{suffix}"] = meter.count

        for name, value in results.items():
            logger.info(f"{name}: {str_scalar(value)}")
        return results


class ExtendedAccuracyState(BaseState):
    r"""Implements a metric state to compute the accuracy and other
    metrics.

    This state has a constant space complexity.

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.metrics.state import ExtendedAccuracyState
        >>> state = ExtendedAccuracyState()
        >>> state
        ExtendedAccuracyState(
          (meter): MeanTensorMeter(count=0, total=0)
        )
        >>> state.get_histories()
        (MaxScalarHistory(name=accuracy, max_size=10, history=()),
         MinScalarHistory(name=error, max_size=10, history=()),
         MaxScalarHistory(name=num_correct_predictions, max_size=10, history=()),
         MinScalarHistory(name=num_incorrect_predictions, max_size=10, history=()))
        >>> state.update(torch.eye(4))
        >>> state.value()
        {'accuracy': 0.25,
         'error': 0.75,
         'num_correct_predictions': 4,
         'num_incorrect_predictions': 12,
         'num_predictions': 16}
    """

    def __init__(self) -> None:
        self._meter = MeanTensorMeter()

    def __repr__(self) -> str:
        args = str_indent(str_mapping({"meter": self._meter}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def num_predictions(self) -> int:
        return self._meter.count

    def get_histories(self, prefix: str = "", suffix: str = "") -> tuple[BaseHistory, ...]:
        return (
            MaxScalarHistory(name=f"{prefix}accuracy{suffix}"),
            MinScalarHistory(name=f"{prefix}error{suffix}"),
            MaxScalarHistory(name=f"{prefix}num_correct_predictions{suffix}"),
            MinScalarHistory(name=f"{prefix}num_incorrect_predictions{suffix}"),
        )

    def reset(self) -> None:
        self._meter.reset()

    def update(self, correct: Tensor) -> None:
        r"""Updates the metric state with a new tensor of errors.

        Args:
        ----
            correct (```torch.Tensor``): A tensor that indicates the
                correct predictions. ``1`` indicates a correct
                prediction and ``0`` indicates a bad prediction.

        Example usage:

        .. code-block:: pycon

            >>> import torch
            >>> from gravitorch.models.metrics.state import ExtendedAccuracyState
            >>> state = ExtendedAccuracyState()
            >>> state.update(torch.eye(4))
            >>> state.value()
            {'accuracy': 0.25,
             'error': 0.75,
             'num_correct_predictions': 4,
             'num_incorrect_predictions': 12,
             'num_predictions': 16}
        """
        self._meter.update(correct.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        meter = self._meter.all_reduce()
        if not meter.count:
            raise EmptyMetricError(f"{self.__class__.__qualname__} is empty")

        accuracy = meter.mean()
        num_correct_predictions = int(meter.sum())
        num_predictions = meter.count
        results = {
            f"{prefix}accuracy{suffix}": accuracy,
            f"{prefix}error{suffix}": 1.0 - accuracy,
            f"{prefix}num_correct_predictions{suffix}": num_correct_predictions,
            f"{prefix}num_incorrect_predictions{suffix}": num_predictions - num_correct_predictions,
            f"{prefix}num_predictions{suffix}": num_predictions,
        }
        for name, value in results.items():
            logger.info(f"{name}: {str_scalar(value)}")
        return results


def setup_state(state: BaseState | dict) -> BaseState:
    r"""Sets up the metric state.

    Args:
    ----
        state (``BaseState`` or dict): Specifies the metric state or
            its configuration.

    Returns:
    -------
        ``BaseState``: The instantiated metric state.

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.models.metrics.state import setup_state
        >>> state = setup_state({"_target_": "gravitorch.models.metrics.state.ErrorState"})
        >>> state
        ErrorState(
          (meter): TensorMeter
              count   : 0
              sum     : N/A (empty)
              average : N/A (empty)
              min     : N/A (empty)
              max     : N/A (empty)
        )
    """
    if isinstance(state, dict):
        logger.info(
            f"Initializing a metric state from its configuration... {str_target_object(state)}"
        )
        state = BaseState.factory(**state)
    if not isinstance(state, BaseState):
        logger.warning(f"state is not a `BaseState` (received: {type(state)})")
    return state
