# Задание 2: коды с минимальными расстояниями 2 и 3.


LETTERS = "стуфхцчш"


def hamming_distance(left: str, right: str) -> int:
    # Считает число несовпадающих позиций двух слов.
    return sum(first != second for first, second in zip(left, right))


def minimum_distance(codebook: dict) -> int:
    # Находит минимальное расстояние между разными кодовыми словами.
    words = list(codebook.values())
    return min(
        hamming_distance(words[i], words[j])
        for i in range(len(words))
        for j in range(i + 1, len(words))
    )


def nearest_letter(received: str, codebook: dict) -> tuple:
    # Возвращает ближайшую букву и расстояние до неё.
    distance, letter = min(
        (hamming_distance(received, code), letter)
        for letter, code in codebook.items()
    )
    return letter, distance


def build_codes(letters: str) -> tuple:
    # Строит коды с минимальными расстояниями 2 и 3.
    even_codes = [
        "0000", "0011", "0101", "0110",
        "1001", "1010", "1100", "1111",
    ]
    distance_two = dict(zip(letters, even_codes))

    generator = ("100110", "010101", "001011")
    distance_three = {}

    for value, letter in enumerate(letters):
        data_bits = [(value >> shift) & 1 for shift in (2, 1, 0)]
        codeword = []

        for column in range(6):
            bit = sum(
                data_bits[row] * int(generator[row][column])
                for row in range(3)
            ) % 2
            codeword.append(str(bit))

        distance_three[letter] = "".join(codeword)

    return distance_two, distance_three


def flip_bit(bits: str, position: int) -> str:
    # Инвертирует один бит кодового слова.
    changed = list(bits)
    changed[position - 1] = "1" if changed[position - 1] == "0" else "0"
    return "".join(changed)


def main() -> None:
    code_d2, code_d3 = build_codes(LETTERS)
    distance_d2 = minimum_distance(code_d2)
    distance_d3 = minimum_distance(code_d3)

    damaged_d2 = flip_bit(code_d2["ф"], 2)
    assert damaged_d2 not in code_d2.values()

    damaged_d3 = flip_bit(code_d3["ф"], 4)
    letter, distance = nearest_letter(damaged_d3, code_d3)
    assert letter == "ф" and distance == 1

    print("2. Минимальные расстояния:", distance_d2, "и", distance_d3)
    print("После исправления:", letter, "на расстоянии", distance)


if __name__ == "__main__":
    main()
