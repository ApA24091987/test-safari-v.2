import random


class Animal:

    def can_defeat(self, other):
        raise NotImplementedError("При не соответствии повторить еще раз!.")

    def symbol(self):
        return self.__class__.__name__[0]


class Lion(Animal):
    def can_defeat(self, other):
        return isinstance(other, (Tiger, Wolf, Deer))


class Tiger(Animal):
    def can_defeat(self, other):
        return isinstance(other, (Wolf, Deer))


class Wolf(Animal):
    def can_defeat(self, other):
        return isinstance(other, Deer)


class Deer(Animal):
    def can_defeat(self, other):
        return False


ANIMAL_CLASSES = [Lion, Tiger, Wolf, Deer]


def create_board(size=10):
    return [
        [random.choice(ANIMAL_CLASSES)() for _ in range(size)]
        for _ in range(size)
    ]


def print_board(board, conquered=None, chosen=None):
    for i, row in enumerate(board):
        line = []
        for j, animal in enumerate(row):
            if conquered and (i, j) in conquered:
                if chosen and (i, j) == chosen:
                    line.append(animal.symbol())  # chosen cell stays as animal symbol
                else:
                    line.append('-')
            else:
                line.append(animal.symbol())
        print(' '.join(line))
    print()


def conquer(board, pos, conquered, original_animal, start_pos):
    size = len(board)
    i, j = pos

    if not (0 <= i < size and 0 <= j < size):
        return

    if (i, j) in conquered:
        return
    current_animal = board[i][j]

    if pos != start_pos and isinstance(current_animal, original_animal.__class__):
        return

    if pos != start_pos and not original_animal.can_defeat(current_animal):
        return
    conquered.add(pos)

    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            conquer(board, (ni, nj), conquered, original_animal, start_pos)


def main():
    size = 10
    board = create_board(size)
    print("Board at start:\n")
    print_board(board)

    i = random.randint(0, size - 1)
    j = random.randint(0, size - 1)
    animal = board[i][j]

    print(f"Chosen cell: [{i + 1},{j + 1}]: {animal.symbol()}\n")

    conquered = set()
    conquer(board, (i, j), conquered, animal, (i, j))

    print("Board after conquer:\n")
    print_board(board, conquered, (i, j))


if __name__ == "__main__":
    main()
