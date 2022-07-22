"""Tests for module ``noxcollections.search``"""


from noxcollections.search import binary_search

import pytest


def test_binary_search_should_return_minus_1_for_an_empty_sequence():
    assert binary_search([], 1) == -1


@pytest.mark.parametrize("searched_value", [-100, 100])
def test_binary_search_should_return_minus_1_for_not_present_element_even_len(
    searched_value: int,
):
    assert binary_search(range(10), searched_value) == -1


@pytest.mark.parametrize("searched_value", [-100, 100])
def test_binary_search_should_return_minus_1_for_not_present_element_odd_len(
    searched_value: int,
):
    assert binary_search(range(11), searched_value) == -1


@pytest.mark.parametrize("searched_value", range(10))
def test_binary_search_should_return_index_for_element_even_len(
    searched_value: int,
):
    assert binary_search(range(10, 20), searched_value + 10) == searched_value


@pytest.mark.parametrize("searched_value", range(11))
def test_binary_search_should_return_index_for_element_odd_len(
    searched_value: int,
):
    assert binary_search(range(10, 21), searched_value + 10) == searched_value


@pytest.mark.parametrize("searched_value", [-100, 100])
def test_binary_search_with_key_should_return_minus_1_for_not_present_element_even_len_(
    searched_value: int,
):
    assert binary_search(range(10), searched_value, lambda x: x * 12) == -1


@pytest.mark.parametrize("searched_value", [-100, 100])
def test_binary_search_with_key_should_return_minus_1_for_not_present_element_odd_len_(
    searched_value: int,
):
    assert binary_search(range(11), searched_value, lambda x: x * 12) == -1


@pytest.mark.parametrize("searched_value", range(10))
def test_binary_search_with_key_should_return_index_for_element_even_len(
    searched_value: int,
):
    assert (
        binary_search(range(10, 20), searched_value, lambda x: x - 10) == searched_value
    )


@pytest.mark.parametrize("searched_value", range(11))
def test_binary_search_with_key_should_return_index_for_element_odd_len(
    searched_value: int,
):
    assert (
        binary_search(range(10, 21), searched_value, lambda x: x - 10) == searched_value
    )
