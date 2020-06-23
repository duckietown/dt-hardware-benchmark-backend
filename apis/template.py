"""Template on which the all apis base"""
from .utility import schema_to_dict


class EndpointConfiguration:
    """Base Endpoint Configuration Auth could be done in here"""

    def __init__(self, api, path, schema):
        self.api = api
        self.path = path
        self.model = api.model(path.title(), schema_to_dict(schema))
