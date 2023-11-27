r"""This module implements a no-operation training loop."""

from __future__ import annotations

__all__ = ["NoOpTrainingLoop"]

import logging
from typing import Any

from gravitorch.engines.base import BaseEngine
from gravitorch.loops.training.base import BaseTrainingLoop

logger = logging.getLogger(__name__)


class NoOpTrainingLoop(BaseTrainingLoop):
    r"""Implements a no-operation training loop.

    This class can be used to ignore the training loop in an engine.

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.loops.training import TrainingLoop
        >>> from gravitorch.testing import create_dummy_engine
        >>> engine = create_dummy_engine()
        >>> loop = NoOpTrainingLoop()
        >>> loop
        NoOpTrainingLoop()
        >>> loop.train(engine)
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def train(self, engine: BaseEngine) -> None:
        r"""Trains the model on the training dataset.

        It is a no-operation method.

        Args:
        ----
             engine (``BaseEngine``): Specifies the engine.
        """

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        pass

    def state_dict(self) -> dict[str, Any]:
        return {}
