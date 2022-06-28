from __future__ import annotations

"""
The code in this class is adapted from: https://github.com/AndreasSoularidis/medium_articles/tree/main/UCSAlgorithm
"""

# packages
from cmath import inf


class Node(object):
    """
        This class is used to represent each Vertex in the graph
    """

    def __init__(self, name: str, neighbors: list = None):
        self.name = name
        self.heuristic_value = inf
        if neighbors is None:
            self.neighbors = []
        else:
            self.neighbors = neighbors
        self.parent = None

    def reset(self):
        self.heuristic_value = inf
        self.parent = None
        self.neighbors = []

    def has_neighbors(self) -> bool:
        """
            Return True if the current node is connected with at least another node.
            Otherwise, return false
        """
        return len(self.neighbors) != 0

    def number_of_neighbors(self) -> int:
        """
            Return the number of nodes with which the current node is connected
        """
        return len(self.neighbors)

    def add_neighbor(self, neighbor: tuple[Node, int]):
        """
            Add a new node to the neighbor list. In other words create a new connection between the
            current node and the neighbor
        """
        self.neighbors.append(neighbor)

    def extend_node(self) -> list[Node]:
        """
            Extends the current node, creating and returning a list with all connected nodes
        """
        children = []
        for child in self.neighbors:
            children.append(child[0])
        return children

    def __gt__(self, other: Node) -> bool:
        """
            Define which node, between current node and other node, has the greater value.
            First examine the heuristic value. If this value is the same for both nodes
            the function checks the lexicographic series
        """
        if isinstance(other, Node):
            if self.heuristic_value > other.heuristic_value:
                return True
            if self.heuristic_value < other.heuristic_value:
                return False
            return self.name > other.name

    def __eq__(self, other: Node) -> bool:
        """
            Define if current node and other node are equal, checking their values.
        """
        if isinstance(other, Node):
            return self.name == other.name
        return self.name == other

    def __str__(self) -> str:
        """
            Define that a node is printed with its value.
        """
        return self.name
