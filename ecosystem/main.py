from random import choice, randint
from typing import Optional, Self


class Animal:
    def reproduce(self, river: list[Optional[Self]]):
        i: Optional[int] = random_empty_pos(river)
        if i is int:
            river[i] = type(self)()

    pass


class Urso(Animal):
    def __str__(self) -> str:
        return '-U-'


class Peixe(Animal):
    def __str__(self) -> str:
        return '-P-'


class Rio:
    def __init__(self, size: int, bear_amt: int, fish_amt: int) -> None:
        self.__size: int = size
        self.__rio: list[Optional[Animal]] = [None] * size
        self.__populate(bear_amt, fish_amt)

    def __place_animal(self, animal: Animal, amount: int) -> None:
        for i in range(amount):
            pos = random_empty_pos(self.__rio)
            self.__rio[pos] = animal

    def __populate(self, bear_amt: int, fish_amt: int) -> None:
        self.__place_animal(Urso(), bear_amt)
        self.__place_animal(Peixe(), fish_amt)

    def game_round(self, round_num: int) -> None:
        print(f'Rodada {round_num}:\n\t{self}')
        self.move_animals()

    def __str__(self) -> str:
        return ''.join(str(a) if a else '---' for a in self.__rio)

    def move_animals(self) -> None:
        for x in range(self.__size):
            if self.__rio[x] is None:
                continue
            direction = randint(-1, 1)
            new_pos = x + direction
            if direction != 0 and 0 <= new_pos < self.__size:
                self.__collide(x, new_pos)

    def __collide(self, start, end) -> None:
        curr_pos: Animal = self.__rio[start]
        next_pos: Optional[Animal] = self.__rio[end]

        match (curr_pos, next_pos):
            case (curr_pos, next_pos) if type(curr_pos) == type(next_pos):  # Animal <=> Animal
                mother = choice([curr_pos, next_pos])
                mother.reproduce(self.__rio)
            case (curr_pos, next_pos) if isinstance(curr_pos, Urso) and isinstance(next_pos, Peixe):  # Urso -> Peixe
                self.__rio[end] = curr_pos
                self.__rio[start] = None
            case (curr_pos, next_pos) if isinstance(curr_pos, Peixe) and isinstance(next_pos, Urso):  # Peixe -> Urso
                self.__rio[start] = None
            case _:  # Animal -> None
                self.__rio[end] = curr_pos
                self.__rio[start] = next_pos


def random_empty_pos(river: list[Optional[any]]) -> Optional[int]:
    empty_spots: list[int] = [i for i, pos in enumerate(river) if pos is None]
    return choice(empty_spots) if empty_spots else None


if __name__ == '__main__':
    rio: Rio = Rio(10, 2, 5)

    game_round: int
    for game_round in range(5):
        rio.game_round(game_round)
