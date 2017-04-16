import settings

from cached_property import cached_property
from pymodm import MongoModel, fields, connect
from pymongo import IndexModel, GEOSPHERE

connect(settings.MONGODB_URI)


class Graph(MongoModel):

    distances_matrix = fields.ListField(fields.ListField(fields.IntegerField()))
    boundary = fields.DictField()

    @cached_property
    def nodes(self):
        return GraphNode.objects.raw({'graph': self.pk})

    def get_nearest_node(self, latitude, longitude, max_distance=3000, min_distance=0):
        """

        :param latitude:
        :param longitude:
        :param max_distance:
        :param min_distance:
        :return:
        """
        return GraphNode.objects.raw(
            {
                'graph': self.pk,
                'point': {
                    '$near': {
                        '$geometry': {
                            'type': 'Point',
                            'coordinates': [latitude, longitude],
                        },
                        '$minDistance': min_distance,
                        '$maxDistance': max_distance,
                    }
                }
            }
        ).first()


class GraphNode(MongoModel):
    graph = fields.ReferenceField(Graph)
    index = fields.IntegerField()
    point = fields.PointField()

    class Meta:
        indexes = [IndexModel([('point', GEOSPHERE)])]
