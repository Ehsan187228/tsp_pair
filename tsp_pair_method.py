# This version only applies to distance matrices with unique edges.

import random
import time
from itertools import permutations


test1_dist =  [
    [0, 849, 210, 787, 601, 890, 617],
    [849, 0, 809, 829, 518, 386, 427],
    [210, 809, 0, 459, 727, 59, 530],
    [787, 829, 459, 0, 650, 346, 837],
    [601, 518, 727, 650, 0, 234, 401],
    [890, 386, 59, 346, 234, 0, 505],
    [617, 427, 530, 837, 401, 505, 0]
    ]

test2_dist = [
    [0, 97066, 6863, 3981, 24117, 3248, 88372],
    [97066, 0, 42429, 26071, 5852, 4822, 7846],
    [6863, 42429, 0, 98983, 29563, 63161, 15974],
    [3981, 26071, 98983, 0, 27858, 9901, 99304],
    [24117, 5852, 29563, 27858, 0, 11082, 35998],
    [3248, 4822, 63161, 9901, 11082, 0, 53335],
    [88372, 7846, 15974, 99304, 35998, 53335, 0]
    ]

test3_dist = [
    [0, 76, 504, 361, 817, 105, 409, 620, 892],
    [76, 0, 538, 440, 270, 947, 382, 416, 59],
    [504, 538, 0, 797, 195, 946, 121, 321, 674],
    [361, 440, 797, 0, 866, 425, 525, 872, 793],
    [817, 270, 195, 866, 0, 129, 698, 40, 871],
    [105, 947, 946, 425, 129, 0, 60, 997, 845],
    [409, 382, 121, 525, 698, 60, 0, 102, 231],
    [620, 416, 321, 872, 40, 997, 102, 0, 117],
    [892, 59, 674, 793, 871, 845, 231, 117, 0]
    ]

def get_dist(x, y, dist_matrix):
    return dist_matrix[x][y]

# Calculate distance of a route which is not complete
def calculate_partial_distance(route, dist_matrix):
    total_distance = 0
    for i in range(len(route)):
        if route[i-1] is not None and route[i] is not None:
            total_distance += get_dist(route[i - 1], route[i], dist_matrix)
    return total_distance


def run_pair_method(dist_matrix):
    n = len(dist_matrix)
    if n < 3: 
        print("Number of nodes is too few, might as well just use Brute Force method.")
        return
    
    shortest_route = [i for i in range(n)]
    shortest_dist = calculate_full_distance(shortest_route, dist_matrix)
    
    # Loop through all possible starting points
    for origin_node in range(n):
        # Initialize unvisited_nodes at each loop
        unvisited_nodes = [i for i in range(n)]
        # Initialize a fix size list, and set the starting node
        starting_route = [None] * n
        # starting_route should contain exactly 1 node at all time, for this case origin_node should be equal to its index, so the pop usage is fine
        starting_route[0] = unvisited_nodes.pop(origin_node)
        
        for perm in permutations(unvisited_nodes, 2):
            # Indices of the head and tail nodes
            head_index = 1
            tail_index = n - 1
            
            # Copy starting_route to current_route
            current_route = starting_route.copy()
            current_unvisited = unvisited_nodes.copy()
            current_route[head_index] = perm[0]
            current_unvisited.remove(perm[0])
            current_route[tail_index] = perm[1]
            current_unvisited.remove(perm[1])
            current_distance = calculate_partial_distance(current_route, dist_matrix)
            
            # If at this point the distance is already more than the shortest distance, then we skip this route
            if current_distance > shortest_dist:
                continue
            
            # Now keep looping while there are at least 2 unvisited nodes
            while head_index < (tail_index-2):

                # Now search for the pair of nodes that give lowest distance for this step, starting from the first permutation
                min_perm = [current_unvisited[0], current_unvisited[1]]
                min_dist = get_dist(current_route[head_index], current_unvisited[0], dist_matrix) + \
                    get_dist(current_unvisited[1], current_route[tail_index], dist_matrix)
                for current_perm in permutations(current_unvisited, 2):
                    dist = get_dist(current_route[head_index], current_perm[0], dist_matrix) + \
                    get_dist(current_perm[1], current_route[tail_index], dist_matrix)
                    if dist < min_dist:
                        min_dist = dist
                        min_perm = current_perm
                
                # Now update the list of route and unvisited nodes
                head_index += 1
                tail_index -= 1
                current_route[head_index] = min_perm[0]
                current_unvisited.remove(min_perm[0])
                current_route[tail_index] = min_perm[1]
                current_unvisited.remove(min_perm[1])

                # Now check that it is not more than the shortest distance we already have
                if calculate_partial_distance(current_route, dist_matrix) > shortest_dist:
                    # Break away from this loop if it does
                    break
                
            # If there is exactly 1 unvisited node, join the head and tail to this node
            if head_index == (tail_index - 2):
                head_index += 1
                current_route[head_index] = current_unvisited.pop(0)
                dist = calculate_full_distance(current_route, dist_matrix)
                # Now check if this dist is less than the shortest one we have, if yes then update our minimum
                if dist < shortest_dist:
                    shortest_dist = dist
                    shortest_route = current_route.copy()

            # If there is 0 unvisited node, just calculate the distance and check if it is minimum
            elif head_index == (tail_index - 1):
                dist = calculate_full_distance(current_route, dist_matrix)
                if dist < shortest_dist:
                    shortest_dist = dist
                    shortest_route = current_route.copy()

    return shortest_route, shortest_dist

def calculate_full_distance(route, dist_matrix):
    total_distance = 0
    for i in range(len(route)):
        total_distance += get_dist(route[i - 1], route[i], dist_matrix)
    return total_distance

def run_brute_force(dist_matrix):
    n = len(dist_matrix)
    # Create permutations of all possible nodes
    routes = permutations(range(n))
    # Pick a starting shortest route and calculate its distance
    shortest_route = [i for i in range(n)]
    min_distance = calculate_full_distance(shortest_route, dist_matrix)

    for route in routes:
        # Calculate distance of the route and compare to the minimum one
        current_distance = calculate_full_distance(route, dist_matrix)
        if current_distance < min_distance:
            min_distance = current_distance
            shortest_route = route

    return shortest_route, min_distance

def run_tsp_analysis(route_title, dist_matrix, run_func):
    print(route_title)
    start_time = time.time()
    shortest_route, min_distance = run_func(dist_matrix)
    end_time = time.time()
    
    print("Shortest route:", shortest_route)
    print("Minimum distance:", min_distance)
    elapsed_time = end_time - start_time
    print(f"Run time: {elapsed_time}s.\n")


run_tsp_analysis("Test 1 Brute Force", test1_dist, run_brute_force)
run_tsp_analysis("Test 1 Pair Method", test1_dist, run_pair_method)

run_tsp_analysis("Test 2 Brute Force", test2_dist, run_brute_force)
run_tsp_analysis("Test 2 Pair Method", test2_dist, run_pair_method)
    
run_tsp_analysis("Test 3 Brute Force", test3_dist, run_brute_force)
run_tsp_analysis("Test 3 Pair Method", test3_dist, run_pair_method)
