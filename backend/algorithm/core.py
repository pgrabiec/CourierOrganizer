import copy
import random

from settings import (
    POPULATION_NUMBER, MAX_ITERATIONS_NUMBER, BEST_SPOTS_NUMBER,
    GOOD_SPOTS_NUMBER, RANDOM_SPOTS_NUMBER,
    BEST_SPOT_BEES, GOOD_SPOT_BEES
)

from .modifiers.simple import modify_solution as modify_solution_simple


def random_ranges(number_of_ranges, max_r):
    random_numbers = [random.randint(0, max_r) for i in range(number_of_ranges - 1)]
    random_numbers = sorted(random_numbers)
    first = 0
    for i in random_numbers:
        yield (first, i)
        first = i
    yield (first, max_r)


def calculate_vehicle_routes(target_points,
                             vehicles_number,
                             distances_matrix,
                             modify_solution=modify_solution_simple):
    """
    Bees pham algorithm
    """
    def get_solution_cost(solution):
        """
        :param solution: [ [1, 3, 6], [2, 4, 5], ...]
        :return: int, distances sum
        """
        return sum(sum(distances_matrix[i][j] for i, j in zip(vehicle[:-1], vehicle[1:]))
                   for vehicle in solution)

    def get_random_solution(points):
        """

        :param points_number:
        :return: Ran
        """
        points = copy.copy(points)
        random.shuffle(points)
        return [points[r[0]:r[1]] for r in random_ranges(vehicles_number, len(points))]

    def get_cost_solution_pair(solution):
        return get_solution_cost(solution), solution

    def get_best_from_neighbourhood(cost_solution_pair, search_size):
        """

        :param cost_solution_pair:
        :param search_size:
        :return:
        """
        cost, solution = cost_solution_pair
        return min([get_cost_solution_pair(modify_solution(solution,
                                                           len(target_points),
                                                           get_solution_cost))
                    for _ in range(search_size)] + [cost_solution_pair])

    iterations = 0

    cost_solution_pairs = sorted([get_cost_solution_pair(get_random_solution(target_points))
                                 for _ in range(POPULATION_NUMBER)])

    for i in range(MAX_ITERATIONS_NUMBER):
        print("Cost: {}".format(cost_solution_pairs[0][0]))

        best_spots = cost_solution_pairs[0:BEST_SPOTS_NUMBER]
        good_spots = cost_solution_pairs[BEST_SPOTS_NUMBER:GOOD_SPOTS_NUMBER]

        best_spots_pairs = [get_best_from_neighbourhood(spot, BEST_SPOT_BEES)
                            for spot in best_spots]
        good_spots_pairs = [get_best_from_neighbourhood(spot, GOOD_SPOT_BEES)
                            for spot in good_spots]
        random_spots_pairs = [get_cost_solution_pair(get_random_solution(target_points))
                              for _ in range(RANDOM_SPOTS_NUMBER)]

        cost_solution_pairs = sorted(best_spots_pairs + good_spots_pairs + random_spots_pairs)

        iterations = i

    cost, solution = cost_solution_pairs[0]

    return {
        'iterations': iterations,
        'cost': cost,
        'routes': solution,
    }
