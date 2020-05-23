from flask_restplus import Namespace, Resource
from .template import EndpointConfiguration
from .utility import queryDocumentation

from schemas.hw_benchmark import HWBenchmarkSchema


api = Namespace('HWbenchmark', description='Request related to Hardware Benchmarks')
hw_bm_config = EndpointConfiguration(api, 'hw_bm', HWBenchmarkSchema)

@api.route('/'+hw_bm_config.path)
class InvoiceEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    def get(self):
        return hw_bm_config.getRequest()

    @api.expect(hw_bm_config.model)
    def post(self):
        return hw_bm_config.postRequest()

