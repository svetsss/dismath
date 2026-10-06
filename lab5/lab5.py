# Запускает все задания лабораторной работы №5.

from task1_matrix import main as run_task1
from task2_capabilities import main as run_task2
from task3_examples import main as run_task3
from task4_error_vector import main as run_task4


def main() -> None:
    run_task1()
    run_task2()
    run_task3()
    run_task4()


if __name__ == "__main__":
    main()
