"""Test for testing utility functions from ``tests/util.py``."""

from typing import Iterable, Sequence, TypeVar

import pytest

from .util import are_iterables_equal, are_sequences_equal

T = TypeVar("T")


def _get_empty_iterables() -> Iterable[Iterable]:
    return range(0), [], ()


class TestAreSequencesEqual:
    def _tested_functions(self, seq1: Sequence[T], seq2: Sequence[T]) -> bool:
        return are_sequences_equal(seq1, seq2)

    @pytest.mark.parametrize("empty_iter1", _get_empty_iterables())
    @pytest.mark.parametrize("empty_iter2", _get_empty_iterables())
    def test_should_return_true_empty_iterables(
        self, empty_iter1: Iterable, empty_iter2: Iterable
    ):
        assert are_iterables_equal(empty_iter1, empty_iter2)

    @pytest.mark.parametrize(
        ("iter1", "iter2"),
        [([1], [2]), ([1, 2], [2, 3]), (range(100), range(100, 200))],
    )
    def test_should_return_false_for_different_items_same_length(
        self, iter1: Iterable, iter2: Iterable
    ):
        assert not are_iterables_equal(iter1, iter2)

    @pytest.mark.parametrize(
        ("iter1", "iter2"),
        [([0], (0,)), ((0, 1, 2), range(3)), (range(5), [0, 1, 2, 3, 4])],
    )
    def test_iterables_of_different_types_and_same_elements_should_return_true(
        self, iter1: Iterable, iter2: Iterable
    ):
        assert are_iterables_equal(iter1, iter2)
        assert are_iterables_equal(iter2, iter1)

    @pytest.mark.parametrize(
        ("iter1", "iter2"),
        [((), (0,)), ((0,), (0, 1)), ((0, 1), (0,)), (range(5), range(10))],
    )
    def test_should_return_false_if_one_iterable_is_prefix_of_another(
        self, iter1: Iterable, iter2: Iterable
    ):
        assert not are_iterables_equal(iter1, iter2)


class TestAreIterablesEqual(TestAreSequencesEqual):
    def _tested_functions(self, iter1: Iterable[T], iter2: Iterable[T]) -> bool:
        return are_iterables_equal(iter1, iter2)
