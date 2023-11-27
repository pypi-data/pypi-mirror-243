from __future__ import annotations

__all__ = [
    "BaseEngineSaver",
    "BestEngineStateSaver",
    "BestHistorySaver",
    "EpochEngineStateSaver",
    "LastHistorySaver",
    "TagEngineStateSaver",
]

import logging
from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from coola.utils import str_indent, str_mapping

from gravitorch.distributed import comm as dist
from gravitorch.engines.events import EngineEvents
from gravitorch.handlers.base import BaseHandler
from gravitorch.handlers.utils import add_unique_event_handler
from gravitorch.utils.events import GEventHandler
from gravitorch.utils.history import get_best_values, get_last_values
from gravitorch.utils.io import save_pytorch
from gravitorch.utils.path import sanitize_path

if TYPE_CHECKING:
    from gravitorch.engines import BaseEngine

logger = logging.getLogger(__name__)


class BaseEngineSaver(BaseHandler):
    r"""Implements a base handler to save something about the engine.

    Note that it is not the only way to save something about the
    engine. Feel free to use another approaches if this approach does
    not fit your needs.

    The child class has to implement the ``_save`` method.

    Args:
    ----
        path (``pathlib.Path`` or str): Specifies the path to the
            folder where to save the artifacts.
        event (str): Specifies the event used to save the artifacts.
        only_main_process (bool, optional): If ``True``, only the
            main process saves the artifacts, otherwise
            all the processes save the artifacts.
            Default: ``True``
    """

    def __init__(
        self,
        path: Path | str,
        event: str,
        only_main_process: bool = True,
    ) -> None:
        self._path = sanitize_path(path)
        self._event = str(event)
        self._only_main_process = only_main_process

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "event": self._event,
                    "path": self._path,
                    "only_main_process": self._only_main_process,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def attach(self, engine: BaseEngine) -> None:
        add_unique_event_handler(
            engine=engine,
            event=self._event,
            event_handler=GEventHandler(self.save, handler_kwargs={"engine": engine}),
        )

    def save(self, engine: BaseEngine) -> None:
        r"""Saves the values associated to the histories.

        Args:
        ----
            engine (``BaseEngine``): Specifies the engine.
        """
        if self._only_main_process and not dist.is_main_process():
            return
        self._save(engine)

    @abstractmethod
    def _save(self, engine: BaseEngine) -> None:
        r"""Saves the values associated to the histories.

        Args:
        ----
            engine (``BaseEngine``): Specifies the engine.
        """


###################
#     History     #
###################


class BestHistorySaver(BaseEngineSaver):
    r"""Implements a handler to save the best history values in a PyTorch
    file.

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.handlers import BestHistorySaver
        >>> from gravitorch.testing import create_dummy_engine
        >>> engine = create_dummy_engine()
        >>> handler = BestHistorySaver(path="tmp/ckpt")
        >>> handler
        BestHistorySaver(
          (event): completed
          (path): .../tmp/ckpt
          (only_main_process): True
        )
        >>> handler.attach(engine)
        >>> engine.trigger_event("completed")  # doctest: +SKIP
    """

    def __init__(
        self,
        path: Path | str,
        event: str = EngineEvents.COMPLETED,
        only_main_process: bool = True,
    ) -> None:
        super().__init__(path=path, event=event, only_main_process=only_main_process)

    def _save(self, engine: BaseEngine) -> None:
        path = self._path.joinpath("history_best.pt")
        logger.info(f"Saving best history values in {path}")
        save_pytorch(get_best_values(engine.get_histories()), path)


class LastHistorySaver(BaseEngineSaver):
    r"""Implements a handler to save the last history values in a PyTorch
    file.

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.handlers import LastHistorySaver
        >>> from gravitorch.testing import create_dummy_engine
        >>> engine = create_dummy_engine()
        >>> handler = LastHistorySaver(path="tmp/ckpt")
        >>> handler
        LastHistorySaver(
          (event): epoch_completed
          (path): .../tmp/ckpt
          (only_main_process): True
        )
        >>> handler.attach(engine)
        >>> engine.trigger_event("epoch_completed")  # doctest: +SKIP
    """

    def __init__(
        self,
        path: Path | str,
        event: str = EngineEvents.EPOCH_COMPLETED,
        only_main_process: bool = True,
    ) -> None:
        super().__init__(path=path, event=event, only_main_process=only_main_process)

    def _save(self, engine: BaseEngine) -> None:
        path = self._path.joinpath("history_last.pt")
        logger.info(f"Saving last history values in {path}")
        save_pytorch(get_last_values(engine.get_histories()), path)


#################
#     state     #
#################


class BestEngineStateSaver(BaseEngineSaver):
    r"""Implements a handler to save the engine state dict in a PyTorch
    file.

    This handler saves the best checkpoint of a set of metrics.
    Internally, this handler uses the history to know if a
    metric has improved or not.

    Note it is usually recommended to save the state dict after the
    other handlers were run to capture the correct engine state.

    Args:
    ----
        path (``pathlib.Path`` or str): Specifies the path to the
            folder where to write the state dict.
        keys (tuple or list): Specifies the set of metrics to create
            the best checkpoint. Each key should be associated to a
            comparable history in the engine.
        event (str, optional): Specifies the event used to save the
            engine state dict. Default: ``'epoch_completed'``
        only_main_process (bool, optional): If ``True``, only the main
            process saves the engine state dict, otherwise all the
            processes save the engine state dict. Default: ``True``

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.handlers import BestEngineStateSaver
        >>> from gravitorch.testing import create_dummy_engine
        >>> engine = create_dummy_engine()
        >>> handler = BestEngineStateSaver(path="tmp/ckpt", keys=["eval/loss"])
        >>> handler
        BestEngineStateSaver(
          (event): epoch_completed
          (path): .../tmp/ckpt
          (keys): ('eval/loss',)
          (only_main_process): True
        )
        >>> handler.attach(engine)
        >>> engine.trigger_event("epoch_completed")  # doctest: +SKIP
    """

    def __init__(
        self,
        path: Path | str,
        keys: tuple[str, ...] | list[str],
        event: str = EngineEvents.EPOCH_COMPLETED,
        only_main_process: bool = True,
    ) -> None:
        super().__init__(path=path, event=event, only_main_process=only_main_process)
        self._keys = tuple(keys)

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "event": self._event,
                    "path": self._path,
                    "keys": self._keys,
                    "only_main_process": self._only_main_process,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def _save(self, engine: BaseEngine) -> None:
        r"""Saves the engine state dict in a PyTorch file.

        Args:
        ----
            engine (``BaseEngine``): Specifies the engine.
        """
        logger.info("Saving the best checkpoints according to some metrics...")
        for key in self._keys:
            if not engine.has_history(key):
                logger.warning(
                    f"Attempting to save the best state dict for '{key}' but there is no "
                    "history so this metric is skipped"
                )
                continue
            history = engine.get_history(key)
            if not history.is_comparable():
                logger.warning(
                    f"Attempting to save the best state dict for '{key}' but the history "
                    "is not comparable so this metric is skipped"
                )
                continue
            if history.is_empty():
                logger.warning(
                    f"Attempting to save the best state dict for '{key}' but the history "
                    "is empty so this metric is skipped"
                )
                continue
            if history.has_improved():
                logger.info(f"Saving 'best_{key}' engine state dict")
                save_pytorch(
                    engine.state_dict(),
                    self._path.joinpath(f"best_{key}/ckpt_engine_{dist.get_rank()}.pt"),
                )


class EpochEngineStateSaver(BaseEngineSaver):
    r"""Implements a handler to save the engine state dict in a PyTorch
    file.

    This engine state dict saver creates a new file for each epoch.

    Note it is usually recommended to save the state dict after the
    other handlers were run to capture the correct engine state.

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.handlers import EpochEngineStateSaver
        >>> from gravitorch.testing import create_dummy_engine
        >>> engine = create_dummy_engine()
        >>> handler = EpochEngineStateSaver(path="tmp/ckpt")
        >>> handler
        EpochEngineStateSaver(
          (event): epoch_completed
          (path): .../tmp/ckpt
          (only_main_process): True
        )
        >>> handler.attach(engine)
        >>> engine.trigger_event("epoch_completed")  # doctest: +SKIP
    """

    def __init__(
        self,
        path: Path | str,
        event: str = EngineEvents.EPOCH_COMPLETED,
        only_main_process: bool = True,
    ) -> None:
        super().__init__(path=path, event=event, only_main_process=only_main_process)

    def _save(self, engine: BaseEngine) -> None:
        r"""Saves the engine state dict in a PyTorch file.

        Args:
        ----
            engine (``BaseEngine``): Specifies the engine.
        """
        logger.info(f"Saving 'epoch {engine.epoch}' engine state dict")
        save_pytorch(
            engine.state_dict(),
            self._path.joinpath(f"epoch/ckpt_engine_{engine.epoch}_{dist.get_rank()}.pt"),
        )


class TagEngineStateSaver(BaseEngineSaver):
    r"""Implements a handler to save the engine state dict in a PyTorch
    file.

    This handler overrides the previous file everytime the ``save``
    method is called.

    Note it is usually recommended to save the state dict after the
    other handlers were run to capture the correct engine state.

    Args:
    ----
        path (``pathlib.Path`` or str): Specifies the path to the
            folder where to save the state dict.
        event (str, optional): Specifies the event used to save the
            engine state dict. Default: ``'epoch_completed'``
        tag (str, optional): Specifies the tag used to create the
            checkpoint name. Default: ``'last'``
        only_main_process (bool, optional): If ``True``, only the main
            process saves the engine state dict, otherwise all the
            processes save the engine state dict. Default: ``True``

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.handlers import TagEngineStateSaver
        >>> from gravitorch.testing import create_dummy_engine
        >>> engine = create_dummy_engine()
        >>> handler = TagEngineStateSaver(path="tmp/ckpt")
        >>> handler
        TagEngineStateSaver(
          (event): epoch_completed
          (path): .../tmp/ckpt
          (tag): last
          (only_main_process): True
        )
        >>> handler.attach(engine)
        >>> engine.trigger_event("epoch_completed")  # doctest: +SKIP
    """

    def __init__(
        self,
        path: Path | str,
        event: str = EngineEvents.EPOCH_COMPLETED,
        tag: str = "last",
        only_main_process: bool = True,
    ) -> None:
        super().__init__(path=path, event=event, only_main_process=only_main_process)
        self._tag = str(tag)

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "event": self._event,
                    "path": self._path,
                    "tag": self._tag,
                    "only_main_process": self._only_main_process,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def _save(self, engine: BaseEngine) -> None:
        logger.info(f"Saving '{self._tag}' engine state dict...")
        save_pytorch(
            engine.state_dict(),
            self._path.joinpath(f"{self._tag}/ckpt_engine_{dist.get_rank()}.pt"),
        )
