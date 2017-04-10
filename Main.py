from ObjectiveFunction import get_distance_sum
from RandomDistancesGenerator import gen_distances
from RandomSolutionGenerator import gen_random_solutions
from SolutionModifier import modify_solution


def print_solution(solution, distances):
    print str(solution) + " " + str(get_distance_sum(solution, distances))


def test():
    points_number = 30
    vehicles_number = 3

    solution = gen_random_solutions(points_number, vehicles_number)
    distances = gen_distances(points_number, 100)

    lowest_cost = get_distance_sum(solution, distances)

    print_solution(solution, distances)
    for i in range(150):
        cost = get_distance_sum(solution, distances)
        if cost < lowest_cost:
            lowest_cost = cost
        modify_solution(solution, points_number, distances)
        print_solution(solution, distances)

    print "lowest cost: " + str(lowest_cost)

test()
