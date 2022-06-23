from __future__ import annotations

# packages
from cmath import inf


class Node(object):
    """
        This class used to represent each Vertex in the graph
        ...
        Attributes
        ----------
        name : str
            Represent the value of the node
        heuristic_value : int
            Corresponds to the distance from the start node to current node. Default value is inf (infinity)
        neighbors : list
            A list with the nodes the current node is connected
        parent : Node
            Represents the parent-node of the current node. Default value is None
        ...
        Methods
        -------
        has_neighbors(self) -> Boolean
            Check if the current node is connected with other nodes (return True). Otherwise return False
        number_of_neighbors(self) -> int
            Calculate and return the number the of the neighbors
        add_neighboor(self, neighboor) -> None
            Add a new neighbor in the list of neighbors
        extend_node(self) -> list
            return a list of nodes with which the current node is connected
        __eq__(self, other) -> Boolean
            Determines if two nodes are equal or not, checking their values
        __str__(self) -> str
            Prints the node data
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

    def has_neighbors(self):
        """
            Return True if the current node is connected with at least another node.
            Otherwise, return false
        """
        return len(self.neighbors) != 0

    def number_of_neighbors(self):
        """
            Return the number of nodes with which the current node is connected
        """
        return len(self.neighbors)

    def add_neighbor(self, neighbor: tuple[Node, int]):
        """
            Add a new node to the neighbor list. In other words create a new connection between the
            current node and the neighbor
            Paramenters
            ----------
            neighbor : node
                Represent the node with which a new connection is created
        """
        self.neighbors.append(neighbor)

    def extend_node(self):
        """
            Extends the current node, creating and returning a list with all connected nodes
            Returns
            -------
                List
        """
        children = []
        for child in self.neighbors:
            children.append(child[0])
        return children

    # def replace_neighbor_value(self, neighbor: tuple[Node, int]):
    #     new_neighbor_list = [item for item in self.neighbors if item[0].name != neighbor[0].name]
    #     new_neighbor_list.append(neighbor)
    #     self.neighbors = new_neighbor_list

    def __gt__(self, other: Node):
        """
            Define which node, between current node and other node, has the greater value.
            First examine the heuristic value. If this value is the same for both nodes
            the function checks the lexicographic series
            Parameters
            ----------
                other: Node:
                    Represent the other node with which the current node is compared
            Returns
            -------
                Boolean
        """
        if isinstance(other, Node):
            if self.heuristic_value > other.heuristic_value:
                return True
            if self.heuristic_value < other.heuristic_value:
                return False
            return self.name > other.name

    def __eq__(self, other: Node):
        """
            Define if current node and other node are equal, checking their values.
            Parameters
            ----------
                other: Node:
                    Represent the other node with which the current node is compared
            Returns
            -------
                Boolean
        """
        if isinstance(other, Node):
            return self.name == other.name
        return self.name == other

    def __str__(self):
        """
            Define that a node is printed with its value.
            Returns
            -------
                str
        """
        return self.name


class Graph:
    """
        This class used to represent the graph data structure.
        ...
        Attributes
        ----------
        nodes : list
            List with all the nodes of the graph
        ...
        Methods
        -------
        add_node(self, node) -> None
            Add a new node in the list of nodes
        find_node(self, value) -> Node
            Find and return the node of the graph with the given value.
        add_edge(self, value1, value2, weight=1) -> None
            Add a new edge in the graph
        number_of_nodes(self) -> int
            Calculate and return the number of nodes of the graph
        are_connected(self, node_one, node_two) -> Boolean
            Check if the two given nodes are connected each other
        __str__(self) -> str
            Prints the nodes of the graph
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
            Parameters
            ----------
                node: Node
                    Represent the inserted node in the graph
        """
        self.nodes.append(node)

    def find_node(self, node_name: str):
        """
            Return True if the node with the given value exist in the graph. Otherwise it return False
            Parameters
            ----------
                node_name: str
                    Is the value of the node we want to find
            ...
            Return
            ------
                Node
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

    def number_of_nodes(self):
        """
            Return the number of nodes of the graph
            ...
            Return
            ------
                int
        """
        return f"The graph has {len(self.nodes)} nodes"

    def are_connected(self, node_one: str, node_two: str) -> bool:
        """
            Return True if the given nodes are connected. Otherwise return False
            ...
            Parameters
            ----------
                node_one: str
                    The value of the first node
                node_two: str
                    The value of the second node
            Return
            ------
                Boolean
        """
        node_one = self.find_node(node_one)
        node_two = self.find_node(node_two)

        for neighbor in node_one.neighbors:
            if neighbor[0].name == node_two.name:
                return True
        return False

    def calculate_distance(self, parent: Node, child: Node):
        """
          Calculate and return the distance from the start to child node. If the heuristic value has already calculated
          and is smaller than the new value, the method return theold value. Otherwise the method return the new value
          and note the parent as the parent node of child
          Parameters
          ----------
          parent : Node
            Represent the parent node
          child : Node
            Represent the child node
          ...
          Return
          ------
            int
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
          Parameters
          ----------
          list_category : str
              Determines the list in which the node will be d. If the value is 'open'
              the node is appended in the opened list. Otherwise, the node is appended in the closed list
          node : Node
              The node of the problem that will be added to the frontier
        """
        if list_category == "open":
            self.opened.append(node)
        else:
            self.closed.append(node)

    def remove_from_opened(self) -> Node:
        """
          Remove the node with the smallest heuristic value from the opened list
          Then add the removed node to the closed list
          Returns
          -------
            Node
        """
        self.opened.sort()
        # for n in self.opened:
        #   print(f"({n},{n.heuristic_value})", end = " ")
        # print("\n")
        node = self.opened.pop(0)
        self.closed.append(node)
        return node

    def opened_is_empty(self) -> bool:
        """
          Check if the the list opened is empty, so no solution found
          Returns
          -------
          Boolean
            True if the list opened is empty
            False if the list opened is not empty
        """
        return len(self.opened) == 0

    def get_old_node(self, node_value: Node):
        """
          Return the node with the given value from the opened list,
          to compare its heuristic_value with a node with the same value
          ...
          Parameters
          ----------
            node_value : Node
            Represent the value of the node
          Returns
          -------
            Node
        """
        for node in self.opened:
            if node.name == node_value:
                return node
        return None

    def calculate_path(self, target_node: Node):
        """
          Calculate and return the path (solution) of the problem
          ...
          Parameters
          ----------
            target_node : Node
            Represent final (destination) node of the problem
          Returns
          -------
            list
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
          Stops if the opened list is empty, so no solution found or if it find a solution.
          ...
          Return
          ------
            list
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
            # print(f"Selected Node {selected_node}")
            # check if the selected_node is the solution
            if selected_node == self.target:
                path = self.calculate_path(selected_node)
                return path, self.number_of_steps

            # extend the node
            new_nodes = selected_node.extend_node()

            # add the extended nodes in the list opened
            # print(f"length of new nodes list: {len(new_nodes)}")
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
        # call self.search and return route in correct form
        return_val = self.search()
        if return_val is None:
            return []
        else:
            path, path_length = return_val
        print(" -> ".join(path))
        if path_length > 50:
            print(f"Length of the path: {path_length}")
        list_of_cities = self.calculate_path(self.target)
        return list_of_cities

    def __str__(self):
        """
            Define the way the nodes of graph will be printed.
            Return
            ------
                str
        """
        graph = ""
        for node in self.nodes:
            graph += f"{node.__str__()}\n"
        return graph
