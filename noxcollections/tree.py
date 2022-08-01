"""Contains ABC for readonly binary tree nodes as well reference implementation using
references. More space-efficient implementation of the same ABC is planned for before
the next (non-dev) release."""

from abc import ABC, abstractmethod
from collections import deque

from typing import Generic, TypeVar, Optional, Generator, Tuple, Deque, Any

T = TypeVar("T")


class BinaryTreeNodeABC(Generic[T], ABC):
    """ABC representing a readonly binary tree node.

    The following properties link node to different nodes in a rather obvious way:
    - left
    - right
    - parent (should be managed by the instance itself, not settable by the user)

    Attributes:
        value (T): value stored in this node
    """

    def __init__(self, value: T):
        self.value = value

    @property
    @abstractmethod
    def left(self) -> "Optional[BinaryTreeNodeABC[T]]":
        """Left child of the node is any or ``None`` if node has no left child."""
        pass

    @property
    @abstractmethod
    def right(self) -> "Optional[BinaryTreeNodeABC[T]]":
        """Right child of the node is any or ``None`` if node has no right child."""
        pass

    @property
    @abstractmethod
    def parent(self) -> "Optional[BinaryTreeNodeABC[T]]":
        """Parent child of the node or ``None`` if this node is root."""

    @property
    def is_root(self) -> bool:
        """``True`` if this node is a root of a binary tree (has no parent)."""
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        """``True`` if this node is a leaf (has no children)."""
        return self.left is None and self.right is None

    @property
    def children(
        self,
    ) -> "Tuple[Optional[BinaryTreeNodeABC[T]], Optional[BinaryTreeNodeABC[T]]]":
        """Tuple representing children of the node in the format ``(left, right)``.

        If node doesn't have given child ``None`` is returned in its place.
        """
        return (self.left, self.right)

    def traverse_bfs(self) -> "Generator[BinaryTreeNodeABC[T], None, None]":
        """Traverses using BFS rules yielding each node as it is encountered.

        Additionally, left node is yielded before the right node. This functions runs in
        ``O(n)`` time using up to aux ``O(n)`` space.
        You might modify yielded nodes but continuing to consume nodes
        **after changing anything but value may lead to unexpected results**.

        Yields:
            Generator[BinaryTreeNodeABC[T], None, None]: Generator of nodes encountered
              while traversing a tree top to bottom and on each of those levels left to
              right.
        """
        to_visit: Deque[BinaryTreeNodeABC[T]] = deque()
        to_visit.append(self)

        while to_visit:
            node = to_visit.pop()
            yield node
            to_visit.extendleft(n for n in node.children if n is not None)

    def values_bfs(self) -> Generator[T, None, None]:
        """Yields values from a tree in BFS order threating this node as a root.

        Values from one level are yielded from the leftmost to the rightmost.
        This function runs in ``O(n)`` time and needs up to ``O(n)`` aux space.

        Yields:
            Generator[T, None, None]: Values from consecutive levels of a tree top to
              bottom and on each level left to right.
        """
        return (n.value for n in self.traverse_bfs())

    def traverse_dfs_preorder(self) -> "Generator[BinaryTreeNodeABC[T], None, None]":
        """Traverses using DFS preorder rules yielding each node as it is encountered.

        Left children are explored until a leaf in encountered then moving on to the
        next seen but not traversed node to the right. This functions runs in
        ``O(n)`` time using up to aux ``O(n)`` space.

        You might modify yielded nodes but continuing to consume nodes
        **after changing anything but value may lead to unexpected results**.


        Yields:
            Generator[BinaryTreeNodeABC[T], None, None]: Nodes as encountered in DFS
              preorder traversal (exploring left children first).
        """
        to_visit = deque()
        to_visit.append(self)

        while to_visit:
            node = to_visit.pop()
            yield node
            to_visit.extend(n for n in node.children[::-1] if n is not None)

    def values_dfs_preorder(self) -> Generator[T, None, None]:
        """Yields values from a tree in DFS preorder threating this node as a root.

        Left children are explored until a leaf in encountered then moving on to the
        next seen but not traversed node to the right. This functions runs in
        ``O(n)`` time using up to aux ``O(n)`` space.


        Yields:
            Generator[T, None, None]: Values from tree as encountered per DFS preorder
              going left first.
        """
        return (n.value for n in self.traverse_dfs_preorder())

    def get_level(self) -> int:
        """Return the level of this node, treating root as having a level of 0.

        Value is calculated **each time this function is called** and this process
        might take **up to ``O(n)`` time** for the leaf of a tree that is essentially a
        linked list.

        Returns:
            int: Level of this node (which is equivalent of the count of ancestors of
              this node).
        """
        node = self
        level = 0
        while node.parent is not None:
            level += 1
            node = node.parent
        return level

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value}, {self.left}, {self.right})"

    def __contains__(self, obj: Any) -> bool:
        return obj in self.values_bfs()


class BinaryTreeNode(BinaryTreeNodeABC[T]):
    """Binary tree node using references to store relationship between nodes.

    In contrast to its ABC this implementation allows setting the child properties.
    Note, that this way of string binary trees is less space-efficient than the method
    using na array.
    """

    def __init__(
        self,
        value: T,
        left: "Optional[BinaryTreeNode[T]]" = None,
        right: "Optional[BinaryTreeNode[T]]" = None,
    ):
        super().__init__(value)
        self._parent: "Optional[BinaryTreeNode[T]]" = None

        self._left = left
        if self._left is not None:
            self._left._parent = self

        self._right = right
        if self._right is not None:
            self._right._parent = self

    @property
    def left(self) -> "Optional[BinaryTreeNode[T]]":
        return self._left

    @left.setter
    def left(self, left: "Optional[BinaryTreeNode[T]]") -> None:
        if left is not None:
            left._parent = self
        self._left = left

    @property
    def right(self) -> "Optional[BinaryTreeNode[T]]":
        return self._right

    @right.setter
    def right(self, right: "Optional[BinaryTreeNode[T]]") -> None:
        if right is not None:
            right._parent = self
        self._right = right

    @property
    def parent(self) -> "Optional[BinaryTreeNode[T]]":
        return self._parent


if __name__ == "__main__":
    tree = BinaryTreeNode(
        0,
        BinaryTreeNode(1, BinaryTreeNode(3), BinaryTreeNode(4)),
        BinaryTreeNode(2, BinaryTreeNode(5), BinaryTreeNode(6)),
    )

    print(*(n.value for n in tree.traverse_dfs_preorder()))
