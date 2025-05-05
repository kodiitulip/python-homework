from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Protocol, Optional


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: T, other: T) -> bool:
        pass


T = TypeVar('T', bound=Comparable)


class Node(Generic[T]):
    def __init__(self, data: T = None, next_: Optional[Node[T]] = None):
        self.data: T = data
        self.next: Optional[Node[T]] = next_

    def __repr__(self) -> str:
        return repr(self.data) + (' -> ' + repr(self.next) if self.next else '')

    def __str__(self) -> str:
        return str(self.data) + (' -> ' + str(self.next) if self.next else '')


class LinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None

    def prepend(self, data: T) -> None:
        node: Node[T] = Node(data, self.head)
        self.head = node

    def append(self, data: T) -> None:
        if self.head is None:
            self.head = Node[T](data)
            return
        itr = self.head
        while itr.next:
            itr = itr.next
        itr.next = Node[T](data)

    def append_list(self, data_list: list[T]):
        for data in data_list:
            self.append(data)

    def __len__(self) -> int:
        count = 0
        itr = self.head

        while itr:
            count += 1
            itr = itr.next

        return count

    def remove_at(self, index: int) -> None:
        if index < 0 or index > len(self):
            raise Exception('Not a valid Index')

        if index == 0:
            self.head = self.head.next
            return

        count = 0
        itr = self.head
        while itr:
            if count == index -1:
                itr.next = itr.next.next
                break
            itr = itr.next
            count += 1

    def __repr__(self) -> str:
        if self.head is None:
            return f'{self.__class__} is empty'
        return f'{self.__class__!s} {repr(self.head)}'

    def __str__(self) -> str:
        if self.head is None:
            return 'Linked List is Empty'
        return str(self.head)


if __name__ == '__main__':
    ll = LinkedList[int]()
    ll.prepend(5)
    ll.prepend(89)
    ll.append(120)
    ll.append_list([12, 10, 9, 8, 7, 6])
    ll.remove_at(3)
    # ll.remove_at(120)
    print(ll)
    print(f'Length: {len(ll)}')
