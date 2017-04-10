import random

from copy import copy

from ObjectiveFunction import get_distance_sum


def modify_solution(solution):
    solution = copy(solution)
    if random.random() < 0.5:
        salesman_index = random.randint(0, len(solution)-1)

        if not solution[salesman_index]:
            return solution

        random_index_1 = random.randint(0, len(solution[salesman_index])-1)
        random_index_2 = random.randint(0, len(solution[salesman_index])-1)
        solution[salesman_index][random_index_1], solution[salesman_index][random_index_2] =\
            solution[salesman_index][random_index_2], solution[salesman_index][random_index_1]
    else:
        salesman_index_1 = random.randint(0, len(solution) - 1)
        salesman_index_2 = random.randint(0, len(solution) - 1)

        if not solution[salesman_index_1] or not solution[salesman_index_2]:
            return solution

        random_index_1 = random.randint(0, len(solution[salesman_index_1]) - 1)
        random_index_2 = random.randint(0, len(solution[salesman_index_2]) - 1)

        element = solution[salesman_index_1].pop(random_index_1)
        solution[salesman_index_2].insert(random_index_2, element)
    return solution


# removes and returns the value of the index'th element (point index) found iterating on consecutive salesman lists
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


# modifies solution by reference
def modify_solution_bruteforce(solution, points_number, distances):
    solution = copy(solution)
    size = points_number - 1  # number of points except the beginning point
    index = random.randint(0, size - 1)
    initial_cost = get_distance_sum(solution, distances)

    # remove point corresponding with the random index
    point = get_point_remove(solution, index)

    # look for an insert that makes the cost decreased
    for salesman_index in range(0, len(solution)):
        salesman = solution[salesman_index]
        for point_index in range(0, len(salesman) + 1):
            salesman.insert(point_index, point)
            cost = get_distance_sum(solution, distances)
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
    cost = get_distance_sum(solution, distances)
    return solution
