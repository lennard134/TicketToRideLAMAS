# """
# UCS
# """
# # settings
# EPSILON = 1e-7
#
#
# class UCS(object):
#     """
#           This class used to represent the Greedy algorithm
#           ...
#           Attributes
#           ----------
#           graph : Graph
#             Represent the graph (search space of the problem)
#           start : str
#             Represent the starting point
#           target : str
#             Represent the destination (target) node
#           opened : list
#             Represent the list with the available nodes in the search process
#           closed : list
#             Represent the list with the closed (visited) nodes
#           number_of_steps : int
#             Keep the number of steps of the algorithm
#           ...
#           Methods
#           -------
#           calculate_distance(self, parent, child) -> int
#             Calculate the distance from the starting node to the child node
#           insert_to_list(self, list_category, node) -> None
#             Insert a new node either ot opened or to closed list according to list_category parameter
#           remove_from_opened(self) -> Node
#             Remove from the opened list the node with the smallest heuristic value
#           opened_is_empty(self) -> Boolean
#             Check if the opened list is empty or not
#           get_old_node(self, node_value) -> Node
#             Return the node from the opened list in case of a new node with the same value
#           calculate_path(self, target_node) -> list
#             Calculate and return the path from the stat node to target node
#           search(self)
#               Implements the core of algorithm. This method searches, in the search space of the problem, a solution
#           """
#     def __init__(self):
#
#     # def setup(self, start, target):
#     #     self.start = start
#     #     self.target = target
#     #     self.opened = []
#     #     self.closed = []
#
#
