"""Module containing tests for the classes from module ``lists``.

Performed tests check if the contract associated with the ``MutableSequence`` ABC in a
way equivalent with built-in ``list``. To put it simply it checks if the tested classes
behave in the same way as the built-in ``list``.

**To add another class** implementing ``MutableSequence`` in above specified manner
just add it the annotation on the ``TestMutableSequence`` class. This will cause all
test to be run against this class as well.
"""

from abc import ABC, abstractmethod

from typing import (
    MutableSequence,
    Callable,
    Iterable,
    Optional,
    Sequence,
    TypeVar,
    Tuple,
)

import pytest

from noxcollections.lists import LinkedList

from .util import are_iterables_equal, are_sequences_equal

T = TypeVar("T")

ListConstructor = Callable[[Optional[Iterable[T]]], MutableSequence]


@pytest.mark.parametrize("list_type", (LinkedList,))
class TestMutableSequence:
    pass


class TestSequenceConstructor(TestMutableSequence):
    def test_constructor_empty_has_len_0(self, list_type: ListConstructor):
        list_ = list_type(None)
        assert len(list_) == 0

    def test_constructor_empty_should_return_empty_iter(
        self, list_type: ListConstructor
    ):
        list_ = list_type(None)
        assert sum(1 for _ in list_) == 0


class TestSequenceIteration(TestMutableSequence):
    @pytest.mark.parametrize("iterable", [[], range(10), "abc"])
    def test_iter_is_consistent_with_passed_iter(
        self, list_type: ListConstructor, iterable: Sequence
    ):
        list_ = list_type(iterable)
        assert are_iterables_equal(list_, iterable)


def _parameters_for_not_rising_index_test() -> Iterable[Tuple[Iterable[int], int, int]]:
    return [
        (range(3), 0, 100),
        (range(3), 1, 100),
        (range(3), 2, 100),
        (range(10), -1, 100),
        (range(10), -2, 100),
    ]


class _TestIndexOperationConsistentWithList(TestMutableSequence, ABC):
    @abstractmethod
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        index: int,
        value: T,
    ) -> Optional[T]:
        pass

    @pytest.mark.parametrize(
        ("iterable", "index", "value"),
        _parameters_for_not_rising_index_test(),
    )
    def test_operation_result_is_consistent_with_builtin_list(
        self,
        list_type: ListConstructor,
        iterable: Iterable[T],
        index: int,
        value: T,
    ) -> None:
        builtin_list = list(iterable)
        list_ = list_type(iterable)

        reference_result = self._tested_operation(builtin_list, index, value)
        tested_result = self._tested_operation(list_, index, value)

        assert reference_result == tested_result

    @pytest.mark.parametrize(
        ("iterable", "index", "value"),
        _parameters_for_not_rising_index_test(),
    )
    def test_operation_state_after_is_consistent_with_builtin_list(
        self,
        list_type: ListConstructor,
        iterable: Iterable[T],
        index: int,
        value: T,
    ) -> None:
        builtin_list = list(iterable)
        list_ = list_type(iterable)

        self._tested_operation(builtin_list, index, value)
        self._tested_operation(list_, index, value)

        assert are_sequences_equal(builtin_list, list_)


class _TestIndexOperationThrowsWhenOutOfRange(TestMutableSequence, ABC):
    @abstractmethod
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        index: int,
        value: T,
    ) -> Optional[T]:
        pass

    @pytest.mark.parametrize(
        ("iterable", "index", "value"),
        [
            ((), 1, 100),
            ((), -1, 100),
            (range(10), 10, 100),
            (range(10), 100, 100),
            (range(10), -100, 100),
        ],
    )
    def test_operation_should_throw_for_index_out_range(
        self,
        list_type: ListConstructor,
        iterable: Iterable[T],
        index: int,
        value: T,
    ) -> None:
        list_ = list_type(iterable)

        with pytest.raises(IndexError):
            self._tested_operation(list_, index, value)


class _TestIndexOperationConsistentWithListAndThrows(
    _TestIndexOperationThrowsWhenOutOfRange, _TestIndexOperationConsistentWithList, ABC
):
    pass


def _parameters_for_slice_tests() -> Iterable[
    Tuple[Iterable[int], slice, Iterable[int]]
]:
    return [
        (range(10), slice(3), range(100, 103)),
        (range(10), slice(3, None), range(100, 107)),
        (range(10), slice(None, None, 2), range(100, 105)),
        (range(10), slice(None, None), range(100, 110)),
        (range(10), slice(3, 3), []),
        (range(10), slice(3, 4), [100]),
        (range(10), slice(2, 9, 3), range(100, 103)),
        (range(10), slice(-3), range(100, 107)),
        (range(10), slice(-9, -3), range(100, 106)),
        (range(10), slice(-3, -9), []),
        (range(10), slice(-8, -3, 2), range(100, 103)),
        (range(10), slice(-100, -3, 2), range(100, 104)),
        (range(10), slice(-100, 5, 3), range(100, 102)),
        (range(10), slice(3, -4, 2), range(100, 102)),
        (range(10), slice(None, None, -3), range(100, 104)),
        (range(10), slice(9, -1, -3), []),
        (range(10), slice(-5, None, -2), range(100, 103)),
    ]


class _TestSliceOperationConsistentWithList(TestMutableSequence, ABC):
    @abstractmethod
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        slice_: slice,
        values: Iterable[T],
    ) -> Optional[MutableSequence[T]]:
        pass

    @pytest.mark.parametrize(
        ("iterable", "slice_", "values"), _parameters_for_slice_tests()
    )
    def test_state_is_consistent_with_builtin_list(
        self,
        list_type: ListConstructor,
        iterable: Iterable[T],
        slice_: slice,
        values: Iterable[T],
    ) -> None:
        builtin_list = list(iterable)
        list_ = list_type(iterable)

        self._tested_operation(builtin_list, slice_, values)
        self._tested_operation(list_, slice_, values)

        assert are_sequences_equal(builtin_list, list_)

    @pytest.mark.parametrize(
        ("iterable", "slice_", "values"), _parameters_for_slice_tests()
    )
    def test_operation_result_is_consistent_with_builtin_list(
        self,
        list_type: ListConstructor,
        iterable: Iterable[T],
        slice_: slice,
        values: Iterable[T],
    ) -> None:
        builtin_list = list(iterable)
        list_ = list_type(iterable)

        reference_result = self._tested_operation(builtin_list, slice_, values)
        tested_result = self._tested_operation(list_, slice_, values)

        if reference_result is None or tested_result is None:
            assert reference_result is None and tested_result is None
            return

        assert are_sequences_equal(reference_result, tested_result)


class TestGetItemForIndexConsistentWithList(
    _TestIndexOperationConsistentWithListAndThrows
):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        index: int,
        value: T,
    ) -> Optional[T]:
        return seq[index]


@pytest.mark.xfail(reason="Not implemented yet")
class TestGetItemForSliceConsistentWithList(_TestSliceOperationConsistentWithList):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        slice_: slice,
        values: Iterable[T],
    ) -> Optional[MutableSequence[T]]:
        return seq[slice_]


class TestSetItemForIndexConsistentWithList(
    _TestIndexOperationConsistentWithListAndThrows
):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        index: int,
        value: T,
    ) -> Optional[T]:
        seq[index] = value
        return None


@pytest.mark.xfail(reason="Not implemented yet")
class TestSetItemForSliceConsistentWithList(_TestSliceOperationConsistentWithList):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        slice_: slice,
        values: Iterable[T],
    ) -> Optional[MutableSequence[T]]:
        seq[slice_] = values
        return None


class TestDelItemForIndexConsistentWithList(
    _TestIndexOperationConsistentWithListAndThrows
):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        index: int,
        value: T,
    ) -> Optional[T]:
        del seq[index]
        return None


@pytest.mark.xfail(reason="Not implemented yet")
class TestDelItemForSliceConsistentWithList(_TestSliceOperationConsistentWithList):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        slice_: slice,
        values: Optional[Iterable[T]],
    ) -> None:
        del seq[slice_]


@pytest.mark.xfail(reason="Bug for indexes out of range")
class TestInsertConsistentWithList(_TestIndexOperationConsistentWithList):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        index: int,
        value: T,
    ) -> None:
        seq.insert(index, value)


@pytest.mark.parametrize("iterable", [None, [], range(10), "abc"])
class TestSequenceClear(TestMutableSequence):
    def test_clear_operation_should_result_in_length_zero(
        self, list_type: ListConstructor, iterable: Optional[Iterable]
    ):
        list_ = list_type(iterable)
        list_.clear()

        assert len(list_) == 0

    def test_clear_operation_should_result_in_empty_sequence(
        self, list_type: ListConstructor, iterable: Optional[Iterable]
    ):
        list_ = list_type(iterable)
        list_.clear()

        assert are_sequences_equal(list_, [])


class TestSequencePop(_TestIndexOperationConsistentWithListAndThrows):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        index: int,
        values: Optional[T],
    ) -> Optional[T]:
        return seq.pop(index)

    def test_pop_zero_arg_from_empty_sequence_should_throw(
        self, list_type: ListConstructor
    ):
        list_ = list_type(None)

        with pytest.raises(IndexError):
            list_.pop()

    @pytest.mark.parametrize(
        ("iterable", "index"),
        [([], 0), ([], 1), (range(10), 10), (range(10), 100), (range(10), -11)],
    )
    def test_pop_out_of_range_should_throw(
        self, list_type: ListConstructor, iterable: Iterable, index: int
    ):
        list_ = list_type(iterable)

        with pytest.raises(IndexError):
            list_.pop(index)

    @pytest.mark.parametrize("seq", [[], range(1), range(10), "abc"])
    def test_pop_zero_arg_should_return_all_items_in_reverse_order(
        self, list_type: ListConstructor, seq: Sequence[T]
    ):
        def reverse_using_pop(seq_: MutableSequence[T]) -> Iterable[T]:
            try:
                while True:
                    yield seq_.pop()
            except IndexError:
                pass

        list_ = list_type(seq)

        assert are_iterables_equal(reversed(seq), reverse_using_pop(list_))


class TestSequenceAppendOnce(_TestIndexOperationConsistentWithList):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        index: int,
        value: T,
    ) -> Optional[T]:
        seq.append(value)
        return None


class TestSequenceAppendMultipleTimes(_TestSliceOperationConsistentWithList):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        slice_: slice,
        values: Iterable[T],
    ) -> None:
        for v in values:
            seq.append(v)


class TestSequenceExtend(_TestSliceOperationConsistentWithList):
    def _tested_operation(
        self,
        seq: MutableSequence[T],
        slice_: slice,
        values: Iterable[T],
    ) -> None:
        seq.extend(values)
