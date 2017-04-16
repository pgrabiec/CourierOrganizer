from collections import Counter


OSM_CAR_ROADS = ('motorway', 'trunk', 'primary', 'secondary', 'tertiary',
                 'unclassified', 'residential',  'service', 'motorway_link',
                 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link',
                 'living_street')


def create_graph_from_osm_map(map_data):
    """
    Solution based on:
    https://help.openstreetmap.org/questions/19213/how-can-i-convert-an-osm-xml-file-into-a-graph-representation
    """
    node_counts = Counter()
    nodes_set = set()

    map_nodes = [element for element in map_data if element['type'] == 'node']
    map_roads = [element for element in map_data if element['type'] == 'way'
                 and 'highway' in element['data']['tag']
                 and element['data']['tag']['highway'] in OSM_CAR_ROADS]

    for way in map_roads:
        way_nodes = way['data']['nd']
        node_counts.update(way_nodes)
        nodes_set.add(way_nodes[0])  # add edges of the road
        nodes_set.add(way_nodes[-1])

    nodes_set = nodes_set.union({node for node, count in node_counts.items() if count > 1})
    nodes = [{'type': 'Point', 'coordinates': (node['data']['lat'], node['data']['lon'])}
             for node in map_nodes if node['data']['id'] in nodes_set]  # GeoPoint format

    # TODO: replace mock, calculate distances_matrix properly
    distances_matrix = [[] for _ in range(len(nodes))]
    for row in distances_matrix:
        for _ in range(len(nodes)):
            row.append(1)

    return nodes, distances_matrix
