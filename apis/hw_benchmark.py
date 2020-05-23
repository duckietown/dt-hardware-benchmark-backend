from flask_restplus import Namespace, Resource
from .template import EndpointConfiguration
from .utility import queryDocumentation
from s3.upload_file import upload_file
from config import BATTERY_TYPES, BOT_TYPES
import json

from schemas.hw_benchmark import HWBenchmarkSchema


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
        upload_file("kkjkjkjj", "kjkjkjkj")
        return {'result': hw_bm_config.path.title() + ' added.'}, 201


hw_bm_meta_config = EndpointConfiguration(api, 'meta', HWBenchmarkSchema)

@api.route('/'+hw_bm_meta_config.path)
class HardwareBenchmarkFilesEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    def get(self):
        print("kjdkjdkjdkjkddk")
        result = {'bot_types': BOT_TYPES, 'battey_types': BATTERY_TYPES}
        return result
