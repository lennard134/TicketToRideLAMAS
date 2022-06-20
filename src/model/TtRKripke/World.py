class World(object):

    def __init__(self, state: dict[int]):
        """
        Initializer for a world that holds a dictionary of states
        :param state: State is dictionary with set of route names for each agent
        """
        self.state = state

    def check_truth(self, agent_id: int, route_card_name: str):
        """
        Function checks if some route card is owned by some agent
        :param agent_id: Id of agent for which we need to check if it owns certain card
        :param route_card_name: Route card for which we have to check if it is owned by some agent
        :return: True if route card id owned by agent, False otherwise
        """
        return route_card_name in self.state[agent_id]

    def get_state(self, agent_id):
        return self.state[agent_id]

    def get_name(self):
        """
        Initializes name of world as string representation
        :return: Returns name of the world
        """
        agent_ids = [agent_id for agent_id in self.state.keys()]
        agent_ids.sort()
        name = f"[({','.join(self.state[agent_ids.pop(0)])})"
        for agent_id in agent_ids:
            name += f",({','.join(self.state[agent_id])})"
        return name + "]"

    def __str__(self):
        return f"{self.get_name()}"


if __name__ == "__main__":
    wrld = World({0: {"a-b", "b-c"}, 1: {"c-d", "d-e"}})
    print(wrld)
