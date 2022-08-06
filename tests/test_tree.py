"""Tests for module ``noxcollections.tree``"""

from typing import Sequence, no_type_check, Iterable, Any, Generator, Callable, Optional
import pytest

from noxcollections.tree import (
    BinaryTreeNode,
    BinaryTreeABC,
    BinaryReferenceTree,
    BstReferenceTree,
)


def _balanced_tree() -> BinaryTreeNode[int]:
    """Returns the balanced tree that in BFS order returns ``0, 1, 2, 3, 4, 5, 6``

    ::

        0
        |--1 (left child)
        |  |--3  (left child)
        |  |__4  (right child)
        |__2  (right child)
           |--5 (left child)
           |__6 (right child)
    """
    return BinaryTreeNode(
        0,
        BinaryTreeNode(1, BinaryTreeNode(3), BinaryTreeNode(4)),
        BinaryTreeNode(2, BinaryTreeNode(5), BinaryTreeNode(6)),
    )


@pytest.fixture
def balanced_tree() -> BinaryTreeNode[int]:
    """Returns the balanced tree that in BFS order returns ``0, 1, 2, 3, 4, 5, 6``

    ::

        0
        |--1 (left child)
        |  |--3  (left child)
        |  |__4  (right child)
        |__2  (right child)
           |--5 (left child)
           |__6 (right child)
    """
    return _balanced_tree()


def _linked_list_tree() -> BinaryTreeNode[int]:
    """Returns a tree degenerated to a linked list where nodes have only right children.

    Consists of values ``0, 1, 2, 3, 4, 5, 6`` in top-bottom order

    ::

        0
        |-x (no left child)
        |__1 (right child)
           |-x
           |__2
              |-x
              |__3
                 |-x
                 |__4
                    |-x
                    |__5
                       |-x
                       |__6
    """
    return BinaryTreeNode(
        0,
        right=BinaryTreeNode(
            1,
            right=BinaryTreeNode(
                2,
                right=BinaryTreeNode(
                    3,
                    right=BinaryTreeNode(
                        4, right=BinaryTreeNode(5, right=BinaryTreeNode(6))
                    ),
                ),
            ),
        ),
    )


def linked_list_tree() -> BinaryTreeNode[int]:
    """Returns a tree degenerated to a linked list where nodes have only right children.

    Consists of values ``0, 1, 2, 3, 4, 5, 6`` in top-bottom order

    ::

        0
        |-x (no left child)
        |__1 (right child)
           |-x
           |__2
              |-x
              |__3
                 |-x
                 |__4
                    |-x
                    |__5
                       |-x
                       |__6
    """
    return _linked_list_tree()


def test_binary_tree_node_constructor_sets_value():
    node = BinaryTreeNode("TEST")

    assert node.value == "TEST"


def test_binary_tree_node_setting_value_changes_value():
    node = BinaryTreeNode(1)
    node.value = -1

    assert node.value == -1


def test_binary_tree_node_one_arg_constructor_creates_a_node_without_children():
    node = BinaryTreeNode(1)

    assert node.left is None
    assert node.right is None


def test_binary_tree_node_without_parent_is_root():
    assert BinaryTreeNode(1).is_root


def test_binary_tree_node_with_a_parent_is_not_root():
    leaf = BinaryTreeNode(2)
    root = BinaryTreeNode(1, leaf)  # noqa: needed to a parent for leaf

    assert not leaf.is_root


def test_binary_tree_node_without_children_is_leaf():
    assert BinaryTreeNode(1).is_leaf


def test_binary_tree_node_with_children_is_not_leaf():
    assert not BinaryTreeNode(1, BinaryTreeNode(2)).is_leaf


def test_binary_tree_node_sets_relationship_with_the_left_child_correctly():
    left_child = BinaryTreeNode(2)
    root = BinaryTreeNode(1, left_child)

    assert root.left is left_child
    assert left_child.parent is root


def test_binary_tree_node_sets_relationship_with_the_right_child_correctly():
    right_child = BinaryTreeNode(2)
    root = BinaryTreeNode(1, None, right_child)

    assert root.right is right_child
    assert right_child.parent is root


def test_binary_tree_node_setting_left_child_sets_the_relationship_properly():
    left_child = BinaryTreeNode(2)
    root = BinaryTreeNode(1)
    root.left = left_child

    assert root.left is left_child
    assert left_child.parent is root


def test_binary_tree_node_setting_right_child_sets_the_relationship_properly():
    right_child = BinaryTreeNode(2)
    root = BinaryTreeNode(1)
    root.right = right_child

    assert root.right is right_child
    assert right_child.parent is root


def test_binary_tree_node_children_should_be_consistent_with_properties_for_a_leaf():
    assert BinaryTreeNode(1).children == (None, None)


def test_binary_tree_node_children_should_be_correct_for_the_left_child_only():
    left_child = BinaryTreeNode(2)
    node = BinaryTreeNode(1, left_child)

    assert node.children == (left_child, None)


def test_binary_tree_node_children_should_be_correct_for_the_right_child_only():
    left_child = BinaryTreeNode(0)
    right_child = BinaryTreeNode(2)
    node = BinaryTreeNode(1, left_child, right_child)

    assert node.children == (left_child, right_child)


def test_binary_tree_node_children_should_be_correct_for_node_with_both_children():
    right_child = BinaryTreeNode(2)
    node = BinaryTreeNode(1, right=right_child)

    assert node.children == (None, right_child)


def test_binary_tree_node_root_get_level_returns_0(balanced_tree: BinaryTreeNode[int]):
    assert balanced_tree.get_level() == 0


@no_type_check  # Since checking for None at each level would obscure the test
def test_binary_tree_node_get_heigh_return_value_consistent_with_number_of_its_parents(
    balanced_tree: BinaryTreeNode[int],
):
    # level 1
    assert balanced_tree.left.get_level() == balanced_tree.right.get_level() == 1

    # Level 2
    assert (
        balanced_tree.left.left.get_level()
        == balanced_tree.left.right.get_level()
        == balanced_tree.right.left.get_level()
        == balanced_tree.right.right.get_level()
        == 2
    )


@no_type_check  # Since checking for None at each level would obscure the test
def test_binary_tree_node_more_complex_structures_is_formed_correctly(
    balanced_tree: BinaryTreeNode[int],
):
    # Check root
    assert balanced_tree.value == 0

    # Check root children
    assert balanced_tree.left.value == 1
    assert balanced_tree.right.value == 2

    # Check children of the root's left child
    assert balanced_tree.left.left.value == 3
    assert balanced_tree.left.right.value == 4

    # Check children of the root's right child
    assert balanced_tree.right.left.value == 5
    assert balanced_tree.right.right.value == 6


@pytest.mark.parametrize("tree", [_balanced_tree(), _linked_list_tree()])
def test_binary_tree_node_traverse_bfs_returns_all_nodes_in_a_tree(
    tree: BinaryTreeNode[int],
):
    assert set(n.value for n in tree.traverse_bfs()) == set(range(7))


@pytest.mark.parametrize(
    ("tree", "order"),
    [
        (_balanced_tree(), [0, 1, 2, 3, 4, 5, 6]),
        (_linked_list_tree(), [0, 1, 2, 3, 4, 5, 6]),
    ],
)
def test_binary_tree_bfs_traverse_returns_values_in_a_correct_order(
    tree: BinaryTreeNode[int], order: Sequence[int]
):
    assert list(n.value for n in tree.traverse_bfs()) == order


@pytest.mark.parametrize("tree", [_balanced_tree(), _linked_list_tree()])
def test_binary_tree_bfs_values_should_be_consistent_with_values_of_traverse_bfs(
    tree: BinaryTreeNode[int],
):
    assert list(n.value for n in tree.traverse_bfs()) == list(tree.values_bfs())


@pytest.mark.parametrize("tree", [_balanced_tree(), _linked_list_tree()])
@pytest.mark.parametrize("to_find", range(7))
def test_binary_tree_bfs_contains_should_return_true_if_value_is_in_tree(
    tree: BinaryTreeNode[int], to_find: int
):
    assert to_find in tree


@pytest.mark.parametrize("tree", [_balanced_tree(), _linked_list_tree()])
@pytest.mark.parametrize("to_find", [-1, "abc"])
def test_binary_tree_bfs_contains_should_return_false_if_value_is_not_in_tree(
    tree: BinaryTreeNode[int], to_find: object
):
    assert to_find not in tree


@pytest.mark.parametrize(
    ("tree", "order"),
    [
        (_balanced_tree(), [0, 1, 3, 4, 2, 5, 6]),
        (_linked_list_tree(), [0, 1, 2, 3, 4, 5, 6]),
    ],
)
def test_binary_tree_traverse_returns_dfs_preorder_values_in_a_correct_order(
    tree: BinaryTreeNode[int], order: Sequence[int]
):
    assert list(n.value for n in tree.traverse_dfs_preorder()) == order


@pytest.mark.parametrize("tree", [_balanced_tree(), _linked_list_tree()])
def test_binary_tree_values_dfs_preorder_should_be_consistent_with_traverse(
    tree: BinaryTreeNode[int],
):
    assert list(n.value for n in tree.traverse_dfs_preorder()) == list(
        tree.values_dfs_preorder()
    )


BinaryTreeConstructor = Callable[[Optional[Iterable]], BinaryTreeABC]


@pytest.fixture(params=[BinaryReferenceTree, BstReferenceTree])
def binary_tree(request) -> BinaryTreeConstructor:
    return request.param


def test_binary_reference_tree_empty_instances_are_falsy(
    binary_tree: BinaryTreeConstructor,
):
    tree = binary_tree(None)

    assert not tree


def test_binary_reference_tree_contains_item_after_add(
    binary_tree: BinaryTreeConstructor,
):
    tree = binary_tree(None)
    tree.add("abc")

    assert "abc" in tree


def test_binary_reference_tree_does_not_contain_not_added_item(
    binary_tree: BinaryTreeConstructor,
):
    tree = binary_tree(None)
    tree.add("abc")

    assert "def" not in tree


def values_for_tree() -> Generator[Sequence[Any], None, None]:
    yield range(3)
    yield [11]
    yield (-999, 999, -10, 123)


@pytest.mark.parametrize("values", values_for_tree())
def test_binary_reference_tree_constructor_with_iterable_adds_passed_iterable(
    binary_tree: BinaryTreeConstructor, values: Sequence
):
    tree = binary_tree(values)

    for item in values:
        assert item in tree


parametrize_discard_tests = pytest.mark.parametrize(
    ("values", "to_discard"),
    [
        ([0], 0),
        ([10, 1, 999], 10),
        ([10, 1, 999], 1),
        ([10, 1, 999], 999),
        (range(10), 7),
    ],
)


@pytest.mark.xfail(reason="Not implemented yet for BST")
@parametrize_discard_tests
def test_binary_reference_tree_discard_removes_item_from_tree(
    binary_tree: BinaryTreeConstructor, values: Iterable[int], to_discard: int
):
    tree = binary_tree(values)
    tree.discard(to_discard)

    assert to_discard not in tree


@pytest.mark.xfail(reason="Not implemented yet for BST")
@pytest.mark.parametrize(
    ("values", "to_discard"),
    [
        ([0], 10),
        ([0], 123),
        ([10, 1, 999], -10),
        ([10, 1, 999], 1.1),
        ([10, 1, 999], [1, 2, 3]),
        (range(10), 10),
    ],
)
def test_binary_reference_tree_discard_element_not_in_tree_throws(
    binary_tree: BinaryTreeConstructor, values: Iterable[int], to_discard: Any
):
    tree = binary_tree(values)

    with pytest.raises(KeyError):
        tree.discard(to_discard)


@pytest.mark.parametrize("values", values_for_tree())
def test_binary_reference_tree_len_consistent_with_iterable_passed_to_constructor(
    binary_tree: BinaryTreeConstructor, values: Sequence
):
    tree = binary_tree(values)

    assert len(tree) == len(values)


@pytest.mark.parametrize("values", values_for_tree())
def test_binary_reference_tree_length_increases_after_add(
    binary_tree: BinaryTreeConstructor, values: Sequence
):
    tree = binary_tree(values)
    tree.add(-987654321)

    assert len(tree) == len(values) + 1


@pytest.mark.xfail(reason="Not implemented yet for BST")
@parametrize_discard_tests
def test_binary_reference_tree_length_decreases_after_discard(
    binary_tree: BinaryTreeConstructor, values: Sequence[int], to_discard: int
):
    tree = binary_tree(values)
    tree.discard(to_discard)

    assert len(tree) == len(values) - 1
