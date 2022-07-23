"""Tests for module ``noxcollections.search``"""


from typing import Callable, Sequence

import pytest

from noxcollections.search import binary_search, search

not_implemented_annotation = pytest.mark.xfail(reason="Not implemented yet.")


@pytest.fixture(params=[binary_search])
def search_ordered(request) -> Callable:
    return request.param


@pytest.fixture(params=[search])
def search_no_assumptions(request) -> Callable:
    return request.param


@pytest.fixture(params=[binary_search])
def search_any(request) -> Callable:
    return request.param


# TODO: Replace comments about search type with custom marks

# ========== Tests for all search functions ==========


def test_binary_search_should_return_minus_1_for_an_empty_sequence(
    search_any: Callable,
):
    assert search_any([], 1) == -1


@pytest.mark.parametrize("searched_value", [-100, 100])
def test_binary_search_should_return_minus_1_for_not_present_element_even_len(
    search_any: Callable,
    searched_value: int,
):
    assert search_any(range(10), searched_value) == -1


@pytest.mark.parametrize("searched_value", [-100, 100])
def test_binary_search_should_return_minus_1_for_not_present_element_odd_len(
    search_any: Callable,
    searched_value: int,
):
    assert search_any(range(11), searched_value) == -1


@pytest.mark.parametrize("searched_value", range(10))
def test_binary_search_should_return_index_for_element_even_len(
    search_any: Callable,
    searched_value: int,
):
    assert search_any(range(10, 20), searched_value + 10) == searched_value


@pytest.mark.parametrize("searched_value", range(11))
def test_binary_search_should_return_index_for_element_odd_len(
    search_any: Callable,
    searched_value: int,
):
    assert search_any(range(10, 21), searched_value + 10) == searched_value


@pytest.mark.parametrize("searched_value", [-100, 100])
def test_binary_search_with_key_should_return_minus_1_for_not_present_element_even_len_(
    search_any: Callable,
    searched_value: int,
):
    assert search_any(range(10), searched_value, lambda x: x * 12) == -1


@pytest.mark.parametrize("searched_value", [-100, 100])
def test_binary_search_with_key_should_return_minus_1_for_not_present_element_odd_len_(
    search_any: Callable,
    searched_value: int,
):
    assert search_any(range(11), searched_value, lambda x: x * 12) == -1


@pytest.mark.parametrize("searched_value", range(10))
def test_binary_search_with_key_should_return_index_for_element_even_len(
    search_any: Callable,
    searched_value: int,
):
    assert search_any(range(10, 20), searched_value, lambda x: x - 10) == searched_value


@pytest.mark.parametrize("searched_value", range(11))
def test_binary_search_with_key_should_return_index_for_element_odd_len(
    search_any: Callable,
    searched_value: int,
):
    assert search_any(range(10, 21), searched_value, lambda x: x - 10) == searched_value


# ========== Tests for search functions without assumptions ==========


def _shuffled_lists_with_elements_0_to_9():
    return [
        [5, 7, 6, 3, 1, 0, 4, 8, 9, 2],
        [4, 3, 8, 6, 1, 5, 2, 0, 9, 7],
        [3, 1, 7, 8, 6, 5, 9, 4, 0, 2],
        [4, 0, 8, 1, 9, 2, 6, 3, 7, 5],
        [2, 0, 4, 8, 6, 1, 9, 7, 3, 5],
    ]


@not_implemented_annotation
@pytest.mark.parametrize("seq", _shuffled_lists_with_elements_0_to_9())
@pytest.mark.parametrize("value", range(10))
def test_search_should_return_index_of_searched(
    search_no_assumptions, seq: Sequence[int], value: int
):
    assert search_no_assumptions(seq, value) == seq.index(value)


@not_implemented_annotation
@pytest.mark.parametrize("seq", _shuffled_lists_with_elements_0_to_9())
@pytest.mark.parametrize("value", range(10))
def test_search_should_return_index_of_searched_element_when_using_key(
    search_no_assumptions, seq: Sequence[int], value: int
):
    assert search_no_assumptions(seq, value + 10, lambda x: x + 10) == seq.index(value)


@not_implemented_annotation
@pytest.mark.parametrize("seq", _shuffled_lists_with_elements_0_to_9())
@pytest.mark.parametrize("value", [100, -100])
def test_search_should_return_minus_1_for_items_not_in_the_sequence(
    search_no_assumptions, seq: Sequence[int], value: int
):
    assert search_no_assumptions(seq, value + 10) == -1


@not_implemented_annotation
@pytest.mark.parametrize("seq", _shuffled_lists_with_elements_0_to_9())
@pytest.mark.parametrize("value", range(10))
def test_search_should_return_minus_1_for_items_not_in_the_sequence_using_key(
    search_no_assumptions, seq: Sequence[int], value: int
):
    assert search_no_assumptions(seq, value, lambda x: x + 13) == -1
