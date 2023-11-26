from __future__ import annotations

__all__ = ["FixedSizePartitioner"]

from collections.abc import Sequence
from typing import TypeVar

from gravitorch.data.partitioners.base import BasePartitioner
from gravitorch.engines import BaseEngine
from gravitorch.utils.partitioning import fixed_size_partitions

T = TypeVar("T")


class FixedSizePartitioner(BasePartitioner[T]):
    r"""Implements a partitioner that creates fixed-size partitions.

    Args:
    ----
        partition_size (int): Specifies the partition size i.e. the
            number of items in each partition.
        drop_last (bool, optional): If ``True``, it drops the last
            items if the number of items is not evenly divisible by
            ``partition_size``.

    Example usage:

    .. code-block:: pycon

        >>> from gravitorch.data.partitioners import FixedSizePartitioner
        >>> partitioner = FixedSizePartitioner(partition_size=3)
        >>> partitioner
        FixedSizePartitioner(partition_size=3, drop_last=False)
        >>> partitions = partitioner.partition(list(range(10)))
        >>> partitions
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """

    def __init__(self, partition_size: int, drop_last: bool = False) -> None:
        self._partition_size = int(partition_size)
        self._drop_last = bool(drop_last)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}("
            f"partition_size={self._partition_size:,}, drop_last={self._drop_last})"
        )

    @property
    def drop_last(self) -> bool:
        r"""``bool``: Indicates if the last items are dropped or not if
        there are not enough items."""
        return self._drop_last

    @property
    def partition_size(self) -> int:
        r"""``int``: The partition size."""
        return self._partition_size

    def partition(self, items: Sequence[T], engine: BaseEngine | None = None) -> list[Sequence[T]]:
        return fixed_size_partitions(
            items=items, partition_size=self._partition_size, drop_last=self._drop_last
        )
