# Программа Б: наибольшее паросочетание методом Форда–Фалкерсона.

from collections import deque

from task_a_bipartite import prepare_bipartite_graph


# находит паросочетание сведением задачи к максимальному потоку
def ford_fulkerson_matching(
    left: set,
    right: set,
    edges: list,
) -> tuple:
    source, sink = 0, 1
    capacities = {}
    neighbors = {}

    def add_arc(start: int, end: int, capacity: int) -> None:
        capacities[start, end] = capacity
        capacities[end, start] = 0
        neighbors.setdefault(start, []).append(end)
        neighbors.setdefault(end, []).append(start)

    for vertex in sorted(left):
        add_arc(source, vertex, 1)

    for first, second in edges:
        if first in right:
            first, second = second, first
        add_arc(first, second, 1)

    for vertex in sorted(right):
        add_arc(vertex, sink, 1)

    residual = dict(capacities)
    augmentations = 0

    while True:
        parent = {source: None}
        queue = deque([source])

        while queue and sink not in parent:
            vertex = queue.popleft()

            for neighbor in neighbors[vertex]:
                has_capacity = residual[vertex, neighbor] > 0
                if neighbor not in parent and has_capacity:
                    parent[neighbor] = vertex
                    queue.append(neighbor)

        if sink not in parent:
            break

        current = sink
        while parent[current] is not None:
            previous = parent[current]
            residual[previous, current] -= 1
            residual[current, previous] += 1
            current = previous

        augmentations += 1

    matching = []
    for first, second in edges:
        if first in right:
            first, second = second, first
        if residual[first, second] == 0:
            matching.append((first, second))

    return sorted(matching), augmentations


def main() -> None:
    _, left, right, edges, _ = prepare_bipartite_graph()
    matching, augmentations = ford_fulkerson_matching(left, right, edges)

    assert len({vertex for edge in matching for vertex in edge}) == 2 * len(matching)
    print("\nБ. Алгоритм Форда–Фалкерсона:")
    print(f"Паросочетание: {matching}")
    print(f"Мощность: {len(matching)}")
    print(f"Увеличивающих цепей: {augmentations}")


if __name__ == "__main__":
    main()
