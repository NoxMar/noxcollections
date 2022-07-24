"""This module contains implementations of a few classical sorting algorithms.

These implementations **modify** the passed sequence.
"""

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def _should_swap_ascending(element_index_i, element_index_i_plus_1) -> bool:
    return element_index_i_plus_1 < element_index_i


def _should_swap_descending(element_index_i, element_index_i_plus_1) -> bool:
    return element_index_i < element_index_i_plus_1


def bubble_sort(seq: MutableSequence[T], *, reverse=False) -> None:
    """Sorts the sequence in place in the ascending order using bubble sort algorithm.

    The time complexity of this sorting is O(n^2). Elements of the sequence have to
    implement the ``<`` comparison between one another.

    Args:
        seq (MutableSequence[T]): MutableSequence to be sorted in place.
        reverse (bool, optional): If set to ``True`` sort in the descending order
            instead. Defaults to ``False``.
    """
    swap_criteria = _should_swap_ascending if not reverse else _should_swap_descending
    last_index = len(seq) - 1
    for i in range(last_index, 0, -1):
        any_swaps = False

        for j in range(i):
            if swap_criteria(seq[j], seq[j + 1]):
                seq[j], seq[j + 1] = seq[j + 1], seq[j]
                any_swaps = any_swaps or True

        if not any_swaps:
            break
