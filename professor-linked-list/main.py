from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class ListADT(ABC):

    @abstractmethod
    def insert(self, indice, elemento):
        """
        Insere na posição <indice> o valor <elemento>.
        Como se trata de uma lista, deve ser graratido que
        se houver valor em <indice> que ele não seja apagado
        """
        ...

    @abstractmethod
    def remove(self, elemento):
        """Remove primeira ocorrência de <elemento>"""
        ...

    @abstractmethod
    def count(self, elemento):
        """Conta a quantidade de <elemento> na lista"""
        ...

    @abstractmethod
    def clear(self):
        """Apaga a lista"""
        ...

    @abstractmethod
    def index(self, elemento):
        """Retorna o primeiro índice de <elemento>"""
        ...

    @abstractmethod
    def length(self):
        """Retorna o tamanho da lista"""
        ...

    @abstractmethod
    def remove_all(self, item):
        ...

    @abstractmethod
    def remove_at(self, index):
        ...

    @abstractmethod
    def append(self, item):
        ...

    @abstractmethod
    def replace(self, index, item):
        ...


class Node[T]:

    def __init__(self, element: T, next_: Optional[Node[T]]=None) -> None:
        self.__element: T = element
        self.__next: Optional[Node[T]] = next_

    def get_next(self) -> Optional[Node[T]]:
        return self.__next

    def set_next(self, next_: Node[T]) -> None:
        self.__next = next_

    def get_element(self) -> T:
        return self.__element

    def set_element(self, element: T) -> None:
        self.__element = element

    def __str__(self) -> str:
        return '|' + self.__element.__str__() + '|'


class LinkedList[E](ListADT):

    def __init__(self, elem: Optional[Node[E]] = None):
        self._head: Optional[Node[E]] = Node[E](elem) if elem else None  # Atenção ao manipular essa referência
        self._tail: Optional[Node[E]] = self._head if elem else None  # Facilita a inserção no fim da lista
        self._length: int = 1 if elem else 0

    def remove_all(self, item: E) -> None:
        if self.empty():
            return

        while self._head.get_element() == item:
            self._head = self._head.get_next()
        itr: Optional[Node[E]] = self._head
        while itr:
            next_ = itr.get_next()
            if next_ and next_.get_element() == item:
                itr.set_next(next_.get_next())
            else:
                itr = itr.get_next()

    def remove_at(self, index: int) -> None:
        pos: int = 0
        itr: Optional[Node[E]] = self._head
        while itr.get_next() and pos < index - 1:
            itr = itr.get_next()
            pos += 1
        to_remove = itr.get_next()
        itr.set_next(to_remove.get_next())

    def append(self, item: E) -> None:
        if self.empty():
            return self.__insert_at_beginning(item)
        return self.__insert_at_end(item)

    def replace(self, index, item: E) -> None:
        if index > self._length - 1:
            return
        pos: int = 0
        itr: Optional[Node[E]] = self._head
        while itr.get_next() and pos < index:
            itr = itr.get_next()
            pos += 1
        itr.set_element(item)

    def insert(self, index: int, elem: E) -> None:
        # a inserção pode acontecer em três locais: início, meio e fim da lista
        # separei em mÃ©todos diferentes (privados) para facilitar o entendimento
        if index == 0:  # primeiro local de inserção é no começo da lista
            self.__insert_at_beginning(elem)
        elif index > self._length:  # segundo local de inserção é no fim da lista
            self.__insert_at_end(elem)  # se o índice passado foi maior que o tamanho da lista, inserir no fim
        else:  # por fim, a inserção no meio da lista
            self.__insert_in_between(index, elem)

        self._length += 1  # após inserido, o tamanho da lista é modificado

    def __insert_at_beginning(self, elem: E) -> None:
        n = Node[E](elem)  # primeiro criamos o nó com o elemento a ser inserido
        if self.empty():  # caso particular da lista vazia
            self.__empty_list_insertion(n)
        else:  # se houver elemento na lista
            n.set_next(self._head)  # o head atual passa a ser o segundo elemento
            self._head = n  # e o novo nó criado passa a ser o novo head

    def __insert_at_end(self, elem: E) -> None:
        n = Node[E](elem)  # primeiro criamos o nó com o elemento a ser inserido
        if self.empty():  # caso particular da lista vazia
            self.__empty_list_insertion(n)
        else:
            self._tail.set_next(n)  # o último elemento da lista aponta para o nó criado
            self._tail = n  # o nó criado ...a a ser o último elemento

    def __empty_list_insertion(self, node: Node[E]) -> None:
        # na inserção na lista vazia, head e tail apontam para o nó
        self._head = node
        self._tail = node

    def __insert_in_between(self, index: int, elem: E) -> None:  # 3
        n = Node[E](elem)  # primeiro criamos o nó com o elemento a ser inserido
        pos: int = 0  # a partir daqui vamos localizar a posição de inserção
        aux: Node[E] = self._head  # variável auxiliar para nos ajudar na configuração da posição do novo nó
        while pos < index - 1:  # precorre a lista atÃ© a posição imediatamente anterior
            aux = aux.get_next()  # Ã posição onde o elemento será inserido
            pos += 1
        n.set_next(aux.get_next())  # quando a posição correta tiver sido alcançada, insere o nó
        aux.set_next(n)

    def remove(self, elem: E) -> None:
        if self.empty():
            return
        aux: Node[E] = self._head
        removed: bool = False  # Flag que marca quando a remoção foi feita
        if aux.get_element() == elem:  # Caso especial: elemento a ser removido está no head
            self._head = aux.get_next()  # head passa a ser o segundo elemento da lista
        else:
            while aux.get_next() and not removed:  # verifico se estamos no fim da lista e não foi removido elemento
                prev: Node[E] = aux
                aux = aux.get_next()  # passo para o próximo elemento
                if aux.get_element() == elem:  # se for o elemento desejado, removo da lista
                    prev.set_next(aux.get_next())
                    removed = True  # marco que foi removido

        if removed:
            self._length -= 1

    def count(self, elem: E) -> int:
        counter: int = 0
        if self.empty():
            return counter
        aux: Node[E] = self._head  # Se a lista não estiver vazia, percorre a lista contando as ocorrências
        if aux.get_element() is elem:
            counter += 1
        while aux.get_next():  # precorrendo a lista....
            aux = aux.get_next()
            if aux.get_element() is elem:
                counter += 1
        return counter

    def clear(self) -> None:
        self._head = None  # todos os nós que compunham a lista serão removidos da memória pelo coletor de lixo
        self._tail = None
        self._length = 0

    def index(self, elem: E) -> Optional[int]:
        result: Optional[int] = None
        pos: int = 0
        aux: Node[E] = self._head
        # Vamos percorrer a lista em busca de elem
        while not result and pos < self._length:  # lembrando que not None é o mesmo que True
            if aux.get_element() is elem:
                result = pos
                break
            aux = aux.get_next()
            pos += 1
        return result  # se o elemento não estiver na lista, retorna None

    def length(self) -> int:
        if self.empty():
            return 0
        count: int = 1
        itr: Optional[Node[E]] = self._head
        while itr.get_next():
            itr = itr.get_next()
            count += 1
        return count

    def empty(self) -> bool:
        return not self._head

    def __str__(self) -> str:
        if self.empty():
            return '||'
        result = ''
        aux: Node[E] = self._head
        result += aux.__str__()
        while aux.get_next():
            aux = aux.get_next()
            result += aux.__str__()
        return result


class DoublyLinkedList(ListADT):
    class _DoublyNode:
        def __init__(self, elem, prev, next_):
            self._elem = elem
            self._prev = prev
            self._next = next_

        def __str__(self):
            if self._elem is not None:
                return str(self._elem) + ' '
            else:
                return '|'

        @property
        def elem(self):
            return self._elem

        @elem.setter
        def elem(self, value):
            self._elem = value

        @property
        def next(self):
            return self._next

        @next.setter
        def next(self, value):
            self._next = value

        @property
        def prev(self):
            return self._prev

        @prev.setter
        def prev(self, value):
            self._prev = value

    def __init__(self):
        self._header = self._DoublyNode(None, None, None)
        self._trailer = self._DoublyNode(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._length = 0

    def remove_all(self, item) -> None:
        if self.empty():
            return

        while self._header.elem == item:
            self._header = self._header.next
        itr = self._header
        while itr:
            next_ = itr.next
            if next_ and next_.elem == item:
                itr.next = next_.next
            else:
                itr = itr.next

    def remove_at(self, index: int) -> None:
        pos: int = 0
        itr = self._header
        while itr.next and pos < index:
            itr = itr.next
            pos += 1
        to_remove = itr.next
        itr.next = to_remove.next

    def append(self, item) -> None:
        if self.empty():
            return self.insert(0, item)
        return self.insert(self.length() - 1, item)

    def replace(self, index, item) -> None:
        length: int = self.length()
        if index >= length:
            index = length
        pos: int = 0
        itr = self._header
        while itr.next and pos <= index:
            itr = itr.next
            pos += 1
        itr.elem = item

    def insert(self, index, elem):
        if index >= self._length:  # se o índice se inserção passado for maior que a lista
            index = self._length  # atualiza para o último índice
        if self.empty():  # Caso da lista vazia
            new_node = self._DoublyNode(elem, self._header, self._trailer)
            self._header.next = new_node
            self._trailer.prev = new_node
        elif index == 0:  # caso da inserção na primeira posição da lista
            new_node = self._DoublyNode(elem, self._header, self._header.next)
            self._header.next.prev = new_node
            self._header.next = new_node
        else:  # outros casos de inserção
            this = self._header.next
            successor = this.next
            pos = 0
            while pos < index - 1:
                this = successor
                successor = this.next
                pos += 1
            new_node = self._DoublyNode(elem, this, successor)
            this._next = new_node
            successor._prev = new_node

        self._length += 1

    def remove(self, elemento):
        if not self.empty():
            node = self._header.next
            pos = 0
            found = False
            while not found and pos < self._length:
                if node.elem == elemento:
                    found = True
                else:
                    node = node.next
                    pos += 1
            if found:
                node.prev.next = node.next
                node.next.prev = node.prev
                self._length -= 1

    def count(self, elem):
        result = 0
        this = self._header.next
        if self._length > 0:
            while this.next is not None:  # aqui a lista Ã© percorrida
                if this.elem == elem:
                    result += 1
                this = this.next
        return result

    def clear(self):
        self._header = self._DoublyNode(None, None, None)
        self._trailer = self._DoublyNode(None, None, None)
        self._header.next = self._trailer
        self._trailer.prev = self._header
        self._length = 0

    def index(self, elem):
        result = None  # armazena a primeira posição do elemento
        pos = 0
        this = self._header.next
        # Vamos percorrer a lista em busca de elem
        while not result and pos < self._length:  # lembrando que not None Ã© o mesmo que True
            if this.elem is elem:
                result = pos
                break
            this = this.next
            pos += 1
        return result  # se o elemento não estiver na lista, retorna None

    def length(self):
        if self.empty():
            return 0
        count: int = 1
        itr = self._header
        while itr.next:
            itr = itr.next
            count += 1
        return count

    def empty(self):
        return not self._header

    def __str__(self):
        if not self.empty():
            result = ''
            aux = self._header
            result += aux.__str__()
            while aux.next:
                aux = aux.next
                result += aux.__str__()
            return result
        else:
            return '||'



if __name__ == '__main__':
    print('Linked List')
    lista = LinkedList()
    print(lista)

    print('inserção')
    lista.insert(0, 'teste')
    print(lista)

    lista.insert(20, 20)
    print(lista)

    lista.insert(10000, 'loooonge')
    print(lista)

    lista.insert(0, 20)
    print(lista)

    print('contagem')
    print(lista.count('no meio'))
    print(lista.count('oi'))
    print(lista.count(20))

    print('indices')
    print(lista.index(20))
    print(lista.index('loooonge'))
    print(lista.index('bla'))
    print('remoção')

    print('lista inicial')
    print(lista)

    print('vamos remover...')
    lista.remove(20)
    print(lista)

    lista.remove('teste')
    print(lista)

    print('length')
    print(lista.length())

    print('append')
    lista.append(20)
    lista.append('oi')
    lista.append(20)
    lista.append(20)
    lista.append('test')
    lista.append(20)
    lista.append(20)
    print(lista)

    print('remove_at')
    lista.remove_at(3)
    print(lista)

    print('remove_all')
    lista.remove_all(20)
    print(lista)

    print('replace')
    lista.replace(1, 'oi')
    print(lista)

    print('''
-------------

-------------
Double Link List
    ''')

    lista = DoublyLinkedList()
    print(lista)

    print('inserção')
    lista.insert(0, 'teste')
    print(lista)

    lista.insert(20, 20)
    print(lista)

    lista.insert(10000, 'loooonge')
    print(lista)

    lista.insert(0, 20)
    print(lista)

    print('contagem')
    print(lista.count('no meio'))
    print(lista.count('oi'))
    print(lista.count(20))

    print('indices')
    print(lista.index(20))
    print(lista.index('loooonge'))
    print(lista.index('bla'))
    print('remoção')

    print('lista inicial')
    print(lista)

    print('vamos remover...')
    lista.remove(20)
    print(lista)

    lista.remove('teste')
    print(lista)

    print('length')
    print(lista.length())

    print('append')
    lista.append(20)
    lista.append('oi')
    lista.append(20)
    lista.append(20)
    lista.append('test')
    lista.append(20)
    lista.append(20)
    print(lista)

    print('remove_at')
    lista.remove_at(3)
    print(lista)

    print('remove_all')
    lista.remove_all(20)
    print(lista)

    print('replace')
    lista.replace(1, 'oi')
    print(lista)
