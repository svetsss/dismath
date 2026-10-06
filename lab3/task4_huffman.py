# Задание 4: кодирование и декодирование по Хаффману.

from heapq import heappop, heappush
from math import ceil, log2
from typing import Optional


FREQUENCIES = {"A": 1, "B": 4, "C": 14, "D": 16, "E": 18, "F": 20, "G": 27}


class HuffmanNode:
    # Узел дерева Хаффмана.

    def __init__(
        self,
        symbol: Optional[str] = None,
        left: Optional[object] = None,
        right: Optional[object] = None,
    ) -> None:
        self.symbol = symbol
        self.left = left
        self.right = right


def huffman_codes(frequencies: dict) -> dict:
    # Строит префиксный код по частотам символов.
    heap = []
    serial = 0

    for symbol, frequency in sorted(frequencies.items()):
        heappush(heap, (frequency, serial, HuffmanNode(symbol=symbol)))
        serial += 1

    while len(heap) > 1:
        left_frequency, _, left = heappop(heap)
        right_frequency, _, right = heappop(heap)
        parent = HuffmanNode(left=left, right=right)
        heappush(heap, (left_frequency + right_frequency, serial, parent))
        serial += 1

    codes: dict = {}

    def walk(node: HuffmanNode, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"
            return
        walk(node.left, prefix + "0")
        walk(node.right, prefix + "1")

    walk(heap[0][2], "")
    return codes


def huffman_decode(bits: str, codes: dict) -> str:
    # Восстанавливает строку по таблице кодов.
    symbols = {code: symbol for symbol, code in codes.items()}
    decoded = []
    prefix = ""

    for bit in bits:
        prefix += bit
        if prefix in symbols:
            decoded.append(symbols[prefix])
            prefix = ""

    if prefix:
        raise ValueError("Неполная кодовая последовательность")
    return "".join(decoded)


def main() -> None:
    codes = huffman_codes(FREQUENCIES)
    example = "ABCDEFG"
    encoded_example = "".join(codes[symbol] for symbol in example)
    assert huffman_decode(encoded_example, codes) == example

    compressed_bits = sum(
        FREQUENCIES[symbol] * len(code)
        for symbol, code in codes.items()
    )
    original_bits = sum(FREQUENCIES.values()) * ceil(log2(len(FREQUENCIES)))
    saving = (1 - compressed_bits / original_bits) * 100

    print(f"4. Хаффман: {original_bits} -> {compressed_bits} бит, экономия {saving:.2f}%")


if __name__ == "__main__":
    main()
