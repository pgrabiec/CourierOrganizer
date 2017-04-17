from bson import ObjectId
from bson.errors import InvalidId
import osmapi

from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from algorithm.core import calculate_vehicle_routes
from models import Graph, GraphNode
from osm import create_graph_from_osm_map

app = Flask(__name__)


@app.route("/graphs/<graph_id>/routes", methods=['post'])
@use_kwargs({
    'vehicles_number': fields.Int(required=True),
    'target_points': fields.List(fields.Nested({
        'latitude': fields.Float(required=True),
        'longitude': fields.Float(required=True),
    }), required=True)
})
def calculate_route(graph_id, vehicles_number, target_points):
    try:
        graph = Graph.objects.get({'_id': ObjectId(graph_id)})
    except (Graph.DoesNotExist, InvalidId):
        return jsonify({'error': 'not found'}), 404

    target_points = [(point['latitude'], point['longitude'])
                     for point in target_points]

    nodes_to_points = {}
    target_nodes = []

    for latitude, longitude in target_points:
        node = graph.get_nearest_node(latitude, longitude)
        nodes_to_points[node.index] = (latitude, longitude)
        target_nodes.append(node.index)

    solution = calculate_vehicle_routes(target_nodes, vehicles_number,
                                        graph.distances_matrix)

    return jsonify({
        'iterations': solution['iterations'],
        'cost': solution['cost'],
        'routes': [[nodes_to_points[node] for node in route]
                   for route in solution['routes']]
    })


@app.route('/graphs', methods=['get'])
def list_graphs():
    return jsonify({
        'graphs': [{'id': str(graph.pk),
                    'boundary': graph.boundary,
                    'nodes_count': graph.nodes.count(),
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

    try:
        osm_map_data = api.Map(args['min_longitude'], args['min_latitude'],
                               args['max_longitude'], args['max_latitude'])
    except osmapi.ApiError as e:
        return jsonify({'error': str(e)}), 400

    nodes, distances_matrix = create_graph_from_osm_map(osm_map_data)

    graph = Graph(boundary=args, distances_matrix=distances_matrix)
    graph.save()

    graph_nodes = [GraphNode(point={'type': 'Point', 'coordinates': coordinates}, graph=graph,
                             index=index) for index, coordinates in enumerate(nodes)]
    GraphNode.objects.bulk_create(graph_nodes)

    return jsonify({
        'graph_id': str(graph.pk),
    }), 201


@app.route('/graphs/<graph_id>', methods=['delete'])
def delete_graph(graph_id):
    """
    Removes graph from database.
    """
    try:
        Graph.objects.get({'_id': graph_id}).delete()
        return jsonify({'status': 'success'}), 200
    except Graph.DoesNotExist:
        return jsonify({'error': 'not found'}), 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
