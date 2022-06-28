"""
The code in this class is adapted from: https://github.com/AndreasSoularidis/medium_articles/tree/main/UCSAlgorithm
"""

# packages
from src.model.search_alg.Node import Node


class Graph:
    """
        This class used to represent the graph data structure.
    """

    def __init__(self, nodes: list[Node] = None):
        self.start = None
        self.target = None
        self.opened = []
        self.closed = []

        self.number_of_steps = 0
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes

    def setup(self, start: str, target: str):
        self.start = self.find_node(start)
        self.target = self.find_node(target)
        self.number_of_steps = 0
        self.opened = []
        self.closed = []
        for node in self.nodes:
            node.reset()

    def add_node(self, node: Node):
        """
            Add a new node (vertex) in the graph
        """
        self.nodes.append(node)

    def find_node(self, node_name: str):
        """
            Return True if the node with the given value exist in the graph. Otherwise, it returns False
        """
        for node in self.nodes:
            if node.name == node_name:
                return node
        return None

    def add_edge(self, value1: str, value2: str, weight: int = 1):
        """
            Add a new edge between the two given nodes
            Parameters
            ----------
                value1: str
                    The value of the first node
                value2: str
                    The value of the second node
                weight:
                    The weight of the edge. Default value 1
            ...
            Return
            ------
                Node
        """
        node1 = self.find_node(value1)
        node2 = self.find_node(value2)

        if (node1 is not None) and (node2 is not None):
            node1.add_neighbor((node2, weight))
            node2.add_neighbor((node1, weight))
        else:
            print("Error: One or more nodes were not found")

    def print_number_of_nodes(self) -> str:
        """
            Return the number of nodes of the graph
        """
        return f"The graph has {len(self.nodes)} nodes"

    def are_connected(self, node_one: str, node_two: str) -> bool:
        """
            Return True if the given nodes are connected. Otherwise, return False
        """
        node_one = self.find_node(node_one)
        node_two = self.find_node(node_two)

        for neighbor in node_one.neighbors:
            if neighbor[0].name == node_two.name:
                return True
        return False

    def calculate_distance(self, parent: Node, child: Node) -> int:
        """
          Calculate and return the distance from the start to child node. If the heuristic value has already calculated
          and is smaller than the new value, the method return the old value. Otherwise, the method return the new value
          and note the parent as the parent node of child
        """
        for neighbor in parent.neighbors:
            if neighbor[0] == child:
                distance = parent.heuristic_value + neighbor[1]
                if distance < child.heuristic_value:
                    child.parent = parent
                    return distance

                return child.heuristic_value

    def insert_to_list(self, list_category: str, node: Node):
        """
          Insert a node in the proper list (opened or closed) according to list_category
        """
        if list_category == "open":
            self.opened.append(node)
        else:
            self.closed.append(node)

    def remove_from_opened(self) -> Node:
        """
          Remove the node with the smallest heuristic value from the opened list
          Then add the removed node to the closed list
        """
        self.opened.sort()
        node = self.opened.pop(0)
        self.closed.append(node)
        return node

    def opened_is_empty(self) -> bool:
        """
          Check if the list opened is empty, so no solution found
        """
        return len(self.opened) == 0

    def get_old_node(self, node_value: str):
        """
          Return the node with the given value from the opened list,
          to compare its heuristic_value with a node with the same value
        """
        for node in self.opened:
            if node.name == node_value:
                return node
        return None

    def calculate_path(self, target_node: Node) -> list[str]:
        """
          Calculate and return the path (solution) of the problem
        """

        path = [target_node.name]
        node = target_node.parent
        while True:
            if node is None:
                print(f"path = {path}")
                print(f"node = {node}")
                print(f"start = {self.start}, target = {self.target}")
            path.append(node.name)
            if node.parent is None:
                break
            node = node.parent
        path.reverse()
        return path

    def search(self):
        """
          Is the main algorithm. Search for a solution in the solution space of the problem
          Stops if the opened list is empty, so no solution found or if it finds a solution.
        """
        # The heuristic value of the starting node is zero
        self.start.heuristic_value = 0
        # Add the starting point to opened list
        self.opened.append(self.start)

        while True:
            self.number_of_steps += 1

            if self.opened_is_empty():
                print(f"No Solution Found after {self.number_of_steps} steps for {self.start} to {self.target}!!!")
                return None

            selected_node = self.remove_from_opened()
            # check if the selected_node is the solution
            if selected_node == self.target:
                path = self.calculate_path(selected_node)
                return path, self.number_of_steps

            # extend the node
            new_nodes = selected_node.extend_node()

            # add the extended nodes in the list opened
            if len(new_nodes) > 0:
                for new_node in new_nodes:
                    new_node.heuristic_value = self.calculate_distance(selected_node, new_node)
                    if new_node not in self.closed and new_node not in self.opened:
                        self.insert_to_list("open", new_node)
                    elif new_node in self.opened and new_node.parent != selected_node:
                        old_node = self.get_old_node(new_node.name)
                        if new_node.heuristic_value < old_node.heuristic_value:
                            new_node.parent = selected_node
                            self.insert_to_list("open", new_node)

    def get_shortest_route(self) -> list[str]:
        """
            Return the shortest route as a list of node names
        """
        # call self.search and return route in correct form
        return_val = self.search()
        if return_val is None:
            return []
        else:
            path, path_length = return_val
        list_of_cities = self.calculate_path(self.target)
        return list_of_cities

    def __str__(self):
        """
            Define the way the nodes of graph will be printed.
        """
        graph = ""
        for node in self.nodes:
            graph += f"{node.__str__()}\n"
        return graph
