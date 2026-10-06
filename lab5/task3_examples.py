# Задание 3: примеры исправления и обнаружения ошибок.

from task1_matrix import (
    GENERATOR,
    M,
    N,
    bit_string,
    bits_to_int,
    build_codewords,
    build_generator_matrix,
    hamming_distance,
    polynomial_remainder,
)


# находит ближайшее кодовое слово
def nearest_decode(received: int, codewords: dict) -> tuple:
    distances = [
        (hamming_distance(received, codeword), message)
        for message, codeword in codewords.items()
    ]
    best_distance = min(distance for distance, _ in distances)
    candidates = [
        message
        for distance, message in distances
        if distance == best_distance
    ]
    return candidates[0], best_distance, len(candidates) == 1


# создаёт пример исправления трёх ошибок
def correction_example(codewords: dict) -> tuple:
    message = 0b10110
    codeword = codewords[message]
    error = sum(1 << position for position in (0, 4, 9))
    received = codeword ^ error
    decoded, distance, unique = nearest_decode(received, codewords)

    assert unique and decoded == message and distance == 3
    return message, codeword, error, received, decoded


# создаёт пример обнаружения шести ошибок
def detection_example() -> tuple:
    error = sum(1 << position for position in range(6))
    syndrome = polynomial_remainder(error, bits_to_int(GENERATOR))

    assert syndrome != 0
    return error, syndrome


def main() -> None:
    matrix = build_generator_matrix()
    codewords = build_codewords(matrix)
    message, codeword, error, received, decoded = correction_example(codewords)
    detection_error, syndrome = detection_example()

    print("\n3. Примеры:")
    print(
        f"   {message:05b} → {bit_string(codeword)}, "
        f"ошибка {bit_string(error)}, принято {bit_string(received)}"
    )
    print(f"После исправления: {decoded:05b}")
    print(
        f"Ошибка веса 6: {bit_string(detection_error)}, "
        f"синдром {bit_string(syndrome, N - M)}"
    )


if __name__ == "__main__":
    main()
