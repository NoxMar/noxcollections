"""Tests for module ``noxcollections.sort``"""

import pytest

from noxcollections.sort import bubble_sort

from typing import Callable, Sequence, TypeVar, Generator


pytestmark = pytest.mark.xfail(reason="Not implemented yet")

T = TypeVar("T")


@pytest.fixture(params=[bubble_sort])
def sort_stable(request) -> Callable:
    return request.param


@pytest.fixture(params=[bubble_sort])
def sort_any(request) -> Callable:
    return request.param


@pytest.mark.parametrize(
    "to_sort",
    [
        [20, 18, 11, 8, 5, 19, 3, 2, 15, 1],
        [18, 20, 20, 16, 11, 11, 3, 3, 3, 10],
        [10, 4, 17, 16, 16, 18, 20, 2, 16, 3],
        [17, 16, 11, 16, 15, 13, 12, 7, 4, 5],
        [10, 9, 12, 1, 9, 4, 16, 15, 13, 18],
        [16, 3, 19, 15, 16, 8, 1, 20, 17, 4],
        [20, 2, 15, 1, 2, 7, 2, 8, 6, 15],
        [9, 10, 9, 15, 6, 8, 17, 9, 16, 13],
        [18, 11, 9, 6, 17, 6, 12, 17, 18, 12],
        [9, 2, 15, 13, 7, 11, 10, 20, 6, 5],
    ],
)
def test_sort_consistent_with_list_sort_method(sort_any, to_sort: Sequence[int]):
    sorted_by_tested = to_sort[:]
    sort_any(sorted_by_tested)

    assert sorted_by_tested == sorted(to_sort)


class _IntWithId:
    _static_id = 0

    def __init__(self, value):
        self.value = value
        self.uid = self.__class__._static_id
        self.__class__._static_id += 1

    def __repr__(self):
        return f"({self.value}, id={self.uid})"

    def __lt__(self, other: object):
        if not isinstance(other, _IntWithId):
            raise NotImplementedError(
                "_IntWithId can be compared only against other instances"
            )
        return self.value < other.value

    def __eq__(self, other: object):
        if not isinstance(other, _IntWithId):
            raise NotImplementedError(
                "_IntWithId can be compared only against other instances"
            )
        return self.value == other.value and self.uid == other.uid


def lists_ints_with_ids() -> Generator[Sequence[_IntWithId], None, None]:
    lists = [
        [2, 1, 1, 1, 1, 2, 4, 4, 5, 5],
        [3, 4, 2, 4, 2, 2, 1, 5, 4, 2],
        [3, 5, 5, 5, 3, 2, 5, 2, 5, 5],
        [5, 3, 2, 5, 1, 3, 5, 5, 5, 1],
        [3, 4, 4, 3, 2, 4, 4, 5, 3, 2],
        [4, 2, 5, 2, 3, 1, 5, 3, 2, 3],
        [4, 1, 4, 4, 4, 1, 5, 1, 1, 5],
        [2, 4, 3, 5, 5, 5, 5, 4, 2, 5],
        [5, 5, 4, 1, 3, 1, 4, 5, 3, 2],
        [2, 3, 2, 2, 4, 3, 3, 2, 2, 4],
    ]
    for li in lists:
        yield [_IntWithId(e) for e in li]


@pytest.mark.parametrize("to_sort", lists_ints_with_ids())
def test_sort_is_stable(sort_stable, to_sort: Sequence[_IntWithId]):
    sorted_by_tested = to_sort[:]
    sort_stable(sorted_by_tested)

    assert sorted_by_tested == sorted(to_sort)
