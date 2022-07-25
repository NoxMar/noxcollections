"""Tests for module ``noxcollections.sort``"""

import pytest

from noxcollections.sort import bubble_sort, merge_sort

from typing import Callable, Sequence, TypeVar, Generator


T = TypeVar("T")


@pytest.fixture(params=[bubble_sort, merge_sort])
def sort_stable(request) -> Callable:
    return request.param


@pytest.fixture(params=[bubble_sort, merge_sort])
def sort_any(request) -> Callable:
    return request.param


@pytest.mark.parametrize(
    "to_sort",
    [
        [2],
        [1, 3],
        [2, 3],
        [1, 2, 4],
        [1, 4, 3],
        [2, 5, 5, 1],
        [2, 1, 3, 5],
        [3, 2, 2, 3, 3],
        [4, 6, 1, 5, 4],
        [7, 4, 6, 7, 2, 2],
        [7, 2, 3, 6, 4, 1],
        [6, 8, 5, 5, 6, 8, 5],
        [7, 8, 3, 8, 8, 4, 2],
        [2, 9, 4, 5, 8, 8, 2, 8],
        [9, 2, 6, 7, 8, 4, 6, 6],
        [4, 6, 1, 4, 4, 10, 8, 3, 4],
        [8, 8, 4, 2, 1, 2, 10, 6, 3],
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
        [4, 16, 20, 20, 18, 16, 16, 12, 20, 7, 15],
        [14, 11, 17, 8, 14, 5, 3, 13, 6, 1, 10],
        [3, 8, 12, 14, 17, 11, 19, 4, 13, 2, 7],
        [2, 4, 10, 4, 7, 14, 1, 2, 8, 14, 9],
        [6, 6, 4, 13, 19, 16, 14, 17, 3, 8, 2],
        [19, 14, 20, 20, 3, 13, 19, 6, 15, 10, 14],
        [5, 14, 6, 4, 8, 9, 15, 11, 1, 2, 20],
        [16, 10, 5, 9, 1, 8, 6, 11, 14, 19, 16],
        [7, 6, 8, 10, 15, 18, 3, 18, 18, 1, 8],
        [15, 16, 4, 19, 4, 4, 17, 17, 11, 5, 7],
    ],
)
@pytest.mark.parametrize("reverse", [True, False])
def test_sort_consistent_with_list_sort_method(
    sort_any, to_sort: Sequence[int], reverse: bool
):
    sorted_by_tested = to_sort[:]
    sort_any(sorted_by_tested, reverse=reverse)

    assert sorted_by_tested == sorted(to_sort, reverse=reverse)


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
        [4, 4, 5, 4, 4, 4, 5, 3, 5, 2, 5],
        [5, 4, 2, 1, 4, 2, 4, 6, 4, 2, 6],
        [1, 3, 6, 2, 5, 3, 4, 4, 1, 4, 3],
        [4, 1, 6, 1, 4, 2, 3, 4, 3, 3, 2],
        [2, 3, 1, 6, 2, 6, 4, 6, 4, 1, 2],
        [3, 2, 4, 1, 2, 2, 2, 4, 1, 5, 1],
        [5, 2, 3, 1, 2, 6, 4, 2, 1, 2, 4],
        [5, 4, 3, 6, 4, 2, 5, 6, 2, 3, 2],
        [4, 4, 5, 6, 3, 6, 2, 5, 6, 2, 2],
        [6, 2, 4, 2, 3, 5, 1, 1, 4, 5, 2],
    ]
    for li in lists:
        yield [_IntWithId(e) for e in li]


@pytest.mark.parametrize("to_sort", lists_ints_with_ids())
@pytest.mark.parametrize("reverse", [True, False])
def test_sort_is_stable(sort_stable, to_sort: Sequence[_IntWithId], reverse: bool):
    sorted_by_tested = to_sort[:]
    sort_stable(sorted_by_tested, reverse=reverse)

    assert sorted_by_tested == sorted(to_sort, reverse=reverse)
