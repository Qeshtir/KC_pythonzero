import pandas as pd
import time
start_time = time.time()

url='https://drive.google.com/uc?id=1-crPzL6qMinByPzsrEHhGn1EJ1MfD3GX'
df = pd.read_csv(url, names=list(range(0, 100, 1)))
city_map_list = df.values.tolist()

tests = [[(17, 99), [(42, 76), (27, 80), (43, 52), (26, 75)]],
            [(84, 17),
            [(66, 32), (39, 75), (90, 10), (89, 60), (79, 77), (65, 38), (9, 5)]],
            [(10, 55),
            [(99, 48),
            (75, 90),
            (23, 29),
            (23, 96),
            (73, 11),
            (91, 88),
            (25, 50),
            (3, 69)]],
            [(10, 87),
            [(83, 38),
            (94, 56),
            (72, 75),
            (74, 64),
            (62, 15),
            (83, 99),
            (84, 25),
            (66, 7),
            (71, 41),
            (2, 40)]],
            [(22, 3),
            [(15, 38),
            (55, 13),
            (33, 1),
            (61, 88),
            (90, 66),
            (19, 91),
            (61, 58),
            (15, 74)]],
            [(9, 82), [(4, 6), (85, 25)]], [(26, 26), [(29, 29), (0, 0), (0, 3)]]]
def navigator(courier_location, orders_location):
    # HERE is the task starts
    # here is a default weight assignment
    if city_map_list[1][1] == 1:
        for i in range(100):
            for j in range(100):
                if city_map_list[i][j] == 1:
                    city_map_list[i][j] = [1, float('inf')]
                else:
                    city_map_list[i][j] = [0, float('inf')]

    map_len = len(city_map_list[0]) - 1
    # here is a courier position weight assignment
    city_map_list[courier_location[1]][courier_location[0]][1] = 0

    def get_adjacent_nodes(node):
        nodes = []
        # let's search if there is any impossible indexes (map borders)
        # If no, it's somewhere out of borders. Let's check each side
        if node[0] < map_len:
            if city_map_list[node[1]][node[0] + 1][0] == 1:  # right cell is reachable
                nodes.append((node[0] + 1, node[1]))
        if node[1] > 0:
            if city_map_list[node[1] - 1][node[0]][0] == 1:  # upper cell is reachable
                nodes.append((node[0], node[1] - 1))
        if node[1] < map_len:
            if city_map_list[node[1] + 1][node[0]][0] == 1:  # bottom cell is reachable
                nodes.append((node[0], node[1] + 1))
        if node[0] > 0:
            if city_map_list[node[1]][node[0] - 1][0] == 1:  # left cell is reachable
                nodes.append((node[0] - 1, node[1]))
        return nodes

    def build_path(to_node, previous_path):
        # previous path is a dict with actual_node as a key and previous_node as a value
        # we used to unpack this dict to a valid path after discovering target node
        path = []
        while previous_path.get(to_node):
            path.append(to_node)
            to_node = previous_path[to_node]
        # print(f"Previous path is {previous_path}")
        return path[::-1]

    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    # def choose_node(reachable):
    #     best_node = None
    #     for node in reachable:
    #         if best_node is None or city_map_list[best_node[1]][best_node[0]][1] > city_map_list[node[1]][node[0]][1]:
    #             best_node = node
    #     return best_node

    def choose_node(reachable, end_node):
        min_cost = float('Inf')
        best_node = None
        for node in reachable:
            cost_start_to_node = city_map_list[node[1]][node[0]][1]
            cost_node_to_goal = heuristic(node, end_node)
            total_cost = cost_start_to_node + cost_node_to_goal

            if min_cost > total_cost:
                min_cost = total_cost
                best_node = node
        return best_node

    def find_path(start_node, end_node):
        # create two lists with reachable and explored nodes
        reachable = [start_node]
        explored = []
        previous_path = {}
        # create cycle, finding the way
        while reachable:
            # choose some node
            node = choose_node(reachable, end_node)
            # testing positions
            # print(f"current node:{node}{city_map_list[node[1]][node[0]][1]}")
            # print(f"reachable nodes:{reachable}")
            # print(f"explored nodes:{explored}")

            # if we are in target node, build path and return
            if node == end_node:
                return build_path(end_node, previous_path)

            # do not repeat explored nodes
            reachable.remove(node)
            explored.append(node)

            # where can we go from here?
            # use difference to find only new nodes. It's a list comprehension
            new_reachable = [variant for variant in get_adjacent_nodes(node) if variant not in explored]
            # Now we are used to create new explorable nodes

            for adjacent in new_reachable:
                if adjacent not in reachable:
                    reachable.append(adjacent)
                    previous_path[adjacent] = node  # last step for getting to the node we are keeping all nodes
                # little trick to make node searcher faster - weight assignment
                if city_map_list[node[1]][node[0]][1] + 1 <= city_map_list[adjacent[1]][adjacent[0]][1]:
                    city_map_list[adjacent[1]][adjacent[0]][1] = city_map_list[node[1]][node[0]][1] + 1

        # If there is no path
        return None

    route = []
    start_pos = courier_location
    order_pos = orders_location
    for order in range(len(order_pos)):
        route.extend(find_path(start_pos, order_pos[order]))
        print(find_path(start_pos, order_pos[order]))
        start_pos = find_path(start_pos, order_pos[order])[-1]

    return route



for test in tests:
        courier_location_test = test[0]
        orders_location_test = test[1]
        result = navigator(courier_location_test, orders_location_test)
        print(result)


end_time = time.time()
elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)