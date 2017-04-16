import osmapi

from pymodm import connect
from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from algorithm.core import calculate_vehicle_routes
from models import Graph
from osm import create_graph_from_osm_map


connect("mongodb://localhost:27017/courierOrganizer")

app = Flask(__name__)


@app.route("/graphs/<graph_id>/routes", methods=['post'])
@use_args({
    'vehicles_number': fields.Int(required=True),
    'target_points': fields.List(fields.Float, required=True),
})
def calculate_route(args, graph_id):
    graph = Graph.objects.get({'_id': graph_id})

    # TODO: add function which matches target_points with specific points in graph
    vehicles_number = args['vehicles_number']
    target_points = []

    solution = calculate_vehicle_routes(target_points, vehicles_number, graph.distances_matrix)

    return jsonify({
        'iterations': solution['iterations'],
        'cost': solution['cost'],
        'routes': []  # TODO: map graph points to map points
    })


@app.route('/graphs', methods=['get'])
def list_graphs():
    return jsonify({
        'graphs': [{'id': str(graph.pk),
                    'boundary': graph.boundary,
                    'nodes_count': len(graph.nodes)
                    } for graph in Graph.objects.all()]
    })


@app.route('/graphs', methods=['post'])
@use_args({
    'min_longitude': fields.Float(required=True),
    'min_latitude': fields.Float(required=True),
    'max_longitude': fields.Float(required=True),
    'max_latitude': fields.Float(required=True),
})
def create_graph(args):
    """

    """
    api = osmapi.OsmApi()
    osm_map_data = api.Map(args['min_longitude'], args['min_latitude'],
                           args['max_longitude'], args['max_latitude'])

    nodes, distances_matrix = create_graph_from_osm_map(osm_map_data)

    graph = Graph(boundary=args, nodes=nodes, distances_matrix=distances_matrix)
    graph.save()

    return jsonify({
        'graph_id': str(graph.pk),
    })


@app.route('/graphs/<graph_id>', methods=['delete'])
def delete_graph(graph_id):
    """
    Removes graph from database.
    """
    try:
        Graph.objects.get({'_id': graph_id}).delete()
        return jsonify({'status': 'success'}), 200
    except Graph.DoesNotExist:
        return jsonify({'status': 'not found'}), 404


if __name__ == "__main__":
    app.run()
