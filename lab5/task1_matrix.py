# Задание 1: порождающая матрица, кодовые слова и расстояние.

from itertools import combinations


N = 15
M = 5
GENERATOR = "10100110111"


# переводит двоичную строку в целое число
def bits_to_int(bits: str) -> int:
    return int(bits, 2)


# записывает число как двоичную строку фиксированной длины
def bit_string(value: int, width: int = N) -> str:
    return f"{value:0{width}b}"


# находит остаток от деления многочленов над полем GF(2)
def polynomial_remainder(value: int, divisor: int) -> int:
    divisor_degree = divisor.bit_length() - 1

    while value and value.bit_length() - 1 >= divisor_degree:
        shift = value.bit_length() - 1 - divisor_degree
        value ^= divisor << shift

    return value


# кодирует сообщение систематическим циклическим кодом
def systematic_encode(message: int) -> int:
    shifted = message << (N - M)
    remainder = polynomial_remainder(shifted, bits_to_int(GENERATOR))
    return shifted ^ remainder


# строит порождающую матрицу по кодам базисных сообщений
def build_generator_matrix() -> list:
    return [
        systematic_encode(1 << (M - row - 1))
        for row in range(M)
    ]


# вычисляет кодовое слово как произведение сообщения на матрицу
def encode_by_matrix(message: int, matrix: list) -> int:
    codeword = 0

    for row, matrix_row in enumerate(matrix):
        message_bit = 1 << (M - row - 1)
        if message & message_bit:
            codeword ^= matrix_row

    return codeword


# вычисляет все кодовые слова по порождающей матрице
def build_codewords(matrix: list) -> dict:
    return {
        message: encode_by_matrix(message, matrix)
        for message in range(1 << M)
    }


# считает количество единиц в двоичной записи числа
def hamming_weight(value: int) -> int:
    return bin(value).count("1")


# вычисляет расстояние Хемминга
def hamming_distance(left: int, right: int) -> int:
    return hamming_weight(left ^ right)


# находит минимальное расстояние между кодовыми словами
def minimum_distance(codewords: dict) -> int:
    return min(
        hamming_distance(left, right)
        for left, right in combinations(codewords.values(), 2)
    )


# строит матрицу расстояний для выбранного фрагмента кода
def build_distance_matrix(fragment: list) -> list:
    return [
        [hamming_distance(left, right) for _, right in fragment]
        for _, left in fragment
    ]


def main() -> None:
    matrix = build_generator_matrix()
    codewords = build_codewords(matrix)
    distance = minimum_distance(codewords)

    assert len(set(codewords.values())) == 1 << M
    assert all(
        polynomial_remainder(codeword, bits_to_int(GENERATOR)) == 0
        for codeword in codewords.values()
    )

    print("1. Порождающая матрица:")
    for row in matrix:
        print("   " + " ".join(bit_string(row)))
    print(f"Всего кодовых слов: {len(codewords)}")
    print(f"Минимальное кодовое расстояние: {distance}")


if __name__ == "__main__":
    main()
