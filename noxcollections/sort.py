"""This module contains implementations of a few classical sorting algorithms.

These implementations **modify** the passed sequence.
"""

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def bubble_sort(seq: MutableSequence[T], *, reverse=False) -> None:
    """Sorts the sequence in place in the ascending order using bubble sort algorithm.

    The time complexity of this sorting is O(n^2). Elements of the sequence have to
    implement the ``<`` comparison between one another.

    Args:
        seq (MutableSequence[T]): MutableSequence to be sorted in place.
        reverse (bool, optional): If set to ``True`` sort in the descending order
            instead. Defaults to ``False``.
    """
    raise NotImplementedError()
