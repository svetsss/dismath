# Задание 3: проверка тождества для чисел Фибоначчи.


def fibonacci(n: int) -> int:
    # Возвращает n-е число Фибоначчи.
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def identity_sides(n: int) -> tuple:
    # Вычисляет левую и правую части заданного тождества.
    left = sum((n + 1 - k) * fibonacci(k) for k in range(1, n + 1))
    right = fibonacci(n + 4) - (n + 3)
    return left, right


def main() -> None:
    for n in range(1, 16):
        left, right = identity_sides(n)
        assert left == right
    print("3. Тождество Фибоначчи проверено для n = 1...15")


if __name__ == "__main__":
    main()
