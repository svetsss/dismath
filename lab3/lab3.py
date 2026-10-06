# Запускает все задания лабораторной работы №3.

from task1_hamming import main as run_task1
from task2_distance import main as run_task2
from task3_rle import main as run_task3
from task4_huffman import main as run_task4
from task5_arithmetic import main as run_task5


def main() -> None:
    run_task1()
    run_task2()
    run_task3()
    run_task4()
    run_task5()


if __name__ == "__main__":
    main()
