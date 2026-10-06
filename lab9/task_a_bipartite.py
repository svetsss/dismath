# Программа А: проверка двудольности и минимальное удаление рёбер.

from collections import deque


EDGES = [
    (3, 8), (3, 6), (4, 16), (14, 15), (12, 15), (2, 6), (4, 8),
    (3, 13), (2, 15), (10, 14), (5, 6), (5, 13), (10, 12),
    (6, 7), (5, 8), (2, 9), (5, 10), (4, 13), (6, 12), (8, 14),
    (8, 12), (5, 16), (7, 10), (11, 13), (6, 11), (9, 11),
    (2, 13), (7, 13), (7, 9), (2, 8), (6, 14), (9, 14), (3, 10),
    (11, 16), (10, 11),
]


# строит список смежности неориентированного графа
def adjacency(vertices: list, edges: list) -> dict:
    adjacency_list = {vertex: [] for vertex in vertices}

    for left, right in edges:
        adjacency_list[left].append(right)
        adjacency_list[right].append(left)

    return adjacency_list


# проверяет двудольность графа обходом в ширину
def bipartite_check(vertices: list, edges: list) -> tuple:
    adjacency_list = adjacency(vertices, edges)
    colors = {}

    for start in vertices:
        if start in colors:
            continue

        colors[start] = 0
        queue = deque([start])

        while queue:
            vertex = queue.popleft()

            for neighbor in adjacency_list[vertex]:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False, colors, (vertex, neighbor)

    return True, colors, None


# оставляет максимум рёбер между двумя долями
def minimum_edge_bipartization(vertices: list, edges: list) -> tuple:
    fixed_vertex = vertices[0]
    best_edge_count = -1
    best_colors = {}

    for mask in range(1 << (len(vertices) - 1)):
        colors = {fixed_vertex: 0}

        for index, vertex in enumerate(vertices[1:]):
            colors[vertex] = (mask >> index) & 1

        crossing_edges = sum(
            colors[left] != colors[right]
            for left, right in edges
        )
        if crossing_edges > best_edge_count:
            best_edge_count = crossing_edges
            best_colors = colors

    kept_edges = [
        edge for edge in edges
        if best_colors[edge[0]] != best_colors[edge[1]]
    ]
    removed_edges = [
        edge for edge in edges
        if best_colors[edge[0]] == best_colors[edge[1]]
    ]
    return best_colors, kept_edges, removed_edges


# подготавливает доли и рёбра для программ Б и В
def prepare_bipartite_graph() -> tuple:
    vertices = sorted({vertex for edge in EDGES for vertex in edge})
    is_bipartite, colors, _ = bipartite_check(vertices, EDGES)

    if is_bipartite:
        kept_edges = EDGES.copy()
        removed_edges = []
    else:
        colors, kept_edges, removed_edges = minimum_edge_bipartization(
            vertices,
            EDGES,
        )

    left = {vertex for vertex in vertices if colors[vertex] == 0}
    right = set(vertices) - left
    return is_bipartite, left, right, kept_edges, removed_edges


def main() -> None:
    is_bipartite, left, right, _, removed = prepare_bipartite_graph()

    print("А. Проверка двудольности:")
    print(f"Граф двудольный: {is_bipartite}")
    print(f"Левая доля: {sorted(left)}")
    print(f"Правая доля: {sorted(right)}")
    print(f"Удалённые рёбра: {removed}")


if __name__ == "__main__":
    main()
