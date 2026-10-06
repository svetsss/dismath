# Запускает все задания лабораторной работы №2.

from task1_words import main as run_task1
from task2_recurrence import main as run_task2
from task3_fibonacci import main as run_task3
from task4_binomial import main as run_task4
from task5_paths import main as run_task5


def main() -> None:
    run_task1()
    run_task2()
    run_task3()
    run_task4()
    run_task5()


if __name__ == "__main__":
    main()
