import pandas as pd
import random
import time
start_time = time.time()

url='https://drive.google.com/uc?id=1-crPzL6qMinByPzsrEHhGn1EJ1MfD3GX'
df = pd.read_csv(url, names=list(range(0, 100, 1)))
city_map_list = df.values.tolist()


# region Test data and an example of really bad implementation of finding map borders, just for history.
# print(city_map_list)

# city_map_list = [
# [1, 1, 0, 0, 1],
# [1, 1, 0, 0, 1],
# [1, 1, 1, 1, 1],
# [0, 0, 0, 0, 1],
# [0, 0, 0, 0, 1]
# ]
# previous_path = {}


# courier_location = (2, 2)
# orders_location = [(4, 0), (0, 2), (4, 3)]
# courier_location = (10, 10)
# orders_location = [(1, 1), (92, 13), (46, 33)]
courier_location = (84, 17)
orders_location = [(66, 32), (39, 75), (90, 10), (89, 60), (79, 77), (65, 38), (9, 5)]
# courier_location = (17, 99)
# orders_location = [(42, 76), (27, 80), (43, 52), (26, 75)]

# def get_adjacent_nodes(node):
#     nodes = []
#     # let's search for map borders
#     # corners
#     # left top corner y == 0, x == 0
#     if node == (0, 0):
#         if city_map_list[0][1] == 1: # right cell is reachable
#             nodes.append((1, 0))
#         if city_map_list[1][0] == 1: # bottom cell is reachable
#             nodes.append((0, 1))
#     # left bottom corner y == map_len, x == 0
#     elif node == (0, map_len_coords):
#         if city_map_list[map_len][1] == 1: # right cell is reachable
#             nodes.append((1, map_len_coords))
#         if city_map_list[map_len - 1][0] == 1: # upper cell is reachable
#             nodes.append((0, map_len_coords - 1))
#     # right top corner y == 0, x == map_len
#     elif node == (map_len_coords, 0):
#         if city_map_list[0][map_len - 1] == 1:  # left cell is reachable
#             nodes.append((map_len_coords - 1, 0))
#         if city_map_list[1][map_len] == 1:  # bottom cell is reachable
#             nodes.append((map_len_coords, 1))
#     # right bottom corner y == map_len, x == map_len
#     elif node == (map_len_coords, map_len_coords):
#         if city_map_list[map_len][map_len - 1] == 1:  # left cell is reachable
#             nodes.append((map_len_coords - 1, map_len_coords))
#         if city_map_list[map_len - 1][map_len] == 1:  # upper cell is reachable
#             nodes.append((map_len_coords, map_len_coords - 1))
#     # borders
#     # top border y == 0, x == any
#     elif node == (node[0], 0):
#         if city_map_list[0][node[0]] == 1:  # right cell is reachable
#             nodes.append((node[0], 0))
#         if city_map_list[1][node[0]] == 1:  # bottom cell is reachable
#             nodes.append((node[0], 1))
#         if city_map_list[0][node[0] - 1] == 1:  # left cell is reachable
#             nodes.append((node[0] - 1, 0))
#     # right border y == any, x == map_len
#     elif node == (map_len_coords, node[1]):
#         if city_map_list[node[1]][map_len - 1] == 1:  # left cell is reachable
#             nodes.append((map_len_coords - 1, node[1]))
#         if city_map_list[node[1] - 1][map_len] == 1:  # upper cell is reachable
#             nodes.append((map_len_coords, node[1] - 1))
#         if city_map_list[node[1] + 1][map_len] == 1:  # bottom cell is reachable
#             nodes.append((map_len_coords, node[1] + 1))
#     # bottom border y == map_len, x == any
#     elif node == (node[0], map_len_coords):
#         if city_map_list[map_len][node[0] - 1] == 1:  # left cell is reachable
#             nodes.append((node[0] - 1, map_len_coords))
#         if city_map_list[map_len - 1][node[0]] == 1:  # upper cell is reachable
#             nodes.append((node[0], map_len_coords - 1))
#         if city_map_list[map_len][node[0] + 1] == 1:  # right cell is reachable
#             nodes.append((node[0] + 1, map_len_coords))
#     # left border y == any, x == 0
#     elif node == (0, node[1]):
#         if city_map_list[node[1]][1] == 1:  # right cell is reachable
#             nodes.append((1, node[1]))
#         if city_map_list[node[1] - 1][0] == 1:  # upper cell is reachable
#             nodes.append((0, node[1] - 1))
#         if city_map_list[node[1] + 1][0] == 1:  # bottom cell is reachable
#             nodes.append((0, node[1] + 1))
#     # all right, it's somewhere out of borders. Let's check each side
#     else:
#         if city_map_list[node[1]][node[0] + 1] == 1:  # right cell is reachable
#             nodes.append((node[0] + 1, node[1]))
#         if city_map_list[node[1] - 1][node[0]] == 1:  # upper cell is reachable
#             nodes.append((node[0], node[1] - 1))
#         if city_map_list[node[1] + 1][node[0]] == 1:  # bottom cell is reachable
#             nodes.append((node[0], node[1] + 1))
#         if city_map_list[node[1]][node[0] - 1] == 1:  # left cell is reachable
#             nodes.append((node[0] - 1, node[1]))
#     return nodes
# endregion

# Промежуточные переменные для более удобной работой с координатами
map_len = len(city_map_list[0]) - 2
map_len_coords = len(city_map_list[0]) - 1
def get_adjacent_nodes(node):
    nodes = []
    # let's search for map borders
    # all right, it's somewhere out of borders. Let's check each side
    if node[0] < map_len:
            if city_map_list[node[1]][node[0] + 1] == 1:  # right cell is reachable
                nodes.append((node[0] + 1, node[1]))
    if node[1] > 0:
          if city_map_list[node[1] - 1][node[0]] == 1:  # upper cell is reachable
                nodes.append((node[0], node[1] - 1))
    if node[1] < map_len:
        if city_map_list[node[1] + 1][node[0]] == 1:  # bottom cell is reachable
            nodes.append((node[0], node[1] + 1))
    if node[0] > 0:
        if city_map_list[node[1]][node[0] - 1] == 1:  # left cell is reachable
            nodes.append((node[0] - 1, node[1]))
    return nodes

def build_path(to_node, previous_path):
    # previous path is a dict with actual_node as a key and previous_node as a value
    # we used to unpack this dict to a valid path after discovering target node
    path = []
    while previous_path.get(to_node):
        #global path

        path.append(to_node)
        to_node = previous_path[to_node]
    return path[::-1]


def find_path(start_node, end_node):
    # create two lists with reachable and explored nodes
    reachable = [start_node]
    explored = []
    previous_path = {}
    # create cycle, finding the way
    while reachable:
        # choose some node
        node = random.choice(reachable)
        # testing positions
        # print(f"current node:{node}")
        # print(f"reachable nodes:{reachable}")
        # print(f"explored nodes:{explored}")
        # if we are in target node, build path and return
        if node == end_node:
            return build_path(end_node, previous_path)
            break

        # do not repeat explored nodes
        reachable.remove(node)
        explored.append(node)

        # where can we go from here?
        # use difference to find only new nodes. It's a list comprehension
        new_reachable = [variant for variant in get_adjacent_nodes(node) if variant not in explored]
        # Now we are used to create new explorable nodes
        for adjacent in new_reachable:
            if adjacent not in reachable:
                previous_path[adjacent] = node  # last step for getting to the node
                reachable.append(adjacent)

    # If there is no path
    return None

# Creating a route
route = []
start_pos = courier_location
for i in range(len(orders_location)):
    route.extend(find_path(start_pos, orders_location[i]))
    start_pos = find_path(start_pos, orders_location[i])[-1]



# region Test data (step by step when creating a route)
# path_1 = find_path(courier_location, orders_location[0])
# path_2 = find_path(path_1[0], orders_location[1])
# path_3 = find_path(path_2[0], orders_location[2])

# print(path_1)
# print(path_2)
# print(path_3)
# endregion

# auto test fot including packages in resulting route
print(f"Route is {route}")
for i in orders_location:
    for j in route:
        if i == j:
            print(f"found {i}")
end_time = time.time()
elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)