"""
This module contains implementations of the ``MutableSequence`` ABC using different
data structures.

All public classes from this module implement the ``collections.abc.MutableSequence``
ABC in a way that is intended to be equivalent to the built-in ``list`` type.
"""

from dataclasses import dataclass
from itertools import islice

from abc import abstractmethod, ABC
from typing import (
    Any,
    Optional,
    TypeVar,
    Union,
    Generic,
    Iterator,
    Iterable,
    MutableSequence,
    overload,
)
from collections.abc import Sized

T = TypeVar("T")


def _nth(index: int, iterable: Iterable[T]) -> T:
    """Returns the nth item from an iterable.

    Raises:
       IndexError: if index is incorrect.
    """
    try:
        return next(islice(iterable, index, None))
    except StopIteration:
        raise IndexError("Index out of range")


def _normalize_index(index: int, len_source: Union[int, Sized]) -> int:
    length = len_source if isinstance(len_source, int) else len(len_source)
    translated_index = index if index >= 0 else length - abs(index)

    if translated_index < 0 or translated_index >= length:
        raise IndexError("Index out of range")

    return translated_index


def _normalize_slice(slice_: slice, len_source: Union[int, Sized]) -> slice:
    length = len_source if isinstance(len_source, int) else len(len_source)
    return slice(*slice_.indices(length))


def _indexes_for_slice(slice_: slice, len_source: Union[int, Sized]) -> Iterable[int]:
    """Returns indexes of all elements that would be returned for a given slice.

    Args:
        slice_ (slice): Slice that would be passed to sequence ``s`` of a given length
          in a following manner: ``s[slice_]``
        len_source (Union[int, Sized]): Length of an addressed sequence of a sized
          object to be the source of the same.

    Returns:
        Iterable[int]: All of the indexes for a ``slice_`` in a correct order.
    """
    length = len_source if isinstance(len_source, int) else len(len_source)
    return range(length)[slice_]


@dataclass
class _LinkedListNode(Generic[T]):
    value: T
    next: Optional["_LinkedListNode"] = None


class _ListABC(MutableSequence[T], Generic[T], ABC):
    def __init__(self, values: Optional[Iterable] = None):
        self._head: Optional[_LinkedListNode[T]] = None
        if values is None:
            return

        try:
            iterator = iter(values)
        except TypeError:
            return

        self.extend(iterator)

    @abstractmethod
    def _get_by_index(self, index: int) -> T:
        pass

    @abstractmethod
    def _get_by_slice(self, slice_: slice) -> MutableSequence[T]:
        pass

    @overload
    def __getitem__(self, key: int) -> T:
        pass

    @overload
    def __getitem__(self, key: slice) -> MutableSequence[T]:
        pass

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._get_by_slice(key)
        else:
            return self._get_by_index(key)

    @abstractmethod
    def _set_by_index(self, index: int, value: T) -> None:
        pass

    @abstractmethod
    def _set_by_slice(self, slice_: slice, values: Iterable[T]) -> None:
        pass

    @overload
    def __setitem__(self, key: int, value: T) -> None:
        ...

    @overload
    def __setitem__(self, key: slice, values: Iterable[T]) -> None:
        ...

    def __setitem__(self, key, value) -> None:
        if isinstance(key, slice) and isinstance(value, Iterable):
            self._set_by_slice(key, value)
        elif isinstance(key, int):
            self._set_by_index(key, value)
        else:
            raise TypeError(
                "Arguments must either of types (int, Any) or (slice, Iterable)"
            )

    def __repr__(self) -> str:
        values_str = ", ".join(repr(e) for e in self)
        return f"{self.__class__.__name__}([{values_str}])"

    @abstractmethod
    def _del_by_index(self, key: int) -> None:
        pass

    @abstractmethod
    def _del_by_slice(self, slice_: slice) -> None:
        pass

    def __delitem__(self, key: Union[int, slice]) -> None:
        if isinstance(key, slice):
            self._del_by_slice(key)
        else:
            self._del_by_index(key)


class _LinkedListAbstractBase(_ListABC, Generic[T], ABC):
    def _get_by_index(self, index: int) -> T:
        return _nth(_normalize_index(index, self), iter(self))

    def _get_by_slice(self, slice_: slice) -> MutableSequence[T]:
        return self.__class__(e.value for e in self._iter_nodes_by_slice(slice_))

    def _set_by_index(self, index: int, value: T) -> None:
        nth_node: _LinkedListNode[T] = _nth(
            _normalize_index(index, self), self._iter_nodes()
        )
        nth_node.value = value

    def _set_by_slice(self, slice_: slice, values: Iterable[T]) -> None:
        values_iter = iter(values)
        for node in self._iter_nodes_by_slice(slice_):
            node.value = next(values_iter)

    def _is_empty(self):
        return self._head is None

    def __bool__(self) -> bool:
        return not self._is_empty()

    @abstractmethod
    def _iter_nodes(self) -> Iterator[_LinkedListNode[T]]:
        pass

    # TODO: Improve efficiency by not iterating from the start each time. This affects
    # performance of ``_get_by_slice`` and ``_set_by_slice``.
    def _iter_nodes_by_slice(self, slice_: slice) -> Iterator[_LinkedListNode[T]]:
        return (_nth(i, self._iter_nodes()) for i in _indexes_for_slice(slice_, self))

    def __iter__(self) -> Iterator[T]:
        return (e.value for e in self._iter_nodes())

    def __len__(self) -> int:
        return sum(1 for _ in self)


class LinkedList(_LinkedListAbstractBase, Generic[T]):
    """Equivalent of a built-in ``list`` implemented using **linked list**.

    In the current development version there are **some missing features**:

    - Deletion (i.e. ``del s[...]``) **doesn't support slicing**.
    - `insert()` **raises** ``IndexError`` **for indexes outside the index range**
    of the instance. For examples following calls currently raise `IndexError` instead
    of working in the way consistent with built-in ``list``: ::

        list_ = LinkedList(range(3))
        # All the lines below are examples of calls to `insert()` which raise
        # while they shouldn't (normally they are equivalent to `list_.append(100)`)
        list_.insert(4, 100)
        list_.insert(100, 100)

    - Negative indexes for ``insert()`` cause insertion at before the first element of
    the list.
    """

    def _del_by_slice(self, slice_: slice) -> None:
        raise NotImplementedError("Planned in the next dev release")

    def _delete_first(self):
        if self._head is not None:
            self._head = self._head.next

    def _del_by_index(self, key: int) -> None:
        key = _normalize_index(key, self)
        if key == 0:
            self._delete_first()
            return

        prev_node = _nth(key - 1, self._iter_nodes())
        to_remove = prev_node.next
        prev_node.next = to_remove.next if to_remove is not None else None

    def _iter_nodes(self) -> Iterator[_LinkedListNode[T]]:
        current = self._head
        while current is not None:
            yield current
            current = current.next

    def insert(self, index: int, obj: Any):
        """Inserts ``obj`` into the list at the ``index`` (same as ``s[i:i] = [x]``).

        Current implementation contains the **following bugs** which are intended to be
        fixed in the before the next beta release:

        - **Negative** `index` causes insertion at the beginning of the list.
        - ``IndexError`` is raised **for indexes out of range** of the list after
        insertion.
        """
        if index == 0:
            self._insert_first(obj)
            return

        before_inserted = _nth(index - 1, self._iter_nodes())
        to_insert = _LinkedListNode(value=obj, next=before_inserted.next)
        before_inserted.next = to_insert

    def _insert_first(self, obj: Any):
        new_node = _LinkedListNode(value=obj)
        new_node.next = self._head
        self._head = new_node

    def _get_last_node(self) -> _LinkedListNode[T]:
        if self._head is None:
            raise ValueError("This list is empty")

        last = self._head
        while last.next is not None:
            last = last.next
        return last

    def extend(self, iterable: Iterable[T]) -> None:
        iter_ = iter(iterable)
        if self._head is None:
            try:
                self._insert_first(next(iter_))
            except StopIteration:
                return

        last: _LinkedListNode[T] = self._get_last_node()
        for e in iter_:
            last.next = _LinkedListNode(value=e)
            last = last.next
