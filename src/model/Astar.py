# packages
import random

# settings
EPSILON = 1e-7


def a_star_algorithm(network, start, stop):
    # Open_lst contains a list of nodes which have not been visited.
    # Closed_lst is a list of nodes which have been visited.
    open_lst = {start}
    closed_lst = set([])

    # poo has current distances from start to all other nodes
    poo = {start: 0}

    # par contains an adjacency mapping of all nodes
    par = {start: start}

    while len(open_lst) > 0:
        n_val = None
        n_options = None

        # it will find a node with the lowest value of f() = g() + h()
        for v in open_lst:
            v_val = poo[v] + network.get_heur_val(v, stop)
            if n_options is None or v_val < n_val - EPSILON:
                n_options = [v]
                n_val = v_val
            elif v_val <= n_val + EPSILON:
                n_options.append(v)

        if n_val is None:
            print('Path does not exist!')
            return None

        n = random.choice(n_options)

        # if the current node is the stop then we obtain the final route by starting again from start
        if n == stop:
            reconstruct_path = []
            while par[n] != n:
                reconstruct_path.append(n)
                n = par[n]
            reconstruct_path.append(start)
            reconstruct_path.reverse()
            # print('Path found: {}'.format(reconstruct_path))
            return reconstruct_path

        # for all the neighbors of the current node do
        neighbours = network.get_neighbours(n).copy()
        random.shuffle(neighbours)
        for (m, weight) in neighbours:
            # if the current node is not present in both open_lst and closed_lst
            # add it to open_lst and note n as it's par
            if m not in open_lst and m not in closed_lst:
                open_lst.add(m)
                par[m] = n
                poo[m] = poo[n] + weight

            # otherwise, check if it's quicker to first visit n, then m
            # and if it is, update par data and poo data
            # and if the node was in the closed_lst, move it to open_lst
            else:
                if poo[m] >= poo[n] + weight - EPSILON:
                    if poo[m] > poo[n] + weight + EPSILON or random.random() > 0.5:
                        poo[m] = poo[n] + weight
                        par[m] = n

                        # if m in closed_lst:  # TODO: still necessary?
                        #     closed_lst.remove(m)
                        #     open_lst.add(m)

        # remove n from the open_lst, and add it to closed_lst
        # because all of his neighbors were inspected
        open_lst.remove(n)
        closed_lst.add(n)

    print('Path does not exist!')
    return None
