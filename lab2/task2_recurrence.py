# Задание 2: вычисление рекуррентной последовательности.

from fractions import Fraction


INITIAL_VALUES = [5, 3, 3]


def recurrence_values(limit: int) -> list:
    # Вычисляет значения от x_0 до x_limit по рекуррентной формуле.
    values = INITIAL_VALUES.copy()

    while len(values) <= limit:
        next_value = -2 * values[-1] + 5 * values[-2] + 6 * values[-3] + 3
        values.append(next_value)

    return values[: limit + 1]


def closed_form(n: int) -> Fraction:
    # Вычисляет x_n по явной формуле.
    return (
        Fraction(11, 5) * 2**n
        + Fraction(17, 4) * (-1) ** n
        - Fraction(43, 40) * (-3) ** n
        - Fraction(3, 8)
    )


def main() -> None:
    recurrence = recurrence_values(10)
    formula = [closed_form(n) for n in range(11)]
    assert recurrence == [int(value) for value in formula]

    print("2. x_0...x_10:", recurrence)
    print("x_10 по явной формуле:", formula[10])


if __name__ == "__main__":
    main()
