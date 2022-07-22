"""This module contains ABC for the stack ADT as well as its implementation based
on a MutableSequence implementation passed by the caller."""

from abc import ABC, abstractmethod

from noxcollections.lists import LinkedList

from typing import (
    Optional,
    Iterable,
    TypeVar,
    Generic,
    Sized,
    Union,
    Any,
    Callable,
    MutableSequence,
)

T = TypeVar("T")
S = TypeVar("S", Any, None)


class StackABC(Generic[T], Sized, ABC):
    """ABC for stack ADT."""

    @abstractmethod
    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        """ABC for stack ADT. If ``iterable`` is passed elements are added to the stack.

        Passing ``iterable`` is equivalent to adding all of the elements from it in
        order.

        Args:
            iterable (Optional[Iterable[T]]): If supplied elements of this will be added
                added to the stack.
        """
        if iterable is None:
            return

        for e in iterable:
            self.push(e)

    @abstractmethod
    def __len__(self) -> int:
        """Returns number of the elements on the stack."""

    def __bool__(self) -> bool:
        return bool(len(self))

    @abstractmethod
    def top(self) -> T:
        """Returns top(last added) element from the stack **without removing it**.

        Raises ``IndexError`` if the stack is empty.

        Returns:
            T: Top-most element from the stack.

        Raises:
            IndexException: If the stack is empty.
        """

    def peek(self, default: S = None) -> Union[T, S]:
        """Returns top element form the stack or ``default`` if the stack is empty.

        Element is not removed. Works the same way as ``top`` but returns a default
        value instead of raising.

        Args:
            default (S): Value to be returned if the stack is empty.

        Returns:
            Union[T, S]: Top-most element from the stack or ``default`` if the stack is
                empty.
        """
        try:
            return self.top()
        except IndexError:
            return default

    @abstractmethod
    def push(self, element: T) -> None:
        """Adds ``element`` as the top-most element of the stack.

        Args:
            element (T): element to be added as the top of the stack.
        """

    @abstractmethod
    def pop(self) -> T:
        """Returns and **removes**  the top-most element form the stack.

        Raises:
            IndexError: if the stack is empty.
        """


class Stack(StackABC, Generic[T]):
    """A stack implementation based on MutableSequence factory passed as a parameter.

    To achieve O(1) time complexity on all operations used MutableSequence
    implementation should ideally have the following operations of time complexity O(1):
    1. Insertion at the first index (``s.insert(0, elem)``)
    2. Deletion at the first index (``del s[0]``)
    3. Length calculation (``len(s)``)

    By default ``noxcollections.lists.LinkedList`` is used as the backing
    ``MutableSequence``. Using ``list`` is not recommended as inserting and deleting
    at the start of the ``lists`` have the time complexity of ``O(n)``.
    """

    def __init__(
        self,
        iterable: Optional[Iterable[T]] = None,
        sequence_factory: Callable[[], MutableSequence] = LinkedList,
    ) -> None:
        """Creates a stack based on a ``MutableSequence`` implementing object.

        If time complexity of operations is important refer to class'es documentation
        for conditions to achieve O(1) time complexity for all operations while choosing
        the type of the sequence returned by the ``sequence_factory``.

        Args:
            iterable (Optional[Iterable[T]], optional): If passed all elements from the
                ``iterable`` are pushed onto the stack after its creation.
            sequence_factory (Callable[[], MutableSequence], optional): Callable
                returning object implementing the MutableSequence protocol. Defaults to
                ``noxcollections.lists.LinkedList``.
        """
        self._sequence_factory = sequence_factory

        self._backing_sequence = sequence_factory()
        super().__init__(iterable)

    def __len__(self) -> int:
        return len(self._backing_sequence)

    def top(self) -> T:
        try:
            return self._backing_sequence[0]
        except IndexError:
            raise IndexError("Stack is empty")

    def push(self, element: T) -> None:
        self._backing_sequence.insert(0, element)

    def pop(self) -> T:
        try:
            return self._backing_sequence.pop(0)
        except IndexError:
            raise IndexError("Stack is empty")

    def __repr__(self) -> str:
        sequence_repr = repr(list(self._backing_sequence)[::-1])
        callable_name = self._sequence_factory.__name__
        return f"{self.__class__.__name__}({sequence_repr}, {callable_name})"
