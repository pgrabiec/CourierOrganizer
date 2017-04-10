import random
from collections import defaultdict


def gen_distances(number_of_points, max_distance):
    pairs = [(i, j) for i in range(number_of_points) for j in range(number_of_points) if i < j]
    distance = defaultdict(dict)
    for l, p in pairs:
        d = random.randint(1, max_distance)
        distance[l][l] = 0
        distance[l][p] = d
        distance[p][l] = d
    return distance
