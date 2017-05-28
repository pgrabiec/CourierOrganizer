import time
import copy
import random

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
                             modify_solution=modify_solution_simple,
                             found_better_solution_callback=lambda iteration, cost: (),
                             BEST_SPOTS_NUMBER=10,
                             GOOD_SPOTS_NUMBER=5,
                             RANDOM_SPOTS_NUMBER=3,
                             BEST_SPOT_BEES=10,
                             GOOD_SPOT_BEES=5,
                             MAX_ITERATIONS_NUMBER=800):
    """
    Bees pham algorithm
    """

    def get_solution_cost(solution):
        """
        :param solution: [ [1, 3, 6], [2, 4, 5], ...]
        :return: int, distances sum
        """
        routes_costs = []
        for route in solution:
            route_cost = 0
            route_len = len(route)
            if route_len < 1:
                continue
            # Distance from starting point to the first on route
            route_cost += distances_matrix[0][route[0]]
            # Distance from the last on route to the starting point
            route_cost += distances_matrix[route[route_len - 1]][0]
            # Distances between points on route
            for index in range(0, route_len):
                if index <= route_len - 2:
                    route_cost += distances_matrix[route[index]][route[index + 1]]

            routes_costs.append(route_cost)
        return max(routes_costs)

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
                    for _ in range(search_size)] + [cost_solution_pair], key=lambda x: x[0])

    POPULATION_NUMBER = BEST_SPOTS_NUMBER + GOOD_SPOTS_NUMBER + RANDOM_SPOTS_NUMBER

    iterations = 0
    last_improvement_iteration = 0
    last_cost = None
    start_time = time.time()

    # Starting point not included in searching for solution
    target_points_to_visit = copy.copy(target_points)
    target_points_to_visit.remove(0)

    cost_solution_pairs = sorted([get_cost_solution_pair(get_random_solution(target_points_to_visit))
                                  for _ in range(POPULATION_NUMBER)])

    cost, _ = cost_solution_pairs[0]
    found_better_solution_callback(0, cost)

    improvement_resolution = 5
    since_improvement = improvement_resolution + 1

    for i in range(1, MAX_ITERATIONS_NUMBER + 1):
        since_improvement += 1
        # print("Cost: {}".format(cost_solution_pairs[0][0]))

        best_spots = cost_solution_pairs[0:BEST_SPOTS_NUMBER]
        good_spots = cost_solution_pairs[BEST_SPOTS_NUMBER:BEST_SPOTS_NUMBER + GOOD_SPOTS_NUMBER]

        best_spots_pairs = [get_best_from_neighbourhood(spot, BEST_SPOT_BEES)
                            for spot in best_spots]
        good_spots_pairs = [get_best_from_neighbourhood(spot, GOOD_SPOT_BEES)
                            for spot in good_spots]
        random_spots_pairs = [get_cost_solution_pair(get_random_solution(target_points_to_visit))
                              for _ in range(RANDOM_SPOTS_NUMBER)]

        cost_solution_pairs = sorted(best_spots_pairs + good_spots_pairs + random_spots_pairs)

        iterations = i

        cost, solution = cost_solution_pairs[0]
        if not last_cost:
            last_cost = cost
        elif cost < last_cost:
            last_improvement_iteration = i
            last_cost = cost
            if since_improvement > improvement_resolution:
                found_better_solution_callback(i, cost)
                since_improvement = 0

    cost, solution = cost_solution_pairs[0]

    found_better_solution_callback(iterations, cost)

    return {
        'total_iterations': iterations,
        'min_iterations': last_improvement_iteration,
        'cost': cost,
        'routes': solution,
        'real_time': time.time() - start_time,
    }
