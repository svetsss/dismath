# Лабораторная работа №6, вариант 14: введение в теорию графов.

from itertools import combinations
from pathlib import Path
from typing import Optional


G1_EDGES = [
    (0, 1), (0, 3), (1, 2), (1, 5), (1, 7), (1, 8),
    (2, 3), (2, 7), (2, 8), (2, 9), (3, 4), (3, 5),
    (3, 6), (3, 9), (4, 5), (4, 6), (4, 8), (5, 6),
    (5, 9), (6, 7), (6, 8), (7, 8), (7, 9), (8, 9),
]

G2_EDGES = [
    (0, 2), (0, 3), (0, 5), (0, 7), (0, 8), (0, 9),
    (1, 4), (1, 7), (2, 4), (2, 6), (2, 8), (3, 4),
    (3, 5), (3, 7), (3, 9), (4, 5), (4, 6), (4, 8),
    (5, 6), (5, 9), (6, 7), (6, 8), (7, 9), (8, 9),
]


# приводит каждое ребро неориентированного графа к единому виду
def normalized_edges(edges: list) -> set:
    return {tuple(sorted(edge)) for edge in edges}


# строит список смежности
def adjacency(vertices: list, edges: list) -> dict:
    result = {vertex: set() for vertex in vertices}
    for left, right in edges:
        result[left].add(right)
        result[right].add(left)
    return result


# строит матрицу смежности
def adjacency_matrix(vertices: list, edges: list) -> list:
    edge_set = normalized_edges(edges)
    matrix = []
    for left in vertices:
        row = [
            int(tuple(sorted((left, right))) in edge_set)
            for right in vertices
        ]
        matrix.append(row)
    return matrix


# строит матрицу инцидентности
def incidence_matrix(vertices: list, edges: list) -> list:
    return [[int(vertex in edge) for edge in edges] for vertex in vertices]


# проверяет новую пару на согласованность с уже найденными
def mapping_is_consistent(
    vertex: int,
    candidate: int,
    mapping: dict,
    first_adjacency: dict,
    second_adjacency: dict,
) -> bool:
    return all(
        (mapped_vertex in first_adjacency[vertex])
        == (mapped_candidate in second_adjacency[candidate])
        for mapped_vertex, mapped_candidate in mapping.items()
    )


# рекурсивно дополняет частичное соответствие вершин
def extend_isomorphism(
    index: int,
    search_order: list,
    candidates: dict,
    first_adjacency: dict,
    second_adjacency: dict,
    mapping: dict,
    used_vertices: set,
    checked_mappings: list,
) -> Optional[dict]:
    if index == len(search_order):
        checked_mappings[0] += 1
        return dict(mapping)

    vertex = search_order[index]
    for candidate in candidates[vertex]:
        if candidate in used_vertices:
            continue
        if not mapping_is_consistent(
            vertex,
            candidate,
            mapping,
            first_adjacency,
            second_adjacency,
        ):
            continue

        mapping[vertex] = candidate
        used_vertices.add(candidate)
        result = extend_isomorphism(
            index + 1,
            search_order,
            candidates,
            first_adjacency,
            second_adjacency,
            mapping,
            used_vertices,
            checked_mappings,
        )
        if result is not None:
            return result

        used_vertices.remove(candidate)
        del mapping[vertex]

    return None


# ищет изоморфизм перебором допустимых соответствий вершин
def find_isomorphism(
    vertices: list,
    edges1: list,
    edges2: list,
) -> tuple:
    first_adjacency = adjacency(vertices, edges1)
    second_adjacency = adjacency(vertices, edges2)

    first_degrees = sorted(map(len, first_adjacency.values()))
    second_degrees = sorted(map(len, second_adjacency.values()))
    if first_degrees != second_degrees:
        return None, 0

    search_order = sorted(
        vertices,
        key=lambda vertex: (-len(first_adjacency[vertex]), vertex),
    )
    candidates = {
        vertex: [
            candidate
            for candidate in vertices
            if len(first_adjacency[vertex]) == len(second_adjacency[candidate])
        ]
        for vertex in vertices
    }
    checked_mappings = [0]
    result = extend_isomorphism(
        0,
        search_order,
        candidates,
        first_adjacency,
        second_adjacency,
        {},
        set(),
        checked_mappings,
    )
    return result, checked_mappings[0]


# строит дополнение графа
def complement_edges(vertices: list, edges: list) -> list:
    edge_set = normalized_edges(edges)
    return [edge for edge in combinations(vertices, 2) if edge not in edge_set]


# находит заданное количество гамильтоновых циклов
def find_hamiltonian_cycles(
    vertices: list,
    edges: list,
    limit: int = 2,
) -> list:
    adj = adjacency(vertices, edges)
    start = min(vertices)
    cycles = []

    def dfs(path: list, used: set) -> None:
        if len(cycles) >= limit:
            return
        current = path[-1]

        if len(path) == len(vertices):
            if start in adj[current] and path[1] < path[-1]:
                cycles.append(path + [start])
            return
        for neighbor in sorted(adj[current]):
            if neighbor in used:
                continue

            used.add(neighbor)
            path.append(neighbor)
            dfs(path, used)
            path.pop()
            used.remove(neighbor)

    dfs([start], {start})
    return cycles


# находит все полные подграфы на четырёх вершинах
def find_k4(vertices: list, edges: list) -> list:
    edge_set = normalized_edges(edges)
    return [
        group
        for group in combinations(vertices, 4)
        if all(tuple(sorted(edge)) in edge_set for edge in combinations(group, 2))
    ]


# строит рёберный граф: его вершины соответствуют рёбрам исходного графа
def line_graph(edges: list) -> tuple:
    labels = list(range(1, len(edges) + 1))
    line_edges = []

    for first, second in combinations(range(len(edges)), 2):
        if set(edges[first]) & set(edges[second]):
            line_edges.append((first + 1, second + 1))

    return labels, line_edges


def main() -> None:
    from lab6_visualization import draw_graph

    output_dir = Path(__file__).parent
    vertices = list(range(10))
    adjacency_list = adjacency(vertices, G1_EDGES)
    matrix = adjacency_matrix(vertices, G1_EDGES)
    incidence = incidence_matrix(vertices, G1_EDGES)
    degrees = [len(adjacency_list[vertex]) for vertex in vertices]
    mapping, _ = find_isomorphism(vertices, G1_EDGES, G2_EDGES)
    complement = complement_edges(vertices, G1_EDGES)
    cycles = find_hamiltonian_cycles(vertices, G1_EDGES, 2)
    k4_groups = find_k4(vertices, G1_EDGES)

    assert mapping is not None
    mapped_edges = {tuple(sorted((mapping[a], mapping[b]))) for a, b in G1_EDGES}
    assert mapped_edges == normalized_edges(G2_EDGES)
    assert all(sum(row) == degrees[index] for index, row in enumerate(matrix))
    assert all(len(row) == len(G1_EDGES) for row in incidence)
    complete_graph_size = len(vertices) * (len(vertices) - 1) // 2
    assert len(complement) == complete_graph_size - len(G1_EDGES)
    assert len(cycles) == 2

    highlighted_cycle = list(zip(cycles[0], cycles[0][1:]))
    draw_graph(
        vertices,
        G1_EDGES,
        output_dir / "graph_g1.png",
        "Граф G1",
        highlighted=highlighted_cycle,
    )
    draw_graph(
        vertices,
        complement,
        output_dir / "graph_complement.png",
        "Дополнение графа G1",
    )

    line_labels, line_edges = line_graph(G1_EDGES)
    draw_graph(
        line_labels,
        line_edges,
        output_dir / "graph_line.png",
        "Рёберный граф L(G1)",
        label_prefix="e",
    )

    print(f"Степени вершин: {degrees}")
    print(f"Изоморфизм G1 → G2: {mapping}")
    print(f"Рёбер в дополнении: {len(complement)}")
    print(f"Гамильтоновы циклы: {cycles}")
    print(f"Подграфы K4: {k4_groups}")
    print(f"Рёберный граф: {len(line_labels)} вершины, {len(line_edges)} рёбер")


if __name__ == "__main__":
    main()
