from flask import make_response
from flask_restplus import Namespace, Resource
from .template import EndpointConfiguration
from .utility import queryDocumentation
from config import BATTERY_TYPES, BOT_TYPES, RELEASES
import json

from schemas.hw_benchmark import HWBenchmarkSchema
from werkzeug.datastructures import FileStorage

from logic.process_files import process_files_request
from logic.utils.create_plots import render_image
from s3.list_files import list_files, get_file



api = Namespace('hw_benchmark', description='Request related to Hardware Benchmarks')

upload_parser = api.parser()
upload_parser.add_argument('diagnostics_json', location='files', type=FileStorage, required=True)
upload_parser.add_argument('latencies_bag', location='files', type=FileStorage, required=True)
upload_parser.add_argument('meta_json', location='files', type=FileStorage, required=True)
upload_parser.add_argument('sd_card_json', location='files', type=FileStorage, required=True)
upload_parser.add_argument('meta', required=True)

get_parser = api.parser()
get_parser.add_argument('page')

hw_bm_config = EndpointConfiguration(api, 'files', HWBenchmarkSchema)
@api.route('/'+hw_bm_config.path)
class HardwareBenchmarkFilesEndpoint(Resource):
    #@api.doc(params=queryDocumentation)
    @api.expect(get_parser)
    def get(self):
        args = get_parser.parse_args()
        return list_files(args['page']), 200
        #return hw_bm_config.getRequest()

    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        process_files_request(args)
        return {'result': hw_bm_config.path.title() + ' added.'}, 201

@api.route('/'+hw_bm_config.path+'/<id>')
class HardwareBenchmarkFilesEndpointById(Resource):
    def get(self, id):
        res = get_file('meas/'+id+'.json')
        return res, 200

@api.route('/'+hw_bm_config.path+'/<id>.png')
class HardwareBenchmarkImagesEndpointById(Resource):
    def get(self, id):

        res = make_response(render_image(id))        
        res.headers['Content-Type'] = 'image/png'

        return res

hw_bm_meta_config = EndpointConfiguration(api, 'meta', HWBenchmarkSchema)
@api.route('/'+hw_bm_meta_config.path)
class HardwareBenchmarkFilesEndpoint(Resource):
    def get(self):
        result = {'dropdowns': [{'name': 'Bot Types', 'key':'bot_type','content': BOT_TYPES}, 
                                {'name': 'Battery Types', 'key':'battery_type', 'content': BATTERY_TYPES}, 
                                {'name': 'Releases', 'key':'release', 'content': RELEASES}]}
        return result, 200
