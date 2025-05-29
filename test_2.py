import random
from typing import List, Tuple, Set


class Animal:
    symbol = ''  
    def can_defeat(self, other: 'Animal') -> bool:
        return False

    def __str__(self) -> str:
        return self.symbol


class Deer(Animal):
    symbol = 'D'

    def can_defeat(self, other: 'Animal') -> bool:
        return False


class Wolf(Animal):
    symbol = 'W'

    def can_defeat(self, other: 'Animal') -> bool:
        return isinstance(other, Deer)


class Tiger(Animal):
    symbol = 'T'

    def can_defeat(self, other: 'Animal') -> bool:
        return isinstance(other, (Wolf, Deer))


class Lion(Animal):
    symbol = 'L'

    def can_defeat(self, other: 'Animal') -> bool:
        return isinstance(other, (Tiger, Wolf, Deer))


class SafariField:

    def __init__(self, size: int = 10):

        self.size = size
        self.board = self._populate_board()

    def _populate_board(self) -> List[List[Animal]]:

        animal_types = [Deer, Wolf, Tiger, Lion]
        board = []

        for _ in range(self.size):
            row = []
            for _ in range(self.size):
                animal_class = random.choice(animal_types)
                row.append(animal_class())
            board.append(row)

        return board

    def display_board(self, conquered_cells: Set[Tuple[int, int]] = None) -> None:

        if conquered_cells is None:
            conquered_cells = set()

        print("\nBoard:")
        for i in range(self.size):
            row_str = ""
            for j in range(self.size):
                if (i, j) in conquered_cells:
                    row_str += " -"
                else:
                    row_str += f" {self.board[i][j]}"
            print(row_str)

    def pick_random_cell(self) -> Tuple[int, int]:

        row = random.randint(0, self.size - 1)
        col = random.randint(0, self.size - 1)
        return (row, col)

    def find_conquerable_cells(self, start_cell: Tuple[int, int]) -> Set[Tuple[int, int]]:

        row, col = start_cell
        starting_animal = self.board[row][col]
        conquered = set()

        def conquer_recursive(r: int, c: int) -> None:

            if not (0 <= r < self.size and 0 <= c < self.size) or (r, c) in conquered:
                return

            target_animal = self.board[r][c]

            if r == row and c == col:
                conquered.add((r, c))

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        conquer_recursive(r + dr, c + dc)
            elif type(target_animal) != type(starting_animal) and starting_animal.can_defeat(target_animal):
                conquered.add((r, c))

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        conquer_recursive(r + dr, c + dc)

        conquer_recursive(row, col)
        return conquered


def main():
    safari = SafariField()

    safari.display_board()

    chosen_cell = safari.pick_random_cell()
    row, col = chosen_cell
    print(f"\nChosen cell: [{row + 1},{col + 1}]: {safari.board[row][col]}")

    conquered = safari.find_conquerable_cells(chosen_cell)

    print("\nBoard after conquer:")
    safari.display_board(conquered)


if __name__ == "__main__":
    main()
