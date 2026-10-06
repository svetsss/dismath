# Задание 1: кодирование и исправление ошибок кодом Хемминга.


def bytes_to_bits(data: bytes) -> str:
    # Переводит последовательность байтов в двоичную строку.
    return "".join(f"{byte:08b}" for byte in data)


def hamming_encode(data_bits: str) -> str:
    # Добавляет контрольные биты с проверкой на чётность.
    check_bits = 0
    while 2**check_bits < len(data_bits) + check_bits + 1:
        check_bits += 1

    code = [0] * (len(data_bits) + check_bits + 1)
    data = iter(map(int, data_bits))

    for position in range(1, len(code)):
        if position & (position - 1):
            code[position] = next(data)

    for bit in range(check_bits):
        check_position = 1 << bit
        parity = 0
        for position in range(1, len(code)):
            if position & check_position:
                parity ^= code[position]
        code[check_position] = parity

    return "".join(map(str, code[1:]))


def hamming_decode(codeword: str) -> tuple:
    # Исправляет одну ошибку и возвращает информационные биты.
    code = [0] + list(map(int, codeword))
    syndrome = 0
    bit = 0

    while (1 << bit) < len(code):
        check_position = 1 << bit
        parity = 0
        for position in range(1, len(code)):
            if position & check_position:
                parity ^= code[position]
        if parity:
            syndrome += check_position
        bit += 1

    if syndrome:
        code[syndrome] ^= 1

    data_bits = "".join(
        str(code[position])
        for position in range(1, len(code))
        if position & (position - 1)
    )
    return data_bits, syndrome


def flip_bit(bits: str, position: int) -> str:
    # Инвертирует бит; позиции нумеруются с единицы.
    changed = list(bits)
    changed[position - 1] = "1" if changed[position - 1] == "0" else "0"
    return "".join(changed)


def main() -> None:
    source = "kantiana"
    bits = bytes_to_bits(source.encode("cp1251"))
    blocks = [bits[:32], bits[32:]]
    error_positions = [7, 17]

    encoded = [hamming_encode(block) for block in blocks]
    damaged = [flip_bit(block, error) for block, error in zip(encoded, error_positions)]
    decoded = [hamming_decode(block) for block in damaged]

    restored_bits = "".join(data for data, _ in decoded)
    restored = int(restored_bits, 2).to_bytes(8, "big").decode("cp1251")
    syndromes = [syndrome for _, syndrome in decoded]

    assert restored == source
    print("1. Восстановленная строка:", restored)
    print("Синдромы:", syndromes)


if __name__ == "__main__":
    main()
