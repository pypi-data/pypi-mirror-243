from __future__ import annotations

__all__ = ["DictBatcherIterDataPipe", "TupleBatcherIterDataPipe"]

import logging
from collections.abc import Hashable, Iterator, Sequence

import torch
from coola import summary
from coola.utils import str_indent, str_mapping
from torch import Tensor
from torch.utils.data import IterDataPipe

from gravitorch.datapipes.iter.shuffling import shuffle_tensor_mapping, shuffle_tensors
from gravitorch.datapipes.iter.source import SourceWrapperIterDataPipe
from gravitorch.utils.mapping import get_first_value
from gravitorch.utils.seed import get_torch_generator

logger = logging.getLogger(__name__)


class DictBatcherIterDataPipe(IterDataPipe[dict]):
    r"""Implements a source DataPipe to generate batch of examples from a
    dictionary of ``torch.Tensor``s.

    Args:
    ----
        data (dict): Specifies a dictionary with the data. The
            generated batches have the same structure that this input.
        batch_size (int): Specifies the batch size.
        shuffle (bool, optional): If ``True``, the examples are
            shuffled before to create the batches. Default: ``False``
        random_seed (int, optional): Specifies the random seed used to
            shuffle the data. Default: ``11918852809641073385``

    Example usage:

    .. code-block:: pycon

        >>> from pathlib import Path
        >>> from torch.utils.data.datapipes.iter import IterableWrapper
        >>> from gravitorch.datapipes.iter import DictBatcher
        >>> dp = DictBatcher(
        ...     IterableWrapper(
        ...         [
        ...             {"key1": torch.randn(4), "key2": torch.randn(4, 6)},
        ...             {"key1": torch.randn(6), "key2": torch.randn(6, 8)},
        ...         ]
        ...     ),
        ...     batch_size=3,
        ... )
        >>> dp
        DictBatcherIterDataPipe(
          (batch_size): 3
          (shuffle): False
          (random_seed): 11918852809641073385
          (datapipe_or_data): IterableWrapperIterDataPipe
        )
        >>> list(dp)
        [{'key1': tensor([...]), 'key2': tensor([[...]])},
         {'key1': tensor([...]), 'key2': tensor([[...]])},
         {'key1': tensor([...]), 'key2': tensor([[...]])},
         {'key1': tensor([...]), 'key2': tensor([[...]])}]
    """

    def __init__(
        self,
        datapipe_or_data: IterDataPipe[dict[Hashable, Tensor]] | dict[Hashable, Tensor],
        batch_size: int,
        shuffle: bool = False,
        random_seed: int = 11918852809641073385,
    ) -> None:
        self._datapipe_or_data = datapipe_or_data
        self._batch_size = int(batch_size)
        self._shuffle = bool(shuffle)
        self._generator = get_torch_generator(random_seed)

    def __iter__(self) -> Iterator[dict]:
        datapipe_or_data = self._datapipe_or_data
        if not isinstance(datapipe_or_data, IterDataPipe):
            datapipe_or_data = SourceWrapperIterDataPipe([datapipe_or_data])
        for batch in datapipe_or_data:
            if self._shuffle:
                batch = shuffle_tensor_mapping(batch, generator=self._generator)
            keys = batch.keys()
            for tensors in zip(*[torch.split(value, self._batch_size) for value in batch.values()]):
                yield {key: tensor for key, tensor in zip(keys, tensors)}

    def __len__(self) -> int:
        if isinstance(self._datapipe_or_data, IterDataPipe):
            raise TypeError(f"{type(self).__qualname__} instance doesn't have valid length")
        return (
            get_first_value(self._datapipe_or_data).shape[0] + self._batch_size - 1
        ) // self._batch_size

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        datapipe_or_data = (
            str(self._datapipe_or_data)
            if isinstance(self._datapipe_or_data, IterDataPipe)
            else summary(self._datapipe_or_data)
        )
        args = str_indent(
            str_mapping(
                {
                    "batch_size": self._batch_size,
                    "shuffle": self._shuffle,
                    "random_seed": self.random_seed,
                    "datapipe_or_data": datapipe_or_data,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __getstate__(self) -> dict:
        state = super().__getstate__().copy()
        # torch.Generator cannot be serialized but its state can.
        state["_generator"] = state["_generator"].get_state()
        return state

    def __setstate__(self, state: dict) -> None:
        # Recreate the torch.Generator because only its state was serialized
        generator = torch.Generator()
        state["_generator"] = generator.set_state(state["_generator"])
        self.__dict__.update(state)

    @property
    def random_seed(self) -> int:
        r"""``int``: The random seed used to initialize the pseudo
        random generator."""
        return self._generator.initial_seed()


class TupleBatcherIterDataPipe(IterDataPipe[tuple[Tensor, ...]]):
    r"""Implements a source DataPipe to generate batch of examples from a
    tuple of ``torch.Tensor``s.

    Args:
    ----
        datapipe_or_data (``IterDataPipe`` or sequence of
            ``torch.Tensor`` of shape ``(num_examples, *)`` where ``*``
            means any number of dimensions): Specifies source DataPipe
            or a sequence of tensors.
        batch_size (int): Specifies the batch size.
        shuffle (bool, optional): If ``True``, the examples are
            shuffled before to create the batches. The
            shuffling is done per sequence of tensors.
            Default: ``False``
        random_seed (int, optional): Specifies the random seed used to
            shuffle the data. Default: ``13382866045483866228``

    Example usage:

    .. code-block:: pycon

        >>> from pathlib import Path
        >>> from torch.utils.data.datapipes.iter import IterableWrapper
        >>> from gravitorch.datapipes.iter import TupleBatcher
        >>> dp = TupleBatcher(
        ...     IterableWrapper(
        ...         [(torch.randn(4), torch.randn(4, 6)), (torch.randn(6), torch.randn(6, 8))]
        ...     ),
        ...     batch_size=3,
        ... )
        >>> dp
        TupleBatcherIterDataPipe(
          batch_size=3,
          shuffle=False,
          random_seed=13382866045483866228,
          datapipe_or_data=IterableWrapperIterDataPipe,
        )
        >>> list(dp)
        [(tensor([...]), tensor([[...]])),
         (tensor([...]), tensor([[...]])),
         (tensor([...]), tensor([[...]])),
         (tensor([...]), tensor([[...]]))]
    """

    def __init__(
        self,
        datapipe_or_data: IterDataPipe[Sequence[Tensor]] | Sequence[Tensor],
        batch_size: int,
        shuffle: bool = False,
        random_seed: int = 13382866045483866228,
    ) -> None:
        self._datapipe_or_data = datapipe_or_data
        self._batch_size = int(batch_size)
        self._shuffle = bool(shuffle)
        self._generator = get_torch_generator(random_seed)

    def __iter__(self) -> Iterator[tuple[Tensor, ...]]:
        datapipe_or_tensors = self._datapipe_or_data
        if not isinstance(datapipe_or_tensors, IterDataPipe):
            datapipe_or_tensors = SourceWrapperIterDataPipe([datapipe_or_tensors])
        for batch in datapipe_or_tensors:
            if self._shuffle:
                batch = shuffle_tensors(batch, generator=self._generator)
            yield from zip(*[torch.split(tensor, self._batch_size) for tensor in batch])

    def __len__(self) -> int:
        if isinstance(self._datapipe_or_data, IterDataPipe):
            raise TypeError(f"{type(self).__qualname__} instance doesn't have valid length")
        return (self._datapipe_or_data[0].shape[0] + self._batch_size - 1) // self._batch_size

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        desc = (
            str(self._datapipe_or_data)
            if isinstance(self._datapipe_or_data, IterDataPipe)
            else summary(self._datapipe_or_data)
        )
        return (
            f"{self.__class__.__qualname__}(\n"
            f"  batch_size={self._batch_size},\n"
            f"  shuffle={self._shuffle},\n"
            f"  random_seed={self.random_seed},\n"
            f"  datapipe_or_data={str_indent(desc)},\n)"
        )

    def __getstate__(self) -> dict:
        state = super().__getstate__().copy()
        # torch.Generator cannot be serialized but its state can.
        state["_generator"] = state["_generator"].get_state()
        return state

    def __setstate__(self, state: dict) -> None:
        # Recreate the torch.Generator because only its state was serialized
        generator = torch.Generator()
        state["_generator"] = generator.set_state(state["_generator"])
        self.__dict__.update(state)

    @property
    def random_seed(self) -> int:
        r"""``int``: The random seed used to initialize the pseudo
        random generator."""
        return self._generator.initial_seed()
