from math import sqrt

import requests
import sys
from flask import Flask, jsonify
from requests import ConnectionError
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_cors import CORS, cross_origin

from algorithm.core import calculate_vehicle_routes

app = Flask(__name__)


def calculate_distance(coor1, coor2):
    coefficient = 111  # km per 1 degree
    lon1, lat1 = coor1
    lon2, lat2 = coor2
    return sqrt(pow(lat1 - lat2, 2) + pow(lon1 - lon2, 2)) * coefficient


def create_distances_cartesian(target_points):
    size = len(target_points)
    return [
        [
            calculate_distance(target_points[i], target_points[j])
            for j in range(size)
        ]
        for i in range(size)
    ]


def get_distances_table_api(target_points):
    point_strings = [','.join([str(lat), str(lon)]) for lat, lon in target_points]
    points_param = ';'.join(point_strings)
    url = "http://router.project-osrm.org/table/v1/driving/{}".format(points_param)
    print("URL: ", url, file=sys.stderr)
    response = requests.get(url, data={'generate_hints': 'false'})
    print("Response: " + str(response), file=sys.stderr)
    return response.json()['durations']


@app.route("/routes", methods=['post'])
@cross_origin(origin='*')
@use_kwargs({
    'vehicles_number': fields.Int(required=True),
    'target_points': fields.List(fields.Nested({
        'latitude': fields.Float(required=True),
        'longitude': fields.Float(required=True),
    }), required=True)
})
def calculate_route(vehicles_number, target_points):
    if len(target_points) < 1:
        return jsonify({
            'iterations': 0,
            'cost': 0,
            'routes': []
        })

    target_points = [(point['longitude'], point['latitude'])
                     for point in target_points]

    nodes_to_points = {}

    for index, target_point in enumerate(target_points):
        nodes_to_points[index] = target_point

    try:
        distances_matrix = create_distances_cartesian(target_points)  # get_distances_table_api(target_points)
    except KeyError as e:
        return jsonify({'error': str(e)}), 400
    except ConnectionError as e:
        return jsonify({'error': str(e)}), 400
    solution = calculate_vehicle_routes(list(range(0, len(target_points))), vehicles_number,
                                        distances_matrix)

    return jsonify({
        'total_iterations': solution['total_iterations'],
        'cost': solution['cost'],
        'real_time': solution['real_time'],
        'min_iterations': solution['min_iterations'],
        'routes': [[nodes_to_points[node] for node in route]
                   for route in solution['routes']]
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
