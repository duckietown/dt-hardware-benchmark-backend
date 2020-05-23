from .query_parser import queryParser
from .utility import schemaToDict
from math import ceil

class EndpointConfiguration: #Authorization to  be done here
    def __init__(self, api, path, schema):
        self.api = api
        self.path = path
        self.model = api.model(path.title(), schemaToDict(schema))

    def getRequest(self):
        args = queryParser()
        res = self.getSerializedResponse(**args)
        return res, 200

    def postRequest(self):
        return {'result': self.path.title() + ' added.'}, 201

    def getSerializedResponse(self, page = 1, sort = None, perPage = 25, where = True):
        items = []
        totalResults = 200
        resultsOnPage = 25
        for result in ['1', '2', '3']:
            items.append(result)
        
        response = {'items': items}
        lastPage = ceil(totalResults/perPage)
        response['meta'] = {'page': page, 'last_page': lastPage, 'results_on_this_page': resultsOnPage, 'max_results_per_page': perPage, 'total_results': totalResults}
        return response
