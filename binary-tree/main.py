from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node[T]:
    data: T
    parent: Node[T] = None
    left: Node[T] = None
    right: Node[T] = None

    def insert(self, data: T) -> None:
        le, ri = self.get_children()
        if data <= self.data:
            if le:
                return le.insert(data)
            self.left = Node(data, parent=self)
        else:
            if ri:
                return ri.insert(data)
            self.right = Node(data, parent=self)

    def get_children(self) -> tuple[Node[T] | None, Node[T] | None]:
        return self.left, self.right

    def __eq__(self, other: Node[T]) -> bool:
        return self.data == other.data

    def __ne__(self, other: Node[T]) -> bool:
        return self.data != other.data

    def __lt__(self, other: Node[T]) -> bool:
        return self.data < other.data

    def __le__(self, other: Node[T]) -> bool:
        return self.data <= other.data

    def __gt__(self, other: Node[T]) -> bool:
        return self.data > other.data

    def __ge__(self, other: Node[T]) -> bool:
        return self.data >= other.data


class BinaryTree[T]:
    def __init__(self, root: Node[T] = None):
        self.__root: Node[T] = root

    def empty(self) -> bool:
        return self.__root is None

    def insert(self, data: T) -> None:
        if self.empty():
            self.__root = Node(data)
            return
        return self.__root.insert(data)

    def search(self, data: T) -> tuple[bool, Node[T]]:
        ...

    def minimum(self, node: Node[T]):
        ...

    def successor(self, node: Node[T]) -> Node[T]:
        ...

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
        if y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        z.data = y.data if y != z else z.data
