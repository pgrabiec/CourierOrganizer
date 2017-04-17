from copy import copy
import random


def modify_solution(solution, *args, **kwargs):
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
