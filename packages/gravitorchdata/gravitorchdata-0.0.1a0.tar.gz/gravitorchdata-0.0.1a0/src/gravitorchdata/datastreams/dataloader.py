from __future__ import annotations

__all__ = ["DataLoaderDataStream"]

from collections.abc import Iterator

from torch.utils.data import DataLoader
from torchdata.dataloader2 import DataLoader2

from gravitorchdata.datastreams.base import BaseDataStream


class DataLoaderDataStream(BaseDataStream):
    r"""Implements a simple datastream for PyTorch data loaders.

    Args:
        dataloader (``DataLoader`` or ``DataLoader2``): Specifies the
            data loader.

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from torch.utils.data import DataLoader, TensorDataset
        >>> from gravitorchdata.datastreams import IterableDataStream
        >>> dataloader = DataLoader(TensorDataset(torch.arange(10)), batch_size=4)
        >>> with DataLoaderDataStream(dataloader) as datastream:
        ...     for batch in datastream:
        ...         print(batch)  # do something
        ...
    """

    def __init__(self, dataloader: DataLoader | DataLoader2) -> None:
        if not isinstance(dataloader, (DataLoader, DataLoader2)):
            raise TypeError(
                "Incorrect type. Expecting DataLoader or DataLoader2 but "
                f"received {type(dataloader)}"
            )
        self.dataloader = dataloader

    def __iter__(self) -> Iterator:
        return iter(self.dataloader)

    def __len__(self) -> int:
        return len(self.dataloader)

    def __repr__(self) -> str:
        try:
            extra = f"length={len(self.dataloader):,}"
        except TypeError:
            extra = ""
        return f"{self.__class__.__qualname__}({extra})"

    def launch(self) -> None:
        r"""Nothing to do for this datastream."""

    def shutdown(self) -> None:
        if isinstance(self.dataloader, DataLoader2):
            self.dataloader.shutdown()
