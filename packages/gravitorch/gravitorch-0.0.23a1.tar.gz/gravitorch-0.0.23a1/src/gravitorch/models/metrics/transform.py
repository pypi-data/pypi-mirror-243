from __future__ import annotations

__all__ = ["TransformedPredictionTarget"]


from torch import Tensor
from torch.nn import Flatten, Identity, Module

from gravitorch.engines.base import BaseEngine
from gravitorch.models.metrics.base import BaseMetric, setup_metric
from gravitorch.nn import Asinh, Log1p, Symlog, setup_module


class TransformedPredictionTarget(BaseMetric):
    r"""Implements a metric wrapper to transform the prediction and
    target inputs.

    Args:
    ----
        metric (``BaseMetric`` or dict): Specifies the metric (or its
            configuration) to wrap to transform the prediction and
            target inputs. The forward method of the metric should
            have only two inputs: prediction and target.
        prediction_transform (``torch.nn.Module`` or dict or ``None``):
            Specifies the prediction transformation or its
            configuration. If ``None``, the identity transformation
            is used. Default: ``None``
        target_transform (``torch.nn.Module`` or dict or ``None``):
            Specifies the target transformation or its configuration.
            If ``None``, the identity transformation is used.
            Default: ``None``
    """

    def __init__(
        self,
        metric: BaseMetric | dict,
        prediction_transform: Module | dict | None = None,
        target_transform: Module | dict | None = None,
    ) -> None:
        super().__init__()
        self.metric = setup_metric(metric)
        self.prediction_transform = setup_module(prediction_transform or Identity())
        self.target_transform = setup_module(target_transform or Identity())

    def attach(self, engine: BaseEngine) -> None:
        self.metric.attach(engine)

    def forward(self, prediction: Tensor, target: Tensor) -> dict | None:
        r"""Updates the metric given a mini-batch of examples.

        Args:
        ----
            prediction (``torch.Tensor`` of type float): Specifies
                the tensor of predictions.
            target (``torch.Tensor`` of type float and same shape as
                ``prediction``): Specifies the tensor of targets.

        Returns:
        -------
            dict or ``None``: The output of the metrics.
        """
        return self.metric(self.prediction_transform(prediction), self.target_transform(target))

    def reset(self) -> None:
        self.metric.reset()

    def value(self, engine: BaseEngine | None = None) -> dict:
        return self.metric.value(engine)

    @classmethod
    def create_asinh(cls, metric: BaseMetric | dict) -> TransformedPredictionTarget:
        r"""Creates a ``TransformedMetric`` with inverse hyperbolic sine
        (arcsinh) transformations.

        Args:
        ----
            metric (``BaseMetric`` or dict): Specifies the metric (or
                its configuration) to wrap to transform the prediction
                and target inputs. The forward method of the metric
                should have only two inputs: prediction and target.

        Returns:
        -------
            ``TransformedPredictionTarget``: An instantiated metric with
                inverse hyperbolic sine (arcsinh) transformations.
        """
        return cls(metric=metric, prediction_transform=Asinh(), target_transform=Asinh())

    @classmethod
    def create_flatten(cls, metric: BaseMetric | dict) -> TransformedPredictionTarget:
        r"""Creates a ``TransformedMetric`` with flatten transformations.

        Args:
        ----
            metric (``BaseMetric`` or dict): Specifies the metric (or
                its configuration) to wrap to transform the prediction
                and target inputs. The forward method of the metric
                should have only two inputs: prediction and target.

        Returns:
        -------
            ``TransformedPredictionTarget``: An instantiated metric
                with ``flatten`` transformations.
        """
        return cls(metric=metric, prediction_transform=Flatten(), target_transform=Flatten())

    @classmethod
    def create_log1p(cls, metric: BaseMetric | dict) -> TransformedPredictionTarget:
        r"""Creates a ``TransformedMetric`` with log1p transformations.

        Args:
        ----
            metric (``BaseMetric`` or dict): Specifies the metric (or
                its configuration) to wrap to transform the prediction
                and target inputs. The forward method of the metric
                should have only two inputs: prediction and target.

        Returns:
        -------
            ``TransformedPredictionTarget``: An instantiated metric
                with ``log1p`` transformations.
        """
        return cls(metric=metric, prediction_transform=Log1p(), target_transform=Log1p())

    @classmethod
    def create_symlog(cls, metric: BaseMetric | dict) -> TransformedPredictionTarget:
        r"""Creates a ``TransformedMetric`` with symlog transformations.

        Args:
        ----
            metric (``BaseMetric`` or dict): Specifies the metric (or
                its configuration) to wrap to transform the prediction
                and target inputs. The forward method of the metric
                should have only two inputs: prediction and target.

        Returns:
        -------
            ``TransformedPredictionTarget``: An instantiated metric
                with ``symlog`` transformations.
        """
        return cls(metric=metric, prediction_transform=Symlog(), target_transform=Symlog())
