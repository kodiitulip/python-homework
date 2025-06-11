from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from re import search
from typing import TYPE_CHECKING, Tuple, List
from random import randint

if TYPE_CHECKING:
    from _typeshed import SupportsAllComparisons


@dataclass
class Node[T: SupportsAllComparisons]:
    data: T
    parent: Node[T] | None = None
    left: Node[T] | None = None
    right: Node[T] | None = None

    def get_children(self) -> tuple[Node[T] | None, Node[T] | None]:
        return self.left, self.right

    def is_leaf(self) -> bool:
        l, r = self.get_children()
        return l is None and r is None

    def __str__(self) -> str:
        lines, *_ = self.__get_pretty_print()
        return "\n".join(lines)

    def __get_pretty_print(self) -> tuple[list[str], int, int, int]:
        left, right = self.get_children()
        data = self.data

        if right is not None and left is not None:
            linesl, wl, hl, pl = left.__get_pretty_print()
            linesr, wr, hr, pr = right.__get_pretty_print()
            ds = str(data)
            dw = len(ds) + 2
            dali = f"{pl * ' '}╓{(wl - pl - 1) * '─'} {ds} {(pr - 1) * '─'}╖{(wr - pr) * ' '}"
            if hl < hr:
                linesl += [wl * " "] * (hr - hl)
            elif hr < hl:
                linesr += [wr * " "] * (hl - hr)
            ziplines = zip(linesl, linesr)
            lines = [dali] + [a + dw * " " + b for a, b in ziplines]
            return lines, wl + wr + dw, max(hl, hr) + 2, wl + dw // 2
        elif left is not None and right is None:
            lines, width, height, pos = left.__get_pretty_print()
            ds = str(data)
            dw = len(ds) + 2
            dali = f"{pos * ' '}╓{(width - pos - 1) * '─'} {ds} "
            shli = [line + dw * " " for line in lines]
            return (
                [dali] + shli,
                width + dw,
                height + 2,
                width + dw // 2,
            )
        elif right is not None and left is None:
            lines, width, height, pos = right.__get_pretty_print()
            ds = str(data)
            dw = len(ds) + 2
            dali = f" {ds} {(pos - 1) * '─'}╖{(width - pos) * ' '}"
            shli = [dw * " " + line for line in lines]
            return (
                [dali] + shli,
                width + dw,
                height + 2,
                dw // 2,
            )
        else:
            line = str(self.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self.data == other.data

    def __ne__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self.data != other.data

    def __lt__(self, other: Node[T]) -> bool:
        return self.data < other.data

    def __le__(self, other: Node[T]) -> bool:
        return self.data <= other.data

    def __gt__(self, other: Node[T]) -> bool:
        return self.data > other.data

    def __ge__(self, other: Node[T]) -> bool:
        return self.data >= other.data

    def __len__(self) -> int:
        left, right = self.get_children()
        amt: int = 1
        amt += left.__len__() if left else 0
        amt += right.__len__() if right else 0
        return amt


class BinaryTree[T: SupportsAllComparisons]:
    def __init__(self, root: Node[T] | None = None):
        self.__root: Node[T] | None = root

    def empty(self) -> bool:
        return self.__root is None

    def insert(self, data: T) -> None:
        if self.__root is None:
            self.__root = Node(data)
            return

        def _insert_aux(node: Node[T]) -> None:
            left, right = node.get_children()
            check = data <= node.data
            aux = left if check else right
            if aux:
                return _insert_aux(aux)
            node.left = Node(data, parent=node) if check else node.left
            node.right = Node(data, parent=node) if not check else node.right

        return _insert_aux(self.__root)

    def search(self, data: T) -> tuple[bool, Node[T]]:
        node = Node(data)
        if self.empty():
            return False, node

        def search_aux(root: Node[T]) -> tuple[bool, Node[T]]:
            if root is None:
                return False, node
            if root == node:
                return True, root
            if node < root:
                return search_aux(root.left)
            return search_aux(root.right)

        return search_aux(self.__root)

    def minimum(self, node: Node[T]):
        left, _ = node.get_children()
        return node if left is None else self.minimum(left)

    def maximum(self, node: Node[T]):
        _, right = node.get_children()
        return node if right is None else self.maximum(right)

    @staticmethod
    def successor(node: Node[T]) -> Node[T]:
        """grabs the lowest value that's greater than <node>"""
        _, right = node.get_children()
        if not right:
            return node

        low: T = right.data
        current = right
        while current.left:
            low = current.left.data if current.left <= low else low
            current = current.left
        return current

    def delete(self, value: T) -> None:
        belongs, z = self.search(value)
        if not belongs:
            return None
        y = self.successor(z)
        x = y.left if y.left else y.right
        if x:
            x.parent = y.parent
        if not y.parent:
            self.__root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        z.data = y.data if y != z else z.data

    def delete_subtree(self, value: T) -> None:
        belongs, n = self.search(value)
        if not belongs:
            return None
        if n.parent is None:
            self.__root = None
        if n.parent.left == n:
            n.parent.left = None
        else:
            n.parent.right = None

    def number_of_leaves(self) -> int:
        def number_aux(node: Node[T]) -> int:
            if node is None:
                return 0
            if node.is_leaf():
                return 1
            numb = 0
            numb += number_aux(node.left)
            numb += number_aux(node.right)
            return numb
        return number_aux(self.__root)

    def number_of_left_leaves(self) -> int:
        if self.empty():
            return 0
        n = self.traversal()
        return len([node for node in n[0] if node.left is not None and node.left.is_leaf()])

    def traversal(self, in_order=True, pre_order=False, post_order=False) -> tuple[
            list[Node[T]] | None, list[Node[T]] | None, list[Node[T]] | None]:
        ino = self.__in_order(self.__root) if in_order else None
        pre = self.__pre_order(self.__root) if pre_order else None
        pos = self.__post_order(self.__root) if post_order else None
        return ino, pre, pos

    def __in_order(self, root, list_=None) -> list[Node[T]]:
        if list_ is None:
            list_ = list()
        if root is None:
            return list_
        self.__in_order(root.left, list_)
        list_.append(root)
        self.__in_order(root.right, list_)
        return list_

    def __pre_order(self, root, list_=None) -> list[Node[T]]:
        if list_ is None:
            list_ = list()
        if root is None:
            return list_
        list_.append(root)
        self.__in_order(root.left, list_)
        self.__in_order(root.right, list_)
        return list_

    def __post_order(self, root, list_=None) -> list[Node[T]]:
        if list_ is None:
            list_ = list()
        if root is None:
            return list_
        self.__in_order(root.left, list_)
        self.__in_order(root.right, list_)
        list_.append(root)
        return list_

    def __len__(self) -> int:
        return len(self.__root)

    def __repr__(self) -> str:
        return self.__root.__repr__()

    def __str__(self) -> str:
        return self.__root.__str__()
        # if self.__root is not None:
        #     return str(self.traversal(in_order=False, pre_order=True)[1])


if __name__ == "__main__":
    bt = BinaryTree()
    for _ in range(10):
        bt.insert(randint(1, 10))
    print(bt)
    print(len(bt))
    print(bt.search(5))
    bt.delete(5)
    print(bt)
    print(bt.number_of_leaves())
    print(bt.number_of_left_leaves())
