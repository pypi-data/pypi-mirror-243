from __future__ import annotations

__all__ = ["ZeroRedundancyOptimizerCreator"]

import logging
from typing import TYPE_CHECKING

from coola.utils import str_indent, str_mapping
from objectory import OBJECT_TARGET
from torch.distributed.optim import ZeroRedundancyOptimizer
from torch.nn import Module
from tornado.util import import_object

from gravitorch import constants as ct
from gravitorch.creators.optimizer.base import BaseOptimizerCreator
from gravitorch.handlers.optimizer_state import ConsolidateOptimizerState
from gravitorch.utils.format import str_pretty_json

if TYPE_CHECKING:
    from gravitorch.engines import BaseEngine

logger = logging.getLogger(__name__)


class ZeroRedundancyOptimizerCreator(BaseOptimizerCreator):
    r"""Implements a zero redundancy optimizer (ZeRO) creator.

    Documentation of ``torch.distributed.optim.ZeroRedundancyOptimizer``:
    https://pytorch.org/docs/stable/distributed.optim.html#torch.distributed.optim.ZeroRedundancyOptimizer

    This creator wraps an arbitrary ``torch.optim.Optimizer``
    optimizer and shards its state as described by ZeRO
    (https://arxiv.org/abs/1910.02054).
    Note ZeRO works only for distributed training.

    Args:
    ----
        optimizer_config (dict): Specifies the optimizer
            configuration. The dictionary must have a key
            ``'_target_`` that indicates the optimizer to shard. The
            other keys are the arguments of the optimizer to shard.
        zero_kwargs (dict): Specifies some keyword arguments used to
            instantiate the
            ``torch.distributed.optim.ZeroRedundancyOptimizer``.
            Please read the documentation of
            ``torch.distributed.optim.ZeroRedundancyOptimizer`` to see
            the possible options. Note that it is not possible to set
            ``params`` and ``optimizer_class`` with a keyword argument.
        add_module_to_engine (bool, optional): If ``True``, the
            optimizer is added to the engine state, so the optimizer
            state is stored when the engine creates a checkpoint.
            Default: ``True``
        attach_handler (bool, optional): If ``True``, a handler is
            attached to the engine to consolidate the ZeRO optimizer
            state at the end of each training epoch. Consolidate the
            optimizer state dict is important to export the optimizer
            state dict. If ``False``, no handler is attached.
            Default: ``True``

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.testing import create_dummy_engine, DummyClassificationModel
        >>> from gravitorch.creators.optimizer import ZeroRedundancyOptimizerCreator
        >>> creator = ZeroRedundancyOptimizerCreator({"_target_": "torch.optim.SGD", "lr": 0.01})
        >>> creator
        ZeroRedundancyOptimizerCreator(
          (optimizer_class): <class 'torch.optim.sgd.SGD'>
          (optimizer_config): {'lr': 0.01}
          (zero_kwargs): {}
          (add_module_to_engine): True
          (attach_handler): True
        )
        >>> engine = create_dummy_engine()
        >>> model = DummyClassificationModel()
        >>> optimizer = creator.create(engine, model)  # doctest: +SKIP
    """

    def __init__(
        self,
        optimizer_config: dict,
        zero_kwargs: dict | None = None,
        add_module_to_engine: bool = True,
        attach_handler: bool = True,
    ) -> None:
        self._optimizer_class = import_object(optimizer_config.pop(OBJECT_TARGET))
        self._optimizer_config = optimizer_config
        self._zero_kwargs = zero_kwargs or {}
        self._add_module_to_engine = bool(add_module_to_engine)
        self._attach_handler = bool(attach_handler)

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "optimizer_class": self._optimizer_class,
                    "optimizer_config": str_pretty_json(self._optimizer_config),
                    "zero_kwargs": str_pretty_json(self._zero_kwargs),
                    "add_module_to_engine": self._add_module_to_engine,
                    "attach_handler": self._attach_handler,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def create(self, engine: BaseEngine, model: Module) -> ZeroRedundancyOptimizer:
        optimizer = ZeroRedundancyOptimizer(
            params=model.parameters(),
            optimizer_class=self._optimizer_class,
            **self._optimizer_config,
            **self._zero_kwargs,
        )
        logger.info(f"optimizer:\n{optimizer}")
        if self._add_module_to_engine:
            logger.info(f"Adding an optimizer to the engine (key: {ct.OPTIMIZER})...")
            engine.add_module(ct.OPTIMIZER, optimizer)
        if self._attach_handler:
            logger.info("Creating handler to consolidate the optimizer state dict...")
            ConsolidateOptimizerState().attach(engine)
        return optimizer
