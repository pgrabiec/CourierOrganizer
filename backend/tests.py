import math
import os
import random

import plotly
from plotly.graph_objs import Scatter, Layout, Figure

from backend.algorithm.core import calculate_vehicle_routes

PROBLEM_SIZE = 25
TESTS_REPEAT = 10


def execute(distances, vehicles_number, bees_best, bees_good):
    improvements = []

    def clb(iteration, cost):
        improvements.append({
            'iteration': iteration,
            'cost': cost
        })
        # print('improvement ' + str(cost))

    result = calculate_vehicle_routes(
        list(range(0, len(distances))),
        vehicles_number,
        distances,
        found_better_solution_callback=clb,
        BEST_SPOT_BEES=bees_best,
        GOOD_SPOT_BEES=bees_good)

    return {
        'best_routes': result['routes'],
        'best_cost': result['cost'],
        'total_iterations': result['total_iterations'],
        'iteration_of_best_solution': result['min_iterations'],
        'total_time_elapsed': result['real_time'],
        'improvements': improvements
    }


def get_sample_settings():
    settings = []
    for bees_best in [4, 10]:
        for salesmen in [2, 5]:
            settings.append((bees_best, int(bees_best * 1 / 4), salesmen))
            settings.append((bees_best, int(bees_best * 3 / 4), salesmen))
    return settings


def create_problem():
    coordinates_limit = 1000
    points = [
        (
            random.random() * coordinates_limit,
            random.random() * coordinates_limit
        )
        for _ in range(PROBLEM_SIZE)
    ]

    def distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    return [
        [
            distance(points[i], points[j])
            for j in range(len(points))
        ]
        for i in range(len(points))
    ]


def bees_algo_evaluate():
    figures = []
    titles = []
    plot_titles = []

    if not os.path.exists("./diagrams"):
        os.makedirs("./diagrams")
    distances = create_problem()
    settings = get_sample_settings()

    tests_count = len(settings) * TESTS_REPEAT

    i = 1
    best_of_the_best = None
    best_of_the_best_iter = None
    best_of_the_best_settings = None
    worst = None
    for bees_best, bees_good, salesmen in get_sample_settings():
        x = []
        y = []
        best = None
        best_iter = 0
        for test_num in range(TESTS_REPEAT):
            print("Test " + str(i) + " out of " + str(tests_count))
            i += 1

            results = execute(distances, salesmen, bees_best, bees_good)

            if best is None:
                best = results['best_cost']
                best_iter = results['iteration_of_best_solution']
            elif best > results['best_cost']:
                best = results['best_cost']
                best_iter = results['iteration_of_best_solution']

            if best_of_the_best is None:
                best_of_the_best = best
                best_of_the_best_iter = best_of_the_best_iter
                best_of_the_best_settings = (bees_best, bees_good, salesmen)

            if best_of_the_best > best:
                best_of_the_best = best
                best_of_the_best_iter = best_iter
                best_of_the_best_settings = (bees_best, bees_good, salesmen)

            for improvement in results['improvements']:
                x.append(improvement['iteration'])
                y.append(improvement['cost'])
                if worst is None:
                    worst = improvement['cost']
                elif worst < improvement['cost']:
                    worst = improvement['cost']

        title = "_".join([
            "salesmen:" + str(salesmen),
            "best:" + str(bees_best),
            "good:" + str(bees_good)
        ])

        plot_title = "\n".join([
            "salesmen: " + str(salesmen),
            "bees best: " + str(bees_best),
            "bees good: " + str(bees_good),
            "best cost: " + str(best),
            "best iterations: " + str(best_iter)
        ])

        figures.append([Scatter(x=x, y=y, mode='markers')])
        plot_titles.append(plot_title)
        titles.append(title)

    print("Best cost: " + str(best_of_the_best))
    print("Best cost iterations: " + str(best_of_the_best_iter))

    bbest, bgood, vehicles = best_of_the_best_settings
    print("Best settings: " + str({
        'bees_best': bbest,
        'bees_good': bgood,
        'vehicles': vehicles
    }))

    for i in range(len(figures)):
        plotly.offline.plot(
            Figure(
                data=figures[i],
                layout=Layout(
                    title=plot_titles[i],
                    xaxis=dict(
                        title='Iterations'
                    ),
                    yaxis=dict(
                        title='Cost',
                        range=[0, int(worst * 1.1)]
                    )
                )
            ),
            filename=("diagrams/" + titles[i] + ".html"),
            auto_open=False
        )

bees_algo_evaluate()
