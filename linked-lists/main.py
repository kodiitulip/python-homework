from __future__ import annotations

from abc import ABC, abstractmethod
from os import get_terminal_size


class BaseList[T](ABC):
    @abstractmethod
    def empty(self) -> bool: ...

    @abstractmethod
    def length(self) -> int: ...

    @abstractmethod
    def append(self, data: T) -> None: ...

    @abstractmethod
    def insert(self, index: int, data: T) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def remove(self, data: T) -> None: ...

    @abstractmethod
    def remove_all(self, data: T) -> None: ...


class LinkedList[T](BaseList[T]):
    class Node:
        def __init__(self, data: T) -> None:
            self.__data: T = data
            self.__next: LinkedList.Node | None = None

        @property
        def data(self):
            """The data contained in this Node"""
            return self.__data

        @data.setter
        def data(self, value: T):
            self.__data = value

        @property
        def next(self):
            """The next Node in the chain"""
            return self.__next

        @next.setter
        def next(self, value):
            self.__next = value

        def count(self) -> int:
            return 1 + (self.next.count() if self.next else 0)

        def __str__(self) -> str:
            return str(self.data) + (" " + str(self.next) if self.next else "")

    def __init__(self) -> None:
        self.__head: LinkedList.Node | None = None
        self.__tail: LinkedList.Node | None = self.__head

    @property
    def head(self) -> LinkedList.Node | None:
        return self.__head

    @head.setter
    def head(self, node: LinkedList.Node | None):
        self.__head = node

    @property
    def tail(self) -> LinkedList.Node | None:
        return self.__tail

    @tail.setter
    def tail(self, node: LinkedList.Node | None):
        self.__tail = node

    def __str__(self) -> str:
        max_size: int = get_terminal_size().columns - 2
        list_str: str = str(self.head if self.head else "")
        final_size: int = min(len(list_str), max_size)
        return f"""
┌{"":─<{final_size}}┐
│{list_str: <{final_size}}│
└{"":─<{final_size}}┘"""

    def empty(self) -> bool:
        return not self.head

    def length(self) -> int:
        return 0 + (self.head.count() if self.head else 0)

    def append(self, data: T) -> None:
        new_node: LinkedList.Node = LinkedList.Node(data)
        if self.empty():
            self.head = new_node
            self.tail = self.head
            return

        if self.tail:
            self.tail.next = new_node
            self.tail = new_node
            return

        raise Exception("Tail Node missing or not assigned")

    def insert(self, index: int, data: T) -> None:
        if not self.head or index > self.length():
            return self.append(data)

        if index == 0:
            aux = LinkedList.Node(data)
            aux.next = self.head
            self.head = aux
            return

        pos: int = 0
        itr: LinkedList.Node = self.head
        while itr.next and pos < index - 1:
            itr = itr.next
            pos += 1

        new_node: LinkedList.Node = LinkedList.Node(data)
        new_node.next = itr.next
        itr.next = new_node

    def clear(self) -> None:
        self.head = None
        self.tail = None

    def remove(self, data: T) -> None:
        if not self.head:
            raise Exception("List is Empty")

        if self.head.data == data:
            self.head = self.head.next
            return

        if not self.head:
            return

        itr: LinkedList.Node = self.head
        while itr.next:
            if itr.next.data == data:
                itr.next = itr.next.next
                return
            else:
                itr = itr.next

    def remove_all(self, data: T) -> None:
        if not self.head:
            raise Exception("List is Empty")
        while self.head and self.head.data == data:
            self.head = self.head.next

        if not self.head:
            return

        itr: LinkedList.Node = self.head
        while itr.next:
            if itr.next.data == data:
                itr.next = itr.next.next
            else:
                itr = itr.next


if __name__ == "__main__":
    ll = LinkedList[str]()
    for i in range(5):
        ll.append("oi")
    print(ll)
    ll.append("no")
    print(ll)
    ll.append("shit")
    print(ll)
    ll.remove("no")
    print(ll)
    ll.insert(1, "io")
    print(ll)
    ll.remove("oi")
    print(ll)
    ll.remove_all("oi")
    print(ll)
    ll.clear()
    print(ll)
