r"""This module contains some tools to analyze the parameters of a
``torch.nn.Module``."""

from __future__ import annotations

__all__ = [
    "analyze_module_architecture",
    "analyze_model_architecture",
    "analyze_model_architecture",
]

import logging
from typing import TYPE_CHECKING

from torch.nn import Module

from gravitorch.models.utils.summary import ModelSummary
from gravitorch.nn.utils.helpers import (
    get_module_devices,
    num_learnable_parameters,
    num_parameters,
)
from gravitorch.utils.exp_trackers import EpochStep

if TYPE_CHECKING:
    from gravitorch.engines import BaseEngine


logger = logging.getLogger(__name__)


def analyze_module_architecture(
    module: Module, engine: BaseEngine | None = None, prefix: str = ""
) -> None:
    r"""Analyzes the architecture of a ``torch.nn.Module`` object.

    This function does nothing if the module is not
    ``torch.nn.Module``.

    Args:
    ----
        module (``torch.nn.Module``): Specifies the module to analyze.
        engine (``BaseEngine`` or ``None``, optional): Specifies the
            engine to use to log the info. If ``None``, no metric will
            be logged about the model. Default: ``None``
        prefix (str, optional): Specifies the prefix used to log the
            number of parameters. Default: ``''``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.utils import analyze_module_architecture
        >>> analyze_module_architecture(torch.nn.Linear(4, 6))
    """
    if not isinstance(module, Module):
        return
    logger.info(f"Architecture analysis of the top layers\n{ModelSummary(module, mode='top')}")
    logger.info(f"Architecture analysis of all the layers\n{ModelSummary(module, mode='full')}")
    logger.info(f"devices: {get_module_devices(module)}")
    if engine:
        engine.log_metrics(
            {
                f"{prefix}num_parameters": num_parameters(module),
                f"{prefix}num_learnable_parameters": num_learnable_parameters(module),
            },
            step=EpochStep(engine.epoch),
        )


def analyze_model_architecture(model: Module, engine: BaseEngine | None = None) -> None:
    r"""Analyzes the architecture of a model.

    Args:
    ----
        model (``torch.nn.Module``): Specifies the model to log info.
        engine (``BaseEngine`` or ``None``, optional): Specifies the
            engine to use to log the info. If ``None``, no metric
            will be logged about the module. Default: ``None``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.utils import analyze_model_architecture
        >>> from gravitorch.testing import DummyClassificationModel
        >>> model = DummyClassificationModel()
        >>> analyze_model_architecture(model)
    """
    analyze_module_architecture(module=model, engine=engine, prefix="model.")


def analyze_network_architecture(model: Module, engine: BaseEngine | None = None) -> None:
    r"""Analyzes the network architecture of a model.

    This function assumes the model has a  ``network`` attribute.
    This function only analyzes the ``model.network`` attribute,
    and it does nothing if ``model.network`` is not a
    ``torch.nn.Module``.

    Args:
    ----
        model (``torch.nn.Module``): Specifies the model to analyze.
        engine (``BaseEngine`` or ``None``, optional): Specifies the
            engine to use to log the info. If ``None``, no metric
            will be logged about the module. Default: ``None``

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from gravitorch.models.utils import analyze_network_architecture
        >>> from gravitorch.testing import DummyClassificationModel
        >>> model = DummyClassificationModel()
        >>> analyze_network_architecture(model)
    """
    if hasattr(model, "network"):
        analyze_module_architecture(module=model.network, engine=engine, prefix="model.network.")
    else:
        logger.info("The module does not have a network attribute")
