"""Module contains functions for searching (checking if value exists) in specific
collection types. Some algorithms have additional requirements which are mentioned in
their documentation"""


from typing import TypeVar, Sequence, Callable, overload

T = TypeVar("T")
S = TypeVar("S")


def identity(arg: T) -> T:
    return arg


@overload
def binary_search(seq: Sequence[T], value: T) -> int:
    ...


@overload
def binary_search(seq: Sequence[T], value: S, key: Callable[[T], S]) -> int:
    ...


def binary_search(seq: Sequence[T], value: S, key: Callable = identity) -> int:
    """Returns the first index of ``value`` in a **sorted sequence** in O(log2(n)) time.

    Sequence needs to be sorted in ascending order (with possible repeats). If no
    instances of ``value`` are found ``-1`` is returned. Callable ``key`` can be
    optionally provided to map elements of sequence. If ``key`` is provided
    the sequence **must be ordered by the results of applying key to them**(``key(e)``).

    Args:
        seq (Sequence[T]): Sequence of elements sorted in **increasing order**.
        value (S): Value of which the index is to be found.
        key (Callable[[T], S], optional): If provided, the search is performed
            for the element of which ``key(e) == value``.

    Returns:
        int: Index of the first occurrence of the ``value`` or ``-1`` if no instances
            are found.
    """
    left = 0
    right = len(seq) - 1

    while left <= right:
        middle = (left + right) // 2
        middle_value = key(seq[middle])

        if middle_value == value:
            return middle

        if middle_value < value:
            left = middle + 1
        else:
            right = middle - 1

    return -1
