from pymodm import MongoModel, fields
from pymodm.errors import ValidationError


class Graph(MongoModel):

    nodes = fields.ListField(fields.PointField())
    distances_matrix = fields.ListField(fields.ListField(fields.IntegerField()))
    boundary = fields.DictField()

    def clean(self):
        nodes_count = len(self.nodes)

        if (nodes_count != len(self.distances_matrix)
                and nodes_count != len(self.distances_matrix[0])):
            raise ValidationError('Invalid size of distances matrix')
