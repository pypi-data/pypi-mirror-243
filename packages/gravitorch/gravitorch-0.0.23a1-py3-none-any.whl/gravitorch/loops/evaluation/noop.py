r"""This module implements a no-operation evaluation loop."""

from __future__ import annotations

__all__ = ["NoOpEvaluationLoop"]

import logging
from typing import Any

from gravitorch.engines.base import BaseEngine
from gravitorch.loops.evaluation.base import BaseEvaluationLoop

logger = logging.getLogger(__name__)


class NoOpEvaluationLoop(BaseEvaluationLoop):
    r"""Implements a no-operation evaluation loop.

    This class can be used to ignore the evaluation loop in an engine.

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.loops.evaluation import EvaluationLoop
        >>> from gravitorch.testing import create_dummy_engine
        >>> engine = create_dummy_engine()
        >>> loop = NoOpEvaluationLoop()
        >>> loop
        NoOpEvaluationLoop()
        >>> loop.eval(engine)
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def eval(self, engine: BaseEngine) -> None:
        r"""Evaluates the model on the evaluation dataset.

        It is a no-operation method.

        Args:
        ----
            engine (``BaseEngine``): Specifies the engine.
        """

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        pass

    def state_dict(self) -> dict[str, Any]:
        return {}
