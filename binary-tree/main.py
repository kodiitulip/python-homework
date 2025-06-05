from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
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

    def __str__(self) -> str:
        lines, *_ = self.__get_pretty_print()
        return "\n".join(lines)

    def __get_pretty_print(self) -> tuple[list[str], int, int, int]:
        left, right = self.get_children()
        data = self.data

        if right and left:
            linesl, wl, hl, pl = left.__get_pretty_print()
            linesr, wr, hr, pr = right.__get_pretty_print()
            ds = str(data)
            dw = len(ds) + 2
            dali = f"{(pl) * ' '}╓{(wl - pl - 1) * '─'} {ds} {(pr - 1) * '─'}╖{(wr - pr) * ' '}"
            if hl < hr:
                linesl += [wl * " "] * (hr - hl)
            elif hr < hl:
                linesr += [wr * " "] * (hl - hr)
            ziplines = zip(linesl, linesr)
            lines = [dali] + [a + dw * " " + b for a, b in ziplines]
            return lines, wl + wr + dw, max(hl, hr) + 2, wl + dw // 2
        elif left and not right:
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
        elif right and not left:
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


class BinaryTree[T: SupportsAllComparisons]:
    def __init__(self, root: Node[T] | None = None):
        self.__root: Node[T] | None = root

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

    def search(self, data: T) -> tuple[bool, Node[T]]: ...

    def minimum(self, node: Node[T]): ...

    def successor(self, node: Node[T]) -> Node[T]:
        """grabs the lowest value thats greater then <node>"""
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
        y = self.successor(z) if z.get_children() else z
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

    def __repr__(self) -> str:
        return self.__root.__repr__()

    def __str__(self) -> str:
        return self.__root.__str__()


if __name__ == "__main__":
    bt = BinaryTree()
    for _ in range(10):
        bt.insert(randint(1, 100))
    print(bt)
