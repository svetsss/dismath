# Лабораторная работа №8, вариант 14: максимальный поток.

from collections import deque
from pathlib import Path
from random import Random


EDGES = [
    ("S", "p", 7),
    ("S", "d", 61),
    ("S", "a", 31),
    ("p", "k", 21),
    ("p", "b", 13),
    ("a", "d", 12),
    ("a", "k", 11),
    ("a", "b", 6),
    ("d", "k", 12),
    ("d", "c", 7),
    ("k", "T", 6),
    ("c", "T", 71),
    ("c", "b", 11),
    ("b", "T", 5),
]

# создаёт остаточную сеть и нулевой начальный поток
def build_residual_network(edge_list: list) -> tuple:
    capacity = {(u, v): value for u, v, value in edge_list}
    residual = {}
    adjacency = {}
    flow = {(u, v): 0 for u, v in capacity}

    for u, v, value in edge_list:
        adjacency.setdefault(u, []).append(v)
        adjacency.setdefault(v, []).append(u)
        residual[u, v] = value
        residual[v, u] = 0

    return capacity, residual, adjacency, flow


# ищет увеличивающую цепь поиском в ширину
def find_augmenting_path(
    adjacency: dict,
    residual: dict,
    source: str,
    sink: str,
) -> list:
    parent = {source: None}
    queue = deque([source])

    while queue and sink not in parent:
        current = queue.popleft()

        for neighbor in adjacency[current]:
            has_capacity = residual[current, neighbor] > 0
            if neighbor not in parent and has_capacity:
                parent[neighbor] = current
                queue.append(neighbor)

    if sink not in parent:
        return []

    path = []
    current = sink
    while parent[current] is not None:
        previous = parent[current]
        path.append((previous, current))
        current = previous

    path.reverse()
    return path


# находит вершины, достижимые из истока в остаточной сети
def reachable_vertices(
    adjacency: dict,
    residual: dict,
    source: str,
) -> set:
    reachable = {source}
    queue = deque([source])

    while queue:
        current = queue.popleft()

        for neighbor in adjacency[current]:
            has_capacity = residual[current, neighbor] > 0
            if neighbor not in reachable and has_capacity:
                reachable.add(neighbor)
                queue.append(neighbor)

    return reachable


# находит максимальный поток методом Форда-Фалкерсона
def ford_fulkerson(
    edge_list: list,
    source: str = "S",
    sink: str = "T",
) -> tuple:
    capacity, residual, adjacency, flow = build_residual_network(edge_list)

    steps = []
    total_flow = 0

    while True:
        path = find_augmenting_path(adjacency, residual, source, sink)
        if not path:
            break

        increment = min(residual[edge] for edge in path)

        for u, v in path:
            residual[u, v] -= increment
            residual[v, u] += increment

            if (u, v) in flow:
                flow[u, v] += increment
            else:
                flow[v, u] -= increment

        total_flow += increment
        path_vertices = [source] + [v for _, v in path]
        steps.append((path_vertices, increment, total_flow))

    source_side = reachable_vertices(adjacency, residual, source)
    sink_side = set(adjacency) - source_side
    cut_edges = [
        (u, v, capacity[u, v])
        for u, v in capacity
        if u in source_side and v in sink_side
    ]

    cut_capacity = sum(value for _, _, value in cut_edges)
    assert cut_capacity == total_flow

    return total_flow, flow, steps, source_side, sink_side, cut_edges


def main() -> None:
    from lab8_visualization import draw_network

    output_dir = Path(__file__).parent
    (
        original_max_flow,
        original_flow,
        _,
        original_source_side,
        _,
        original_cut,
    ) = ford_fulkerson(EDGES)
    randomizer = Random(14)
    random_edges = [
        (u, v, randomizer.randint(100, 1000))
        for u, v, _ in EDGES
    ]
    (
        random_max_flow,
        random_flow,
        _,
        random_source_side,
        _,
        random_cut,
    ) = ford_fulkerson(random_edges)

    draw_network(EDGES, output_dir / "network_initial.png", "Исходная сеть")
    draw_network(
        EDGES,
        output_dir / "network_result.png",
        f"Максимальный поток = {original_max_flow}",
        original_flow,
        original_source_side,
        original_cut,
    )
    draw_network(
        random_edges,
        output_dir / "network_random_result.png",
        f"Случайные ёмкости: максимальный поток = {random_max_flow}",
        random_flow,
        random_source_side,
        random_cut,
    )

    print(f"Максимальный поток исходной сети: {original_max_flow}")
    print(f"Минимальный разрез исходной сети: {original_cut}")
    print(f"Максимальный поток случайной сети: {random_max_flow}")
    print(f"Минимальный разрез случайной сети: {random_cut}")


if __name__ == "__main__":
    main()
