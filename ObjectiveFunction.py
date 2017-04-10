# Param solution [[1, 3, 6], [2, 4, 5], ...]
def get_distance_sum(solution, distances):
    dist = 0
    for salesman in solution:
        for i, j in zip(salesman[:-1], salesman[1:]):
            dist = dist + distances[i][j]
    return dist
