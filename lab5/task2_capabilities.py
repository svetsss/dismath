# Задание 2: исправляющая и обнаруживающая способности кода.

from task1_matrix import build_codewords, build_generator_matrix, minimum_distance


# вычисляет гарантированное число исправляемых и обнаруживаемых ошибок
def code_capabilities(distance: int) -> tuple:
    correctable = (distance - 1) // 2
    detectable = distance - 1
    return correctable, detectable


def main() -> None:
    matrix = build_generator_matrix()
    codewords = build_codewords(matrix)
    distance = minimum_distance(codewords)
    correctable, detectable = code_capabilities(distance)

    print("\n2. Характеристики кода:")
    print(f"Гарантированно исправляет ошибок: {correctable}")
    print(f"Гарантированно обнаруживает ошибок: {detectable}")


if __name__ == "__main__":
    main()
