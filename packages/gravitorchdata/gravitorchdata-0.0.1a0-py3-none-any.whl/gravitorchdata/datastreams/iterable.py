from __future__ import annotations

__all__ = ["IterableDataStream"]

import copy
import logging
from collections.abc import Iterable, Iterator
from typing import TypeVar

from gravitorchdata.datastreams.base import BaseDataStream

logger = logging.getLogger(__name__)

T = TypeVar("T")


class IterableDataStream(BaseDataStream[T]):
    r"""Implements a simple datastream for iterables.

    Args:
    ----
        iterable (``Iterable``): Specifies the iterable.
        deepcopy (bool, optional): If ``True``, the input iterable
            object is deep-copied before to iterate over the data.
            It allows a deterministic behavior when in-place
            operations are performed on the data. Default: ``False``

    Example usage:

    .. code-block:: pycon

        >>> from gravitorchdata.datastreams import IterableDataStream
        >>> with IterableDataStream([1, 2, 3, 4, 5]) as datastream:
        ...     for batch in datastream:
        ...         print(batch)  # do something
        ...
    """

    def __init__(self, iterable: Iterable[T], deepcopy: bool = False) -> None:
        if not isinstance(iterable, Iterable):
            raise TypeError(f"Incorrect type. Expecting iterable but received {type(iterable)}")
        self.iterable = iterable
        self._deepcopy = bool(deepcopy)

    def __iter__(self) -> Iterator[T]:
        iterable = self.iterable
        if self._deepcopy:  # TODO: move to launch
            logger.info("Copying the input iterable...")
            try:
                iterable = copy.deepcopy(iterable)
            except TypeError:
                logger.warning(
                    "The input iterable can not be deepcopied, please be aware of in-place "
                    "modification would affect source data."
                )
        yield from iterable

    def __len__(self) -> int:
        return len(self.iterable)

    def __repr__(self) -> str:
        try:
            extra = f"length={len(self.iterable):,}"
        except TypeError:
            extra = ""
        return f"{self.__class__.__qualname__}({extra})"

    def launch(self) -> None:
        r"""Nothing to do for this datastreams."""

    def shutdown(self) -> None:
        r"""Nothing to do for this datastreams."""
