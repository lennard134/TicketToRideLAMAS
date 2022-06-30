# packages
import itertools

from ..ttr_kripke.World import World


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
        self._init_relations()

    def _init_worlds(self):
        """
        Initialize worlds by creating possible combinations of route cards
        """
        print("- Initializing worlds...", end=" -> ")
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
        print(f"Number of Kripke worlds = {len(self.worlds)}")

    def _init_relations(self):
        """
        Initialize relations for all worlds before agents knows their own card
        """
        print(f"- Initializing relations...", end=" -> ")
        relation_list = []
        for relation in itertools.product(self.worlds, repeat=2):
            relation_list.append(relation)
        for i in self.agent_ids:
            self.relations[i] = relation_list
        print(f"Number of relations per agent = {len(relation_list)}\n")

    def update_once_cards_known(self, agent_id: int, route_cards: set[str]):
        """
        Update relations for agent_id that knows that target_agent has route_cards
        :param agent_id: Id of agent for which relations will be updated
        :param route_cards: Route cards of which agent knows
        """
        print(f"--> Agent {agent_id} knows that itself has cards {route_cards}")

        update_dict = []
        for relation in self.relations[agent_id]:
            # check if intersection is equal to route cards
            from_state = relation[0].get_state(agent_id)
            to_state = relation[1].get_state(agent_id)
            if not from_state.symmetric_difference(to_state):
                # true if internal states of agent_id is not equal
                update_dict.append(relation)

        self.relations[agent_id] = update_dict

        # agents no longer consider the worlds that violate their own relations
        for world in self.worlds:
            if world.has_agent_in_agent_list(agent_id, agent_id):
                target_set = world.get_state(agent_id)
                if route_cards.difference(target_set):
                    world.remove_agent_from_list(agent_id)

        if len(self.agent_ids) == 2:
            # In case of two agents, all route cards are publicly known
            self.public_announcement_route_card(agent_id, route_cards)

    def update_relations(self, agent_id: int, target_agent_id: int, route_cards: set[str]):
        """
        Update relations for agent_id that knows that target_agent has route_cards
        :param agent_id: Id of agent for which relations will be updated
        :param target_agent_id: id of target agent of which the agent knows
        :param route_cards: Route cards of which agent knows
        """
        print(f"--> Agent {agent_id} knows that agent {target_agent_id} has cards {route_cards}")

        update_dict = []
        # Remove all relations from considered states by an agent where the above holds
        for relation in self.relations[agent_id]:
            if relation[0].has_agent_in_agent_list(agent_id, agent_id):
                # check if intersection is equal to route cards
                from_state = relation[0].get_state(target_agent_id)
                to_state = relation[1].get_state(target_agent_id)
                if (not route_cards.difference(from_state) and route_cards.difference(to_state)) or (
                        route_cards.difference(from_state) and not route_cards.difference(to_state)):
                    # removing relation if there is a difference between two states
                    continue
            update_dict.append(relation)

        self.relations[agent_id] = update_dict

        # agents no longer consider the worlds that violate their own relations
        total_removal = 0
        for world in self.worlds:
            if world.has_agent_in_agent_list(agent_id, agent_id):
                target_set = world.get_state(target_agent_id)
                if route_cards.difference(target_set):
                    total_removal += 1
                    world.remove_agent_from_list(agent_id)

    def update_possible_relations(self, agent_id: int, target_agent_id: int, route_cards: set[str]):
        """
        Function that updates relations, relations are either removed or nothing happens
        :param agent_id: Agent for which the relations are updated
        :param target_agent_id: Target agent of which the agent knows
        :param route_cards: Route card of which agent knows
        """
        print(f"--> Agent {agent_id} knows that agent {target_agent_id} has at least one of cards {route_cards}")
        if len(route_cards) == 1:
            # certainty when there is only one considered route card.
            self.update_relations(agent_id, target_agent_id, route_cards)
            return

        update_dict = []

        # Remove all relations from considered states by an agent where the above holds
        for relation in self.relations[agent_id]:
            if relation[0].has_agent_in_agent_list(agent_id, agent_id):
                # check if intersection is equal to route cards
                from_state = relation[0].get_state(target_agent_id)
                to_state = relation[1].get_state(target_agent_id)
                # remove relations where you go from considered states to states that don't have the above property
                if from_state.intersection(route_cards) and not to_state.intersection(route_cards):
                    continue
            update_dict.append(relation)

        self.relations[agent_id] = update_dict

        # agents no longer consider the worlds that violate the above property
        total_removal = 0
        for world in self.worlds:
            if world.has_agent_in_agent_list(agent_id, agent_id):
                target_set = world.get_state(target_agent_id)
                if not route_cards.intersection(target_set):
                    total_removal += 1
                    world.remove_agent_from_list(agent_id)

    def public_announcement_possibilities(self, agent_id: int, route_cards: set[str]):
        """
        Function that publicly announces the states agents think of as possible true states
        :param agent_id: Agent that announces possibilities
        :param route_cards: Route cards of which there will be an announcement
        """
        print(f"--> Publicly known that agent {agent_id} has at least one of cards {route_cards}")

        if len(route_cards) == 1:
            self.public_announcement_route_card(agent_id, route_cards)

        # remove relations
        for agent in self.agent_ids:
            update_dict = []
            for relation in self.relations[agent]:
                from_state = relation[0].get_state(agent_id)
                to_state = relation[1].get_state(agent_id)
                if from_state.intersection(route_cards) and to_state.intersection(route_cards):
                    # keep state if one of route cards is in state
                    update_dict.append(relation)

            self.relations[agent] = update_dict

        # remove worlds
        world_list = []
        for world in self.worlds:
            if route_cards.intersection(world.get_state(agent_id)):
                # true if card is in state for agent_id
                world_list.append(world)
            # else:
            #     print(f"Removing world {str(world)}")
        self.worlds = world_list

    def public_announcement_route_card(self, agent_id: int, route_card: set[str]):
        """
        Method to do a public announcement of a route card and remove worlds that are no longer possible
        :param agent_id: Agent that has route card
        :param route_card: Route card that is being announced
        """
        print(f"--> Publicly known that agent {agent_id} has card {route_card}")

        # remove relations
        for agent in self.agent_ids:
            update_dict = []
            for relation in self.relations[agent]:
                from_state = relation[0].get_state(agent_id)
                to_state = relation[1].get_state(agent_id)
                if not route_card.difference(from_state) and not route_card.difference(to_state):
                    # true if card in both states
                    update_dict.append(relation)

            self.relations[agent] = update_dict

        # remove worlds
        world_list = []
        for world in self.worlds:
            if not route_card.difference(world.get_state(agent_id)):
                # true if card is in state for agent_id
                world_list.append(world)
            # else:
            #     print(f"Removing world {str(world)}")

        self.worlds = world_list

    def get_known_route_cards(self, agent_id: int, target_agent_id: int) -> list[str]:
        """
        Function to retrieve the cards that one agent knows another agent has.
        :param agent_id: Agent of which the worlds are considered
        :param target_agent_id: Agent Id of which the agent knows the cards
        :return: List containing knows cards in string representation
        """
        world_counter = 0
        possible_target_cards = {}

        for world in self.worlds:
            if world.has_agent_in_agent_list(agent_id, agent_id):
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
