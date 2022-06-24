# packages

import itertools

from src.model.TtRKripke.World import World


class TtRKripke(object):

    def __init__(self, agent_ids: list[int], route_cards_ids: list[str]):
        """
        Initialization of Kripke model
        :param agent_ids: List of all agent id's
        :param route_cards_ids: List of all route card id's
        """
        self.agent_ids = agent_ids
        self.route_cards_ids = route_cards_ids
        self.worlds = []
        self.relations = {}

        self._init_worlds()
        # print("worlds initialized")
        self._init_relations()
        # print("relations initialized")

    def _init_worlds(self):
        """
        Initialize worlds by creating possible combinations of route cards
        """
        m_route_cards = len(self.route_cards_ids)
        n_agents = len(self.agent_ids)
        num_cards_per_agent, rem = divmod(m_route_cards, n_agents)
        assert rem == 0, "Cards cannot be evenly distributed among agents. EXITING..."

        m_cards_combinations = list(itertools.combinations(self.route_cards_ids, num_cards_per_agent))
        n_agents_combinations = list(itertools.permutations(m_cards_combinations, n_agents))
        for world_i in n_agents_combinations:
            to_add = True
            set_cards = set(world_i[0])
            for idx in range(1, n_agents):
                new_set = set(world_i[idx])
                if set_cards.intersection(new_set):
                    to_add = False
                    break  # Do not add
                set_cards.update(new_set)

            if to_add:
                state = {}
                for idx, agent_id in enumerate(self.agent_ids):
                    state[agent_id] = set(world_i[idx])
                self.worlds.append(World(state, self.agent_ids.copy()))
        print(f"Number of worlds = {len(self.worlds)}")

    def _init_relations(self):
        """
        Initialize relations for all worlds before agents knows their own card
        """
        relation_list = []
        for relation in itertools.product(self.worlds, repeat=2):  # List of string tuples (world1,world2)
            relation_list.append(relation)
        for i in self.agent_ids:
            self.relations[i] = relation_list

    def update_once_cards_known(self, agent_id: int, route_cards: set[str]):
        """
        Update relations for agent_id that knows that target_agent has route_cards
        :param agent_id: Id of agent for which relations will be updated
        :param target_agent_id: id of target agent of which the agent knows
        :param route_cards: Route cards of which agent knows
        """
        print(f"----------------------------------------------------------------------------------\n"
              f"Agent {agent_id} knows that itself has cards {route_cards}\n"
              f"----------------------------------------------------------------------------------\n")
        update_dict = []
        print(f"Agent first has {len(self.relations[agent_id])} relations")
        for relation in self.relations[agent_id]:  # agent0: (e) [(e,f),(d,c),(a,b)], [(e,d),(d,c),(a,b)]
            # check if intersection is equal to route cards
            from_state = relation[0].get_state(agent_id)
            to_state = relation[1].get_state(agent_id)
            if not from_state.symmetric_difference(to_state):
                # true if internal states of agent_id is not equal
                update_dict.append(relation)
            # else:
            #     print(f"Removing relation: {relation[0]}, {relation[1]}")

        self.relations[agent_id] = update_dict
        print(f"Agent {agent_id} remains with {len(self.relations[agent_id])} relations")

        # agents no longer consider the worlds that violate their own relations
        total_removal = 0
        for world in self.worlds:
            if world.has_agent_in_agent_list(agent_id):
                target_set = world.get_state(agent_id)
                if route_cards.difference(target_set):
                    print(f"removing {agent_id} from world {str(world)}")
                    total_removal += 1
                    world.remove_agent_from_list(agent_id)

        for world in self.worlds:
            if world.has_agent_in_agent_list(agent_id):
                print(f"{agent_id} still in {str(world)}")
        print(f"TOTAL REMOVED = {total_removal}")

    def update_relations(self, agent_id: int, target_agent_id: int, route_cards: set[str]):
        """
        Update relations for agent_id that knows that target_agent has route_cards
        :param agent_id: Id of agent for which relations will be updated
        :param target_agent_id: id of target agent of which the agent knows
        :param route_cards: Route cards of which agent knows
        """
        print(f"\n----------------------------------------------------------------------------------\n"
              f"Agent {agent_id} knows that agent {target_agent_id} has cards {route_cards}\n"
              f"----------------------------------------------------------------------------------\n")
        update_dict = []
        print(f"Agent first has {len(self.relations[agent_id])} relations")
        for relation in self.relations[agent_id]:  # agent0: (e) [(e,f),(d,c),(a,b)], [(e,d),(d,c),(a,b)]
            # check if intersection is equal to route cards
            from_state = relation[0].get_state(target_agent_id)
            to_state = relation[1].get_state(target_agent_id)
            # if (not route_cards.difference(from_state) and route_cards.difference(to_state)) or (
            #         route_cards.difference(from_state) and not route_cards.difference(to_state)):
            if (route_cards.difference(from_state) or not route_cards.difference(to_state)) and (
                    not route_cards.difference(from_state) or route_cards.difference(to_state)):
                # true if all route cards are in first world, but not in second
                # or if all route cards are in the second world, but not in the first (for symmetry)
                update_dict.append(relation)
            # else:
            #     print(f"Removing relation: {relation[0]}, {relation[1]}")

        self.relations[agent_id] = update_dict
        print(f"Agent {agent_id} remains with {len(self.relations[agent_id])} relations")

        # agents no longer consider the worlds that violate their own relations
        total_removal = 0
        for world in self.worlds:
            if world.has_agent_in_agent_list(agent_id):
                target_set = world.get_state(target_agent_id)
                if route_cards.difference(target_set):
                    print(f"removing {agent_id} from world {str(world)}")
                    total_removal += 1
                    world.remove_agent_from_list(agent_id)
        print(f"TOTAL REMOVED = {total_removal}")

    def public_announcement_route_card(self, agent_id: int, route_card: str):
        """
        Method to do a public announcement of a route card and remove worlds that are no longer possible
        :param agent_id: Agent that has route card
        :param route_card: Route card that is being announced
        """
        print(f"\n----------------------------------------------------------------------------------\n"
              f"Publicly known that agent {agent_id} has card {route_card}\n"
              f"----------------------------------------------------------------------------------\n")
        # remove relations
        card_set = {route_card}
        for agent in self.agent_ids:
            update_dict = []
            for relation in self.relations[agent]:
                from_state = relation[0].get_state(agent_id)
                to_state = relation[1].get_state(agent_id)
                if not card_set.difference(from_state) and not card_set.difference(to_state):
                    # true if card in both states
                    update_dict.append(relation)
                # else:
                #     print(f"Removing relation: {relation[0]}, {relation[1]}")

            self.relations[agent] = update_dict

        # remove worlds
        world_list = []
        for world in self.worlds:
            # print(f"card set = {card_set}")
            # print(f"get state = {world.get_state(agent_id)}")
            # print(f"difference = {card_set.difference(world.get_state(agent_id))}")
            if not card_set.difference(world.get_state(agent_id)):
                # true if card is in state for agent_id
                print(f"agent list of kept world {world._agent_list}")
                world_list.append(world)
            else:
                print(f"Removing world {str(world)}")

        self.worlds = world_list
        print(f"Number of worlds left = {len(self.worlds)}")
        print(f"Number of relations left for agent {agent_id} = {len(self.relations[agent_id])}")

    def print_world_agent_list(self):
        empty_worlds = 0
        for world in self.worlds:
            if world._agent_list:
                print(f"Agents considering world {str(world)} are {world._agent_list}")
            else:
                empty_worlds += 1
        print(f"total number of empty worlds = {empty_worlds}")

    def get_known_route_cards(self, agent_id: int, target_agent_id: int) -> list[str]:
        """
        Function to retrieve the cards that one agent knows another agent has.
        :param agent_id: Agent of which the worlds are considered
        :param target_agent_id: Agent Id of which the agent knows the cards
        :return: List containing knows cards in string representation
        """
        # return list of cards known by agent to be of target agent
        # this means if a card occurs in every world in the state of a single agent, then it is known
        world_counter = 0
        possible_target_cards = {}

        for world in self.worlds:
            if world.has_agent_in_agent_list(agent_id):
                world_counter += 1
                for route_card in world.get_state(target_agent_id):
                    if route_card in possible_target_cards.keys():
                        possible_target_cards[route_card] += 1
                    else:
                        possible_target_cards[route_card] = 1

        known_cards = []
        for route_card, card_count in possible_target_cards.items():
            if card_count == world_counter:
                known_cards.append(route_card)

        return known_cards

    def __str__(self):
        name = ""
        cnt = 0
        for agent_id in self.agent_ids:
            name += f"--{agent_id}:"
            for relation in self.relations[agent_id]:
                cnt += 1
                name += f"{str(relation[0])}-{str(relation[1])} || "
                if cnt == 10:
                    cnt = 0
                    break
            if agent_id != self.agent_ids[-1]:
                name += "\n"

        return name



