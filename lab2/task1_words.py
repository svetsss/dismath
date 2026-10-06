# Задание 1: подсчёт различных пятибуквенных слов.

from collections import Counter


WORD = "ЧЕРЕСПОЛОСИЦА"


def unique_words(source: str, length: int) -> list:
    # Строит слова без повторного использования экземпляров букв.
    remaining = Counter(source)
    words: list = []

    def build(prefix: list) -> None:
        if len(prefix) == length:
            words.append("".join(prefix))
            return

        for letter in sorted(remaining):
            if remaining[letter] == 0:
                continue

            remaining[letter] -= 1
            prefix.append(letter)
            build(prefix)
            prefix.pop()
            remaining[letter] += 1

    build([])
    return words


def main() -> None:
    words = unique_words(WORD, 5)
    print("1. Число пятибуквенных слов:", len(words))


if __name__ == "__main__":
    main()
