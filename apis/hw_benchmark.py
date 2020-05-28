from flask_restplus import Namespace, Resource
from .template import EndpointConfiguration
from .utility import queryDocumentation
from s3.upload_file import upload_file
from config import BATTERY_TYPES, BOT_TYPES, RELEASES
import json

from schemas.hw_benchmark import HWBenchmarkSchema
from logic.process_files import process_files_request


api = Namespace('hw_benchmark', description='Request related to Hardware Benchmarks')
hw_bm_config = EndpointConfiguration(api, 'files', HWBenchmarkSchema)

@api.route('/'+hw_bm_config.path)
class HardwareBenchmarkFilesEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    def get(self):
        print("kjdkjdkjdkjkddk")
        #return hw_bm_config.getRequest()

    @api.expect(hw_bm_config.model)
    def post(self):
        print(api.payload)
        process_files_request(api.payload)
        return {'result': hw_bm_config.path.title() + ' added.'}, 201


hw_bm_meta_config = EndpointConfiguration(api, 'meta', HWBenchmarkSchema)

@api.route('/'+hw_bm_meta_config.path)
class HardwareBenchmarkFilesEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    def get(self):
        result = {'dropdowns': [{'name': 'Bot Types', 'key':'bot_type','content': BOT_TYPES}, 
                                {'name': 'Battery Types', 'key':'battery_type', 'content': BATTERY_TYPES}, 
                                {'name': 'Releases', 'key':'releases', 'content': RELEASES}]}
        return result
