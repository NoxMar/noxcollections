"""Contains ABC for readonly binary tree nodes as well reference implementation using
references. More space-efficient implementation of the same ABC is planned for before
the next (non-dev) release."""

from abc import ABC, abstractmethod
from collections import deque

from typing import (
    Generic,
    TypeVar,
    Optional,
    Generator,
    Tuple,
    Deque,
    Any,
    Iterator,
    AbstractSet,
    Iterable,
    Protocol,
)

T = TypeVar("T")


S = TypeVar("S", bound="BinaryTreeNodeABC")


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
        """Left child of the node, if any. See note about permissible values to set.

        Note: Setting should be constrained to nodes of the same tree, leafs, or roots
        of a tree that don't have any parents (aren't roots of a subtree in a different
        tree). Handling the same nodes in different trees (not subtrees) is not
        defined."""
        pass

    @left.setter
    def left(self, new_val: "Optional[BinaryTreeNodeABC[T]]") -> None:
        pass

    @property
    @abstractmethod
    def right(self) -> "Optional[BinaryTreeNodeABC[T]]":
        """Right child of the node, if any. See note about permissible values to set.

        Note: Setting should be constrained to nodes of the same tree, leafs, or roots
        of a tree that don't have any parents (aren't roots of a subtree in a different
        tree). Handling the same nodes in different trees (not subtrees) is not
        defined."""
        pass

    @right.setter
    def right(self, new_val: "Optional[BinaryTreeNodeABC[T]]") -> None:
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

    def traverse_bfs(
        self,
    ) -> "Generator[BinaryTreeNodeABC[T], None, None]":
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

    def get_leftmost_descendant(self):
        node = self
        left_child = node.left
        while left_child is not None:
            node = left_child
            left_child = node.left
        return node

    def get_rightmost_descendant(self):
        node = self
        right_child = node.right
        while right_child is not None:
            node = right_child
            right_child = node.right
        return node

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
        to_visit: Deque[BinaryTreeNodeABC[T]] = deque()
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


class BinaryTreeABC(AbstractSet[T], ABC):
    """ABC representing a higher level view of a binary tree as a set.

    This view exposes higher level operations like insertion, membership testing, and
    deletion without exposing nodes for direct manipulation. Additionally, empty
    instances are considered truthy and instances containing at least one node - falsy.

    Concrete implementations of this ABC may include additional ways in which those
    operations are conducted to achieve some type of order or improve complexity of
    those operations (e.g. BST and its variants).
    """

    def __init__(self, values: Optional[Iterable[T]] = None):
        if values is None:
            return
        for v in values:
            self.add(v)

    @property
    @abstractmethod
    def root(self) -> Optional[BinaryTreeNodeABC]:
        """Root of this tree. This object **should not be modified in any way**.

        This property is meant to be used for traversal and any other non-mutating
        operations.
        """

    @abstractmethod
    def add(self, value: T) -> None:
        """Inserts ``value`` into this instance of a tree.

        After this operation ``value in tree`` will return True.

        Args:
            value (T): Value to be inserted.
        """

    @abstractmethod
    def discard(self, value: T) -> None:
        """Removes ``value`` if it is present, otherwise throws ``KeyError``.

        Args:
            value (T): Value to be removed from the tree.

        Throws:
            KeyError: If ``value`` was not present in this tree.
        """

    @abstractmethod
    def __contains__(self, value: Any) -> bool:
        """Returns ``True`` if node representing ``value`` exits in this tree.

        Returns:
            bool: Boolean value indicating if a node representing ``value`` exists in
              this tree.
        """

    def __repr__(self):
        keys_str = (
            ", ".join(repr(v) for v in self.root.values_bfs())
            if self.root is not None
            else ""
        )
        return f"{self.__class__.__name__}({keys_str})"

    def __iter__(self) -> Iterator[T]:
        if self.root is None:
            yield from ()
            return
        yield from self.root.values_bfs()

    def __len__(self) -> int:
        # TODO: cache length since now it takes O(n) time to count the number of nodes.
        return sum(1 for _ in self)


CT = TypeVar("CT", bound="Comparable")


class Comparable(Protocol):
    """Protocol for annotating comparable types."""

    @abstractmethod
    def __lt__(self: CT, other: CT) -> bool:
        pass


class BinaryReferenceTree(BinaryTreeABC[T]):
    """Set implementation based on binary tree where nodes storing references to each other.

    This is meant for reference (as in reference implementation in terms of behavior) of
    a binary tree-based set. For practical purposes, BST or its self-balancing variants
    are probably a better fit.

    Note that because there are no rules placed on the tree, all operations have the
    same complexity as if they were done on a list and worse aux space complexity.
    """

    def __init__(self, values: Optional[Iterable[T]] = None):
        self._root: Optional[BinaryTreeNodeABC[T]] = None
        super().__init__(values)

    @property
    def root(self) -> Optional[BinaryTreeNodeABC]:
        return self._root

    def _find_node_and_parent(
        self, value: T
    ) -> Tuple[Optional[BinaryTreeNodeABC[T]], Optional[BinaryTreeNodeABC[T]]]:
        """Finds a node holding `value` and its parent if such a node exists.

        If node with this value does not exist then `None` is returned in its place.
        In this case the second returned node will be the node that would be a parent
        of node with `value` if such a node existed.

        Args:
            value (CT): `value` to be found

        Returns:
            Tuple[Optional[BinaryTreeNodeABC[CT]], Optional[BinaryTreeNodeABC[CT]]]:
              A tuple of node containing `value` if found and a (if not found potential)
              parent of this node.
        """
        if self._root is None:
            return None, None

        node = next((n for n in self._root.traverse_bfs() if n.value == value), None)
        if node is None:
            return None, None

        parent = node.parent if node.parent is not None else None
        return node, parent

    def add(self, value: T) -> None:
        """Inserts ``value`` into this instance of a tree in O(n) time.

        After this operation ``value in tree`` will return ``True``. This method does
        **not provide any guarantees where the new value will be inserted**.

        Args:
            value (T): Value to be inserted.
        """
        if self._root is None:
            self._root = BinaryTreeNode(value)
            return

        to_append_to = next(
            n for n in self._root.traverse_bfs() if n.left is None or n.right is None
        )
        if to_append_to.left is None:
            to_append_to.left = BinaryTreeNode(value)
        else:
            to_append_to.right = BinaryTreeNode(value)

    def _delete_leaf(self, leaf: BinaryTreeNodeABC[T]) -> None:
        if leaf.parent is None:
            self._root = None
            return

        if leaf.parent.left is leaf:
            leaf.parent.left = None
        else:
            leaf.parent.right = None

    def _delete_non_leaf(
        self,
        node: BinaryTreeNodeABC[T],
        remaining_nodes_bfs: Iterator[BinaryTreeNodeABC[T]],
    ) -> None:
        # Placing the last node in the level order in place of the removed node to try
        # to keep the tree balanced.
        bottom_rightmost_leaf = None
        for bottom_rightmost_leaf in remaining_nodes_bfs:
            pass
        if bottom_rightmost_leaf is None:
            raise ValueError("Leaf passed to _delete_not_leaf")
        node.value = bottom_rightmost_leaf.value
        self._delete_leaf(bottom_rightmost_leaf)

    def discard(self, value: T) -> None:
        """Removes one instance of ``value`` in O(n) time throwing ``KeyError`` if not present.

        Only guarantee provided after this operation is that tree will still be a
        proper binary tree. If there were multiple node containing ``value``
        **only one of them will be removed**.

        Args:
            value (T): Value to be removed from the tree.

        Throws:
            KeyError: If ``value`` was not present in this tree.
        """
        if self._root is None:
            raise KeyError("Cannot remove elements from an empty tree")

        nodes = iter(self._root.traverse_bfs())
        try:
            node_value = next(n for n in nodes if n.value == value)
        except StopIteration:
            raise KeyError(f"Key {value} not found")

        if node_value.is_leaf:
            self._delete_leaf(node_value)
            return

        self._delete_non_leaf(node_value, nodes)

    def __contains__(self, value: Any) -> bool:
        return self._find_node_and_parent(value)[0] is not None


class BstReferenceTree(BinaryReferenceTree[CT]):
    """Set implementation based on a reference-based BST.

    Values in the tree have to be comparable among themselves (support at least ``<``
    and ``==`` operators).

    This is a normal BST without any self balancing strategies. So operations run in
    average O(log_2(n)) time however the worst case time complexity is O(n) (for
    operations on a tree that is essentially a linked list)"""

    def __init__(self, values: Optional[Iterable[CT]] = None):
        self._root: Optional[BinaryTreeNodeABC[CT]] = None
        super().__init__(values)

    def _find_node_and_parent(
        self, value: CT
    ) -> Tuple[Optional[BinaryTreeNodeABC[CT]], Optional[BinaryTreeNodeABC[CT]]]:
        """Finds a node holding `value` and its parent if such a node exists.

        If node with this value does not exist then `None` is returned in its place.
        In this case the second returned node will be the node that would be a parent
        of node with `value` if such a node existed.

        Args:
            value (CT): `value` to be found

        Returns:
            Tuple[Optional[BinaryTreeNodeABC[CT]], Optional[BinaryTreeNodeABC[CT]]]:
              A tuple of node containing `value` if found and a (if not found potential)
              parent of this node.
        """
        parent = None
        node = self._root

        # `not node.value == value` since only `<` and `==` are ensured by the contract.
        while node is not None and not node.value == value:
            parent = node
            node = node.left if value < node.value else node.right

        return node, parent

    def add(self, value: CT) -> None:
        """Inserts ``value`` into a tree in O(log2(n)) avg, O(n) worst case time.

        After this operation ``value in tree`` will return ``True``.

        Args:
            value (CT): Value to be inserted.
        """
        node_to_add = BinaryTreeNode(value)
        _, parent = self._find_node_and_parent(value)
        if parent is None:
            self._root = node_to_add
            return

        if value < parent.value:
            parent.left = node_to_add
        else:
            parent.right = node_to_add

    def _delete_with_both_children(self, node: BinaryTreeNodeABC[CT]) -> None:
        if node.left is None:
            return
        replacement_node = node.left.get_rightmost_descendant()
        # TODO: replace with delete
        replacement_node.parent.left = replacement_node.right
        node.value = replacement_node.value

    def _delete_node_with_children(self, node: BinaryTreeNodeABC[CT]) -> None:
        if node.left is not None and node.right is not None:
            self._delete_with_both_children(node)
            return

        replacement_node = node.left if node.left is not None else node.right
        if node.parent is None:
            self._root = replacement_node
            return

        if node is node.parent.left:
            node.parent.left = replacement_node
        else:
            node.parent.right = replacement_node

    def discard(self, value: CT) -> None:
        """Removes one instance of ``value`` in O(log_2(n)) avg O(n) worst case time.

        If there is no instance of ``value`` is this tree ``KeyError`` is raised.

        Args:
            value (CT): Value to be removed from the tree.

        Throws:
            KeyError: If ``value`` was not present in this tree.
        """
        node, _ = self._find_node_and_parent(value)
        if node is None:
            # TODO remove string duplication
            raise KeyError(f"Key {value} not found")

        if node.is_leaf:
            self._delete_leaf(node)
            return

        self._delete_node_with_children(node)
