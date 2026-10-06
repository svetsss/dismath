# Запускает три программы лабораторной работы №9.

from task_a_bipartite import main as run_task_a
from task_b_ford_fulkerson import main as run_task_b
from task_v_kuhn import main as run_task_v


def main() -> None:
    run_task_a()
    run_task_b()
    run_task_v()


if __name__ == "__main__":
    main()
