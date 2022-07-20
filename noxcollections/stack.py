"""This module contains ABC for the stack ADT as well as its implementation based
on a MutableSequence implementation passed by the caller."""

from abc import ABC, abstractmethod

from typing import Optional, Iterable, TypeVar, Generic, Sized, Union, Any

T = TypeVar("T")
S = TypeVar("S", Any, None)


class StackABC(Generic[T], Sized, ABC):
    """ABC for stack ADT."""

    @abstractmethod
    def __init__(self, iterable: Optional[Iterable[T]]) -> None:
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
    def empty(self) -> bool:
        """Returns ``True`` if the stack is empty and ``False`` otherwise."""

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
    def pop(self) -> None:
        """Returns and **removes**  the top-most element form the stack.

        Raises:
            IndexError: if the stack is empty.
        """
