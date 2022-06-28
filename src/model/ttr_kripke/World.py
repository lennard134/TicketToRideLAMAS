"""
World object that stores the states
"""


class World(object):

    def __init__(self, state: dict[int], agent_list: list[int]):
        """
        Initializer for a world that holds a dictionary of states
        :param state: State is dictionary with set of route names for each agent
        :param agent_list: List of agent_ids of agents that are allowed to consider said state given their knowledge
        """
        self.state = state
        self._agent_list = agent_list

    def check_truth(self, agent_id: int, route_card_name: str):
        """
        Function checks if some route card is owned by some agent
        :param agent_id: Id of agent for which we need to check if it owns certain card
        :param route_card_name: Route card for which we have to check if it is owned by some agent
        :return: True if route card id owned by agent, False otherwise
        """
        return route_card_name in self.state[agent_id]

    def get_state(self, agent_id) -> set:
        return self.state[agent_id]

    def get_name(self) -> str:
        agent_ids = [agent_id for agent_id in self.state.keys()]
        agent_ids.sort()
        name = f"[({','.join(self.state[agent_ids.pop(0)])})"
        for agent_id in agent_ids:
            name += f",({','.join(self.state[agent_id])})"
        return name + "]"

    def has_agent_in_agent_list(self, agent_asking: int, agent_targeting: int) -> bool:
        """
        Returns true if the provided agent_id is in the agent list
        """
        assert agent_asking == agent_targeting, f"Agent {agent_asking} may not ask about {agent_targeting}."
        return agent_targeting in self._agent_list

    def remove_agent_from_list(self, agent_id: int):
        """
        Removes provided agent_id from the agent list
        """
        self._agent_list.remove(agent_id)

    def __str__(self):
        return f"{self.get_name()}"
