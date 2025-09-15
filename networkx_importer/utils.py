import networkx as nx


def is_switch(graph: nx.Graph, node) -> bool:
    return graph.degree[node] == 3  # type: ignore


def is_end_node(graph: nx.Graph, node) -> bool:
    return graph.degree[node] == 1  # type: ignore


def is_same_edge(e1: tuple, e2: tuple) -> bool:
    if e1 == e2:
        return True
    if e1[0] == e2[1] and e1[1] == e2[0]:
        return True
    return False
