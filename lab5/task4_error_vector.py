# Задание 4: ошибка, которая обнаруживается, но не исправляется.

from task1_matrix import (
    GENERATOR,
    M,
    N,
    bit_string,
    bits_to_int,
    build_codewords,
    build_generator_matrix,
    hamming_weight,
    minimum_distance,
    polynomial_remainder,
)
from task2_capabilities import code_capabilities
from task3_examples import nearest_decode


# находит конкретный пример ошибки за пределами исправляющей способности
def find_uncorrectable_error(codewords: dict) -> tuple:
    distance = minimum_distance(codewords)
    correctable, _ = code_capabilities(distance)
    nearest_message = min(
        (message for message in codewords if message != 0),
        key=lambda message: hamming_weight(codewords[message]),
    )
    nearest_word = codewords[nearest_message]
    support = [
        position
        for position in range(N)
        if nearest_word & (1 << position)
    ]
    error = sum(1 << position for position in support[:correctable + 1])
    syndrome = polynomial_remainder(error, bits_to_int(GENERATOR))
    decoded, decoded_distance, unique = nearest_decode(error, codewords)

    assert syndrome != 0
    assert unique and decoded != 0
    return error, syndrome, decoded, decoded_distance


def main() -> None:
    matrix = build_generator_matrix()
    codewords = build_codewords(matrix)
    error, syndrome, decoded, decoded_distance = find_uncorrectable_error(codewords)

    print("\n4. Ошибка обнаруживается, но не исправляется:")
    print(f"Вектор ошибки: {bit_string(error)}")
    print(f"Синдром: {bit_string(syndrome, N - M)}")
    print(
        f"Вместо 00000 декодировано {decoded:05b}, "
        f"расстояние до выбранного слова: {decoded_distance}"
    )


if __name__ == "__main__":
    main()
