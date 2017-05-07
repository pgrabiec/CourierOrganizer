import requests
from flask import Flask, jsonify
from requests import ConnectionError
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_cors import CORS, cross_origin

from algorithm.core import calculate_vehicle_routes

app = Flask(__name__)


def get_distances_json(target_points):
    point_strings = [','.join([str(lat), str(lon)]) for lat, lon in target_points]
    points_param = ';'.join(point_strings)
    url = "http://router.project-osrm.org/table/v1/driving/{}".format(points_param)
    response = requests.get(url, data={'generate_hints': 'false'})
    return response.json()


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

    osrm_table_json = None
    try:
        osrm_table_json = get_distances_json(target_points)
        distances_matrix = osrm_table_json['durations']
    except KeyError as e:
        return jsonify({'error': str(e) + "\nOSRM response: " + str(osrm_table_json)}), 400
    except ConnectionError as e:
        return jsonify({'error': str(e) + "\nOSRM response: " + str(osrm_table_json)}), 400

    solution = calculate_vehicle_routes(list(range(0, len(target_points))), vehicles_number,
                                        distances_matrix)

    return jsonify({
        'iterations': solution['iterations'],
        'cost': solution['cost'],
        'routes': [[nodes_to_points[node] for node in route]
                   for route in solution['routes']]
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
