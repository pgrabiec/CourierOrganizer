import requests
from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs

from algorithm.core import calculate_vehicle_routes

app = Flask(__name__)


def get_distances_json(target_points):
    url = "http://router.project-osrm.org/table/v1/driving/"
    append_colon = False
    for node in target_points:
        if append_colon:
            url += ";"
        append_colon = True

        lat, lon = node

        url += str(lat)
        url += ","
        url += str(lat)

    url += "?generate_hints=false"

    request = requests.get(url)

    return request.json()


@app.route("/routes", methods=['post'])
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

    target_points = [(point['latitude'], point['longitude'])
                     for point in target_points]

    nodes_to_points = {}
    target_nodes = []

    osrm_table_json = ""
    try:
        osrm_table_json = get_distances_json(target_points)
        distances_matrix = osrm_table_json['durations']
    except KeyError as e:
        return jsonify({'error': str(e) + "\nOSRM response: " + str(osrm_table_json)}), 400

    solution = calculate_vehicle_routes(target_nodes, vehicles_number,
                                        distances_matrix)

    return jsonify({
        'iterations': solution['iterations'],
        'cost': solution['cost'],
        'routes': [[nodes_to_points[node] for node in route]
                   for route in solution['routes']]
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
