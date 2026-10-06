# Задание 5: подсчёт кратчайших путей в прямоугольной сетке.


def lattice_paths(width: int, height: int, forbid_two_vertical: bool) -> int:
    # Считает пути динамическим программированием.
    # Последний индекс показывает, был ли предыдущий шаг вертикальным.
    paths = [[[0, 0] for _ in range(height + 1)] for _ in range(width + 1)]
    paths[0][0][0] = 1

    for x in range(width + 1):
        for y in range(height + 1):
            if x < width:
                paths[x + 1][y][0] += sum(paths[x][y])

            if y < height:
                paths[x][y + 1][1] += paths[x][y][0]
                if not forbid_two_vertical:
                    paths[x][y + 1][1] += paths[x][y][1]

    return sum(paths[width][height])


def main() -> None:
    all_paths = lattice_paths(19, 18, False)
    restricted_paths = lattice_paths(19, 18, True)
    print("5. Все кратчайшие пути:", all_paths)
    print("Без двух вертикальных шагов подряд:", restricted_paths)


if __name__ == "__main__":
    main()
