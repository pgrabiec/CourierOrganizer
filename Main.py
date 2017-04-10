from RandomDistancesGenerator import gen_distances
from RandomSolutionGenerator import gen_random_solutions

points_nubmer = 20
vehicles_number = 3

solution = gen_random_solutions(points_nubmer, vehicles_number)
distances = gen_distances(points_nubmer, 100)


