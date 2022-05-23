"""
This module provides with classes for Dijkstra's algorithm
Classes:
    - Node: node class with connections to other nodes.
    - DijkstraGraphSolver: solver class to solve graph with Dijkstra's algorithm
"""

class Node:
    # pylint: disable=R0903
    """Graph node for Dijkstra's algorithm."""
    def __init__(self):
        self.neighbors: dict[Node, int] = {}  # Node: value_to_reach
        self.value_to_reach: int = None
        self.reset()
        self.previous = None

    def reset(self):
        """Reset value to reach to initial."""
        self.value_to_reach: int = float('inf')
        self.previous = None

    def connect(self, other: 'Node', value: int):
        """
        Connect two nodes with way cost.

        Args:
            other (Node): other Node to connect to.
            value (int): cost to travel between nodes.
        """
        self.neighbors[other] = value
        other.neighbors[self] = value



class DijkstraGraphSolver:
    """
    Solve graph shortest path from first to last node using Dijkstra's algorithm.
    """
    def __init__(self, first: Node, last: Node):
        self.first = first
        self.last = last

    def solve(self, *, _first=None) -> True:
        """
        Solve lowest path for each of neighbour nodes.

        Returns:
            True
        """
        first = _first or self.first
        for node, value in first.neighbors.items():
            if (total := first.value_to_reach + value) < node.value_to_reach:
                node.value_to_reach = total
                node.previous = first
                self.solve(_first=node)
        return True

    def get_path(self) -> list[Node]:
        """
        Get path of the lowest cost from first to last node.
        If two path are equal cost, random is picked.

        Returns:
            list[Node]
        """
        self.first.value_to_reach = 0
        self.solve()
        path = []
        last = self.last
        while last is not None:
            path.append(last)
            last = last.previous
        return path[::-1]

    @staticmethod
    def reset(nodes: list[Node]):
        """
        Reset each node `value_to_reach` to float('inf').
        """
        for node in nodes:
            node.reset()
