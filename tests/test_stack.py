from typing import TypeVar, Sequence, Generator

import pytest

from noxcollections.stack import Stack, StackABC

T = TypeVar("T")


def sequence_types():
    yield list


def exhaust_stack_using_pop(stack: StackABC[T]) -> Generator[T, None, None]:
    while stack:
        yield stack.pop()


@pytest.mark.parametrize("sequence_factory", sequence_types())
@pytest.fixture(params=sequence_types())
def empty_stack(request) -> Stack:
    return Stack(sequence_factory=request.param)


def two_plus_element_sequences() -> Generator[Sequence[int], None, None]:
    yield (1, 2)
    yield range(10)
    yield [1, 2, 100]


def all_sequences() -> Generator[Sequence[int], None, None]:
    yield []
    yield from two_plus_element_sequences()


def test_empty_stack_has_len_0(empty_stack: StackABC):
    stack = empty_stack

    assert len(stack) == 0


@pytest.mark.parametrize("seq", all_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_length_of_the_stack_consistent_with_passed_iterable(
    sequence_factory, seq: Sequence[int]
):
    stack = Stack(seq, sequence_factory)

    assert len(stack) == len(seq)


def test_top_from_empty_stack_raises(empty_stack: StackABC) -> None:
    stack = empty_stack

    with pytest.raises(IndexError):
        stack.top()


@pytest.mark.parametrize("seq", two_plus_element_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_top_from_not_empty_stack_returns_last_element(
    sequence_factory, seq: Sequence[int]
):
    stack = Stack(seq, sequence_factory)
    assert stack.top() == seq[-1]


@pytest.mark.parametrize("seq", two_plus_element_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_top_from_not_empty_stack_does_not_remove_top_element(
    sequence_factory, seq: Sequence[int]
):
    stack = Stack(seq, sequence_factory)
    stack.top()
    assert stack.top() == seq[-1]


def test_pop_from_empty_stack_raises(empty_stack: StackABC) -> None:
    stack = empty_stack

    with pytest.raises(IndexError):
        stack.pop()


@pytest.mark.parametrize("seq", two_plus_element_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_pop_from_not_empty_stack_returns_the_last_element(
    sequence_factory, seq: Sequence[int]
):
    stack = Stack(seq, sequence_factory)

    assert stack.pop() == seq[-1]


@pytest.mark.parametrize("seq", two_plus_element_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_pop_from_not_empty_stack_removes_the_last_element(
    sequence_factory, seq: Sequence[int]
):
    stack = Stack(seq, sequence_factory)
    stack.pop()

    assert len(stack) == len(seq) - 1
    assert stack.top() == seq[-2]


def test_peek_returns_default_for_empty_stack(empty_stack: StackABC):
    assert empty_stack.peek() is None


@pytest.mark.parametrize("seq", two_plus_element_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_peek_returns_top_for_not_empty_stack(sequence_factory, seq: Sequence[int]):
    stack = Stack(seq, sequence_factory)

    assert stack.peek() == seq[-1]


@pytest.mark.parametrize("seq", two_plus_element_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_peek_returns_does_not_remove_top_element(sequence_factory, seq: Sequence[int]):
    stack = Stack(seq, sequence_factory)
    stack.peek()

    assert len(stack) == len(seq)
    assert stack.top() == seq[-1]


@pytest.mark.parametrize("seq", all_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_push_should_put_element_on_the_stack(sequence_factory, seq: Sequence[int]):
    new_top = -1234
    stack = Stack(seq, sequence_factory)
    stack.push(new_top)

    assert stack.top() == new_top


@pytest.mark.parametrize("seq", all_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_push_should_increment_stack_size(sequence_factory, seq: Sequence[int]):
    stack = Stack(seq, sequence_factory)
    stack.push(-1234)

    assert len(stack) == len(seq) + 1


def test_empty_stack_should_be_falsy(empty_stack):
    assert not empty_stack


@pytest.mark.parametrize("seq", two_plus_element_sequences())
@pytest.mark.parametrize("sequence_factory", sequence_types())
def test_not_empty_stack_should_be_truthy(sequence_factory, seq: Sequence[int]):
    stack = Stack(seq, sequence_factory)

    assert stack
