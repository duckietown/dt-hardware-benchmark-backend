"""Template on which the all apis base"""
from math import ceil
from .utility import schemaToDict

class EndpointConfiguration:
    """Base Endpoint Configuration Auth could be done in here"""
    def __init__(self, api, path, schema):
        self.api = api
        self.path = path
        self.model = api.model(path.title(), schemaToDict(schema))

    def get_serialized_response(self, page=1, per_page=25):
        """ Not used yet. Idea: use for pageination if more than 25 results are around

        Args:
            page (int, optional): requested-page. Defaults to 1.
            per_page (int, optional): amount-page. Defaults to 25.

        Returns:
            [type]: [description]
        """
        items = []
        total_results = 200
        results_on_page = 25
        for result in ['1', '2', '3']:
            items.append(result)

        response = {'items': items}
        last_page = ceil(total_results / per_page)
        response['meta'] = {
            'page': page,
            'last_page': last_page,
            'results_on_this_page': results_on_page,
            'max_results_per_page': per_page,
            'total_results': total_results}
        return response
