from collections import defaultdict
from typing import Any, Optional

import networkx as nx
from utils import is_end_node, is_same_edge, is_switch
from yaramo.edge import Edge
from yaramo.geo_node import EuclideanGeoNode
from yaramo.node import Node
from yaramo.topology import Topology


class NetworkxImporter:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.topology = Topology()
        self.top_nodes: list[tuple[int, int]] = list(
            filter(lambda node: is_end_node(graph, node) or is_switch(graph, node), graph.nodes)
        )
        self.paths: dict[tuple[Optional[Any], Optional[Any]], list[list]] = defaultdict(list)

    def _get_next_top_node(self, node, edge, path):
        node_to = edge[1]
        if node_to in self.top_nodes:
            return node_to, path

        path.append(node_to)

        if self.graph.degree[node_to] == 0:  # type: ignore
            return None, path

        distinct_edges = [e for e in self.graph.edges(node_to) if not is_same_edge(e, edge)]
        if len(distinct_edges) != 1:
            raise Exception(f"Could not determine next edge to follow for node {node_to}.")

        return self._get_next_top_node(node_to, distinct_edges[0], path)

    def _add_geo_nodes(self, path, top_edge: Edge):
        for idx, node in enumerate(path):
            if idx == 0:
                continue
            x, y = node
            top_edge.intermediate_geo_nodes.append(EuclideanGeoNode(x, y))

    def _should_add_edge(self, node_a: Node, node_b: Node, path: list[int]):
        edge_not_present = not self.topology.get_edge_by_nodes(node_a, node_b)
        if edge_not_present:
            return True
        reversed_path = list(reversed(path))
        present_paths = self.paths[(node_a, node_b)] + self.paths[(node_b, node_a)]
        return path not in present_paths and reversed_path not in present_paths

    # TODO do GeoNodes need to be in DBRef?
    # TODO add signals etc.
    def run(self) -> Topology:
        for node in self.top_nodes:
            x, y = node
            top_node = Node(name=str(node))
            top_node.geo_node = EuclideanGeoNode(x, y)
            self.topology.add_node(top_node)

        for node in self.top_nodes:
            for edge in self.graph.edges(node):
                next_top_node, path = self._get_next_top_node(node, edge, [])
                if next_top_node and next_top_node != node:
                    node_a = next(
                        (n for n in self.topology.nodes.values() if n.name == str(node)),
                        None,
                    )
                    node_b = next(
                        (n for n in self.topology.nodes.values() if n.name == str(next_top_node)),
                        None,
                    )
                    if node_a and node_b and self._should_add_edge(node_a, node_b, path):
                        self.paths[(node_a, node_b)].append(path)
                        current_edge = Edge(node_a, node_b)
                        node_a.connected_nodes.append(node_b)
                        node_b.connected_nodes.append(node_a)
                        self.topology.add_edge(current_edge)
                        self._add_geo_nodes(path, current_edge)
                        current_edge.update_length()
        return self.topology
