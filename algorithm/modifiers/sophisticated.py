from random import random
from copy import copy


def get_point_remove(solution, index):
    # look for the salesman with the random index point
    count = 0  # number of points passed so far
    last_count = 0  # number of points seen before the current salesman
    salesman_to_modify = None
    for salesman in solution:
        last_count = count
        count += len(salesman)
        if count >= index + 1:
            salesman_to_modify = salesman
            break

    if salesman_to_modify is None:
        return

    salesman_index = index - last_count - 1
    value = salesman_to_modify[salesman_index]
    del salesman_to_modify[salesman_index]
    return value


def modify_solution(solution, points_number, get_solution_cost):
    solution = copy(solution)
    size = points_number - 1  # number of points except the beginning point
    index = random.randint(0, size - 1)
    initial_cost = get_solution_cost(solution)

    # remove point corresponding with the random index
    point = get_point_remove(solution, index)

    # look for an insert that makes the cost decreased
    for salesman_index in range(0, len(solution)):
        salesman = solution[salesman_index]
        for point_index in range(0, len(salesman) + 1):
            salesman.insert(point_index, point)
            cost = get_solution_cost(solution)
            if cost < initial_cost:
                # print "Found better solution"
                # print cost
                return solution  # found a better solution - done
            del salesman[point_index]

    # no insert makes the solution better - insert randomly
    rand_salesman = random.randint(0, len(solution) - 1)
    salesman = solution[rand_salesman]
    if len(salesman) > 0:
        rand_index = random.randint(0, len(salesman) - 1)
    else:
        rand_index = 0
    salesman.insert(rand_index, point)
    # print "Inserting randomly"
    cost = get_solution_cost(solution)
    return solution
