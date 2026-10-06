# Задание 4: знакочередующаяся биномиальная сумма.

from math import comb


def alternating_binomial_sum(n: int) -> int:
    # Вычисляет сумму из условия задания.
    return sum((-1) ** k * (k - 1) * comb(n, k) for k in range(2, n + 1))


def main() -> None:
    values = [alternating_binomial_sum(n) for n in range(2, 16)]
    assert all(value == 1 for value in values)
    print("4. Знакочередующаяся сумма равна 1 для n = 2...15")


if __name__ == "__main__":
    main()
