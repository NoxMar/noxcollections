"""This module contains implementations of a few classical sorting algorithms.

These implementations **modify** the passed sequence.
"""

from typing import MutableSequence, TypeVar, Callable, cast, Optional

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


def _merge(
    left: MutableSequence[T],
    right: MutableSequence[T],
    should_swap_func: Callable[[T, T], bool],
) -> MutableSequence[T]:
    i_left = i_right = i_result = 0

    result: MutableSequence[Optional[T]] = [None] * (len(left) + len(right))

    while i_left < len(left) and i_right < len(right):
        if not should_swap_func(left[i_left], right[i_right]):
            result[i_result] = left[i_left]
            i_left += 1
        else:
            result[i_result] = right[i_right]
            i_right += 1
        i_result += 1

    for e in left[i_left:]:
        result[i_result] = e
        i_result += 1

    for e in right[i_right:]:
        result[i_result] = e
        i_result += 1

    return cast(MutableSequence[T], result)


def _merge_sorted(
    seq: MutableSequence[T], should_swap_func: Callable[[T, T], bool]
) -> MutableSequence[T]:
    if len(seq) <= 1:
        return seq

    if len(seq) == 2:
        if should_swap_func(seq[0], seq[1]):
            seq.reverse()
        return seq

    last_left = (len(seq) - 1) // 2
    left, right = seq[: last_left + 1], seq[last_left + 1 :]

    return _merge(
        _merge_sorted(left, should_swap_func),
        _merge_sorted(right, should_swap_func),
        should_swap_func,
    )


def merge_sort(seq: MutableSequence[T], *, reverse: bool = False) -> None:
    """Sorts a sequence using merge sort algorithm in O(n log2(n)) using O(n) aux space.

    Sorting is done in **stable** manner. Elements of the sequence have to implement
    the ``<`` comparison between one another.

    Args:
        seq (MutableSequence[T]): MutableSequence to be sorted in place.
        reverse (bool, optional): If set to ``True`` sort in the descending order
            instead. Defaults to ``False``.
    """
    swap_criteria = _should_swap_ascending if not reverse else _should_swap_descending
    seq[:] = _merge_sorted(seq, swap_criteria)
