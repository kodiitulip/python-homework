"""
Escreva um programa em Python que simula um ecossistema.
Este ecossistema consiste em um rio, modelado como uma lista,
que contem dois tipos de animais: ursos e peixes.

No ecossistema, cada elemento da lista deve ser um objeto do
tipo Urso, Peixe ou None (que indica que a posição do rio
está vazia).

A cada rodada do jogo, baseada em um processo aleatório, cada
animal tenta se mover para uma posição da lista adjacente (a
esquerda ou direita) ou permanece na sua mesma posição.

Se dois animais do mesmo tipo colidirem (urso com urso ou peixe com peixe),
eles permanecem em suas posições originais, mas uma nova instância do
animal deve ser posicionada em um local vazio, aleatoriamente determinado.

Se um Urso e um peixe colidirem, entretanto, o peixe morre.
"""
from random import randint, choice, seed
from abc import ABC, abstractmethod
from typing import Self


class Jogo:

    def __init__(self, tamanho, ursos, peixes, num_rodadas, fixed_seed = -1):
        if fixed_seed != -1:
            seed(fixed_seed)
        self.__ecossistema = Rio(tamanho, ursos, peixes)
        self.__num_rodadas = num_rodadas


    def run(self):
        print(self.__ecossistema)
        for x in range(self.__num_rodadas):
            self.__ecossistema.rodada()
            print(self.__ecossistema)


class Rio:
    def __init__(self, tamanho_rio: int, qtd_ursos: int, qtd_peixes: int):
        self.__rio: list[None | Animal] = [None] * tamanho_rio
        self.__popular_rio(qtd_ursos, qtd_peixes)

    def __popular_rio(self, qtd_ursos: int, qtd_peixes: int):
        self.__posicionar(Urso, qtd_ursos)
        self.__posicionar(Peixe, qtd_peixes)

    def __posicionar(self, classe, qtd: int) -> None:
        empty_poss = self.__rio.count(None)
        if empty_poss < qtd:
            return

        for _ in range(qtd):
            pos = randint(0, len(self.__rio) - 1)
            while self.__rio[pos] is not None:
                pos = randint(0, len(self.__rio) - 1)
            self.__rio[pos] = classe()

    def rodada(self) -> None:
        for x in range(len(self.__rio)):
            if self.__rio[x] is None:
                continue

            direcao: int = choice([-1, 0, 1])
            nova_posicao: int = (x + direcao) % len(self.__rio)
            if nova_posicao != x and 0 <= nova_posicao < len(self.__rio):
                self.__colisao(x, nova_posicao)

    def __colisao(self, posicao_atual: int, nova_posicao: int) -> None:
        animal_atual: Animal | None = self.__rio[posicao_atual]
        animal_novo: Animal | None = self.__rio[nova_posicao]

        acao = animal_atual.interagir(animal_novo)

        match acao:
            case "comer":
                self.__rio[nova_posicao] = animal_atual
                self.__rio[posicao_atual] = None
            case "morrer":
                self.__rio[posicao_atual] = None
            case "reproduzir":
                self.__posicionar(type(animal_atual), 1)
            case "mover":
                self.__rio[nova_posicao] = animal_atual
                self.__rio[posicao_atual] = None
            case _:
                raise Exception('ação não reconhecida')

    def __str__(self):
        return "".join(str(animal) if animal else " | " for animal in self.__rio)


class Animal(ABC):
    @abstractmethod
    def interagir(self, outro: Self) -> str:
        """
        Define a interação entre dois animais. Possíveis ações:

        - "comer": o animal come o outro
        - "morrer": o animal morre
        - "reproduzir": o animal se reproduz
        """
        ...


class Urso(Animal):
    def interagir(self, outro: Animal) -> str:
        if isinstance(outro, Peixe):
            return "comer"

        elif isinstance(outro, Urso):
            return "reproduzir"

        else:
            return "mover"

    def __str__(self):
        return " U "


class Peixe(Animal):
    def interagir(self, outro: Animal) -> str:
        if isinstance(outro, Urso):
            return "morrer"

        elif isinstance(outro, Peixe):
            return "reproduzir"

        else:
            return "mover"

    def __str__(self):
        return " P "


if __name__ == '__main__':
    jogo = Jogo(10, 2, 3, 5, 4)
    jogo.run()
