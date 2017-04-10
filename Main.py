from ObjectiveFunction import get_distance_sum
from RandomDistancesGenerator import gen_distances
from RandomSolutionGenerator import gen_random_solutions
from SolutionModifier import modify_solution

points_nubmer = 20
vehicles_number = 3

solution = gen_random_solutions(points_nubmer, vehicles_number)
distances = gen_distances(points_nubmer, 100)


population_number = 10  # number of solutions
iterations = 100
selected_spots_number = 5

best_solution_bees = 10

solutions = [gen_random_solutions(points_nubmer, vehicles_number)
             for _ in range(population_number)]

solutions = sorted([(get_distance_sum(s, distances), s) for s in solutions])


def get_best_modified_solution(solution):
    modified_solutions = [modify_solution(solution) for _ in range(best_solution_bees)]
    modified_solution_fitness = sorted([(get_distance_sum(s, distances), s) for s in modified_solutions]
                                       + [(get_distance_sum(solution, distances), solution)])
    return modified_solution_fitness[0]


while iterations > 0:
    print("Fitness: {}".format(solutions[0][0]))
    selected_spots = solutions[0:selected_spots_number]
    new_solutions = [get_best_modified_solution(s) for s in selected_spots]

    random_solutions = [gen_random_solutions(points_nubmer, vehicles_number)
                        for _ in range(population_number-selected_spots)]
    random_solutions = [(get_distance_sum(s, distances), s) for s in random_solutions]

    solutions = sorted(new_solutions + random_solutions)

    iterations -= 1


