from random import choice
from typing import Optional

from colorama import Fore, Style, init as colorama_init

class Animal:
    """
    Um Animal
    """
    pass

class Urso(Animal):
    """
    Um Urso
    """
    def __str__(self) -> str:
        return f'{Fore.RED} 󱣻 {Style.RESET_ALL}'

class Peixe(Animal):
    """
    Um Peixe
    """
    def __str__(self) -> str:
        return f'{Fore.GREEN}  {Style.RESET_ALL}'


def random_animal() -> Optional[Animal]:
    return choice([None, Urso(), Peixe()])


def random_empty_pos(river: list[Optional[Animal]]) -> Optional[int]:
    empty_spots: list[int] = [i for i, pos in enumerate(river) if pos is None]
    return choice(empty_spots) if empty_spots else None


class Rio:
    """
    Um Rio
    """
    def __init__(self, tamanho: int) -> None:
        self.__tamanho: int = tamanho
        self.__rio: list[Optional[Animal]] = [random_animal() for _ in range(tamanho)]

    def render_river(self) -> None:
        print('|' + ''.join(str(a) if a else f'{Fore.BLUE} - {Style.RESET_ALL}' for a in self.__rio) + '|')

    def move_animals(self) -> None:
        new_river: list[Optional[Animal]] = self.__rio.copy()
        moved: list[bool] = [False] * self.__tamanho

        for i in range(self.__tamanho):
            if self.__rio[i] is None or moved[i]:
                continue

            direction: int = choice([-1, 0, 1])
            new_pos: int = i + direction

            if new_pos < 0 or new_pos >= self.__tamanho or direction == 0:
                continue

            animal: Animal = self.__rio[i]
            final_pos: Optional[Animal] = self.__rio[new_pos]

            match (animal, final_pos):
                case (_, None):
                    new_river[new_pos] = animal
                    new_river[i] = None
                    moved[i] = True

                case (a1, a2) if type(a1) == type(a2):
                    new_empty_pos: Optional[int] = random_empty_pos(self.__rio)
                    if new_empty_pos is not None:
                        new_river[new_empty_pos] = type(animal)()
                case (Urso(), Peixe()):
                    new_river[new_pos] = animal
                    new_river[i] = None
                    moved[new_pos] = True

                case (Peixe(), Urso()):
                    new_river[i] = None

                case _:
                    pass
        self.__rio = new_river


if __name__ == '__main__':
    rio: Rio = Rio(10)

    colorama_init()
    print("[  ] <- if you can't see this symbol, you're not using a NerdFont")

    game_round: int
    for game_round in range(5):
        print(f'Rodada {game_round + 1}:')
        rio.render_river()
        rio.move_animals()

