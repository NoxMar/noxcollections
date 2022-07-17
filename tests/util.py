"""Utility functions used only in tests."""

from itertools import zip_longest

from typing import Iterable, TypeVar, Sequence

T = TypeVar("T")


def are_iterables_equal(iter1: Iterable[T], iter2: Iterable[T]) -> bool:
    """Compares iterables element-wise. Compares using ``!=`` operator.

    Elements are accessed trough iterator. To be considered equal they also have
    to have the same length."""
    null_obj = object()
    iter1, iter2 = iter(iter1), iter(iter2)
    for e1, e2 in zip_longest(iter1, iter2, fillvalue=null_obj):
        if e1 != e2:
            return False
    return True


def are_sequences_equal(seq1: Sequence[T], seq2: Sequence[T]) -> bool:
    """Compares sequences (list-like objects) element-wise.

    Sequences are considered equal if they have the same length and equal elements at
    the same indexes. Compares using ``!=`` operator. Elements are accessed trough
    ``__getitem__`` protocol."""
    if len(seq1) != len(seq2):
        return False

    length = len(seq1)
    for i in range(length):
        if seq1[i] != seq2[i]:
            return False

    return True
