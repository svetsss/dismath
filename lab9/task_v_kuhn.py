# Программа В: наибольшее паросочетание алгоритмом Куна.

from pathlib import Path

from task_a_bipartite import prepare_bipartite_graph


# находит паросочетание алгоритмом увеличивающих цепей Куна
def kuhn_matching(
    left: set,
    right: set,
    edges: list,
) -> tuple:
    adjacency_list = {vertex: [] for vertex in left}

    for first, second in edges:
        if first in right:
            first, second = second, first
        adjacency_list[first].append(second)

    for vertex in left:
        adjacency_list[vertex].sort()

    left_match = {}
    edge_checks = 0

    def augment(vertex: int, visited: set) -> bool:
        nonlocal edge_checks

        for neighbor in adjacency_list[vertex]:
            edge_checks += 1
            if neighbor in visited:
                continue

            visited.add(neighbor)
            if neighbor not in left_match or augment(left_match[neighbor], visited):
                left_match[neighbor] = vertex
                return True

        return False

    augmentations = 0
    for vertex in sorted(left):
        if augment(vertex, set()):
            augmentations += 1

    matching = sorted(
        (left_vertex, right_vertex)
        for right_vertex, left_vertex in left_match.items()
    )
    return matching, augmentations, edge_checks


def main() -> None:
    from lab9_visualization import draw_matching

    _, left, right, edges, removed = prepare_bipartite_graph()
    matching, augmentations, edge_checks = kuhn_matching(left, right, edges)

    assert len({vertex for edge in matching for vertex in edge}) == 2 * len(matching)
    draw_matching(
        left,
        right,
        edges,
        removed,
        matching,
        Path(__file__).parent / "matching.png",
    )

    print("\nВ. Алгоритм Куна:")
    print(f"Паросочетание: {matching}")
    print(f"Мощность: {len(matching)}")
    print(f"Увеличивающих цепей: {augmentations}")
    print(f"Проверок рёбер: {edge_checks}")


if __name__ == "__main__":
    main()
