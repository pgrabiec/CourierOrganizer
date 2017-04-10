import random


def gen_random_ranges(number_of_ranges, max_r):
    # Index starting with 1 (0 reserved for starting point)
    random_numbers = [random.randint(1, max_r) for i in range(number_of_ranges - 1)]
    random_numbers = sorted(random_numbers)
    first = 0
    for i in random_numbers:
        yield (first, i)
        first = i
    yield (first, max_r)


def gen_random_solutions(number_of_points, number_of_vehicles):
    points = list(range(number_of_points))
    random.shuffle(points)
    solutions = [points[r[0]:r[1]] for r in gen_random_ranges(number_of_vehicles, number_of_points)]
    return solutions
