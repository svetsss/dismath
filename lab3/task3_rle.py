# Задание 3: кодирование серий RLE.


SOURCE = b"aaaaadggggggggggggggghtyiklooooop"


def rle_encode(data: bytes) -> bytes:
    # Кодирует серии и последовательности одиночных байтов.
    encoded = bytearray()
    index = 0

    while index < len(data):
        run_length = 1
        while (
            index + run_length < len(data)
            and data[index + run_length] == data[index]
            and run_length < 255
        ):
            run_length += 1

        if run_length >= 2:
            encoded.extend((run_length, data[index]))
            index += run_length
            continue

        literals = bytearray([data[index]])
        index += 1

        while index < len(data) and len(literals) < 255:
            next_is_repetition = (
                index + 1 < len(data)
                and data[index] == data[index + 1]
            )
            if next_is_repetition:
                break
            literals.append(data[index])
            index += 1

        encoded.extend((0, len(literals)))
        encoded.extend(literals)

    return bytes(encoded)


def main() -> None:
    encoded = rle_encode(SOURCE)
    saving = (1 - len(encoded) / len(SOURCE)) * 100
    print(f"3. RLE: {len(SOURCE)} -> {len(encoded)} байт, экономия {saving:.2f}%")


if __name__ == "__main__":
    main()
