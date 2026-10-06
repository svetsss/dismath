# Задание 5: арифметическое кодирование строки.

from fractions import Fraction
from math import ceil, log2


PROBABILITIES = {
    "a": Fraction(5, 100),
    "b": Fraction(10, 100),
    "c": Fraction(5, 100),
    "d": Fraction(55, 100),
    "e": Fraction(15, 100),
    "f": Fraction(10, 100),
}


def arithmetic_interval(text: str, probabilities: dict) -> tuple:
    # Последовательно сужает интервал для символов строки.
    intervals = {}
    boundary = Fraction(0)

    for symbol, probability in probabilities.items():
        intervals[symbol] = (boundary, boundary + probability)
        boundary += probability

    low, high = Fraction(0), Fraction(1)
    for symbol in text:
        width = high - low
        symbol_low, symbol_high = intervals[symbol]
        high = low + width * symbol_high
        low = low + width * symbol_low

    return low, high


def shortest_binary_prefix(low: Fraction, high: Fraction) -> str:
    # Находит кратчайший двоичный интервал внутри результата.
    for length in range(1, 256):
        scale = 1 << length
        numerator = (
            low.numerator * scale + low.denominator - 1
        ) // low.denominator
        left = Fraction(numerator, scale)
        right = Fraction(numerator + 1, scale)

        if left >= low and right <= high:
            return f"{numerator:0{length}b}"

    raise RuntimeError("Не удалось найти двоичный префикс")


def main() -> None:
    text = "eacdbf"
    low, high = arithmetic_interval(text, PROBABILITIES)
    code = shortest_binary_prefix(low, high)
    original_bits = len(text) * ceil(log2(len(PROBABILITIES)))
    saving = (1 - len(code) / original_bits) * 100

    assert code == "11000000010100001001"
    print(f"5. Арифметический код: {original_bits} -> {len(code)} бит, {saving:.2f}%")


if __name__ == "__main__":
    main()
