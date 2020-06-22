"""Endpoint for Hardware Benchmark"""
from flask import make_response
from flask_restplus import Namespace, Resource
from werkzeug.datastructures import FileStorage

from schemas.hw_benchmark import HWBenchmarkSchema
from logic.process_files import process_files_request
from logic.overall_average import calc_overall_average
from logic.utils.create_plots import render_image
from files.list_files import list_files, get_file

from config import BATTERY_TYPES, BOT_TYPES, RELEASES
from .template import EndpointConfiguration


api = Namespace(
    'hw_benchmark',
    description='Request related to Hardware Benchmarks')

upload_parser = api.parser()
upload_parser.add_argument(
    'meta_json',
    location='files',
    type=FileStorage,
    required=True)
upload_parser.add_argument(
    'latencies_bag',
    location='files',
    type=FileStorage,
    required=True)
upload_parser.add_argument(
    'sd_card_json',
    location='files',
    type=FileStorage,
    required=True)
upload_parser.add_argument(
    'localization_bag',
    location='files',
    type=FileStorage,
    required=False)
upload_parser.add_argument('meta', required=True)

frontend_parser = api.parser()
frontend_parser.add_argument(
    'diagnostics_json',
    location='files',
    type=FileStorage,
    required=True)
frontend_parser.add_argument(
    'latencies_bag',
    location='files',
    type=FileStorage,
    required=True)
frontend_parser.add_argument(
    'meta_json',
    location='files',
    type=FileStorage,
    required=True)
frontend_parser.add_argument(
    'sd_card_json',
    location='files',
    type=FileStorage,
    required=True)
frontend_parser.add_argument(
    'localization_bag',
    location='files',
    type=FileStorage,
    required=False)
frontend_parser.add_argument('meta', required=True)

get_parser = api.parser()
get_parser.add_argument('page')

hw_bm_config = EndpointConfiguration(api, 'files', HWBenchmarkSchema)


@api.route('/' + hw_bm_config.path)
class HardwareBenchmarkFilesEndpoint(Resource):
    """ Endpoint for Hardware Benchmark Files
    Extends
        Resource (Restplus)
    """
    # @api.doc(params=queryDocumentation)
    @api.expect(get_parser)
    def get(self):
        """ GET-Request for uploaded files
        Returns:
            Array of files: array of the summary of all uploaded files, success
        """
        args = get_parser.parse_args()
        return list_files(args['page']), 200
        # return hw_bm_config.getRequest()

    @api.expect(frontend_parser)
    def post(self):
        """POST-Request to upload every file used for the BM
        Returns:
            dict: resulkt and corresponding uuid
        """
        args = frontend_parser.parse_args()
        uuid = process_files_request(args)
        return {'result': hw_bm_config.path.title() + ' added as' + str(uuid), 'uuid': str(uuid)}, 201


@api.route('/' + hw_bm_config.path + '/<hw_bm_file_key>')
class HardwareBenchmarkFilesEndpointFromDiagnostics(Resource):
    """ Endpoint for Hardware Benchmark Files retrieving the data from the Diagnostics API
    Extends
        Resource (Restplus)
    """
    @api.expect(upload_parser)
    def post(self, hw_bm_file_key):
        """POST-Request to upload every file used for the BM
        Returns:
            dict: result and corresponding uuid
        """
        args = upload_parser.parse_args()
        uuid = process_files_request(args, hw_bm_file_key)
        return {'result': hw_bm_config.path.title() + ' added as' + str(uuid), 'uuid': str(uuid)}, 201



@api.route('/' + hw_bm_config.path + '/<uuid>')
class HardwareBenchmarkFilesEndpointById(Resource):
    """ Endpoint for Hardware Benchmark Files specified by bm_uuid
    Extends
        Resource (Restplus)
    """
    def get(self, uuid):
        """ GET-Request for uploaded files by uuid
        Returns:
            Corresponding dict
        """
        res = get_file('meas/' + uuid + '.json')
        return res, 200


@api.route('/' + hw_bm_config.path + '/<uuid>.png')
class HardwareBenchmarkImagesEndpointById(Resource):
    """ Endpoint for Hardware Benchmark Images
    Extends
        Resource (Restplus)
    """
    def get(self, uuid):
        """ GET-Request for BM matplotlib images
        Returns:
            Images generated by matplotlib
        """
        res = make_response(render_image(uuid))
        res.headers['Content-Type'] = 'image/png'

        return res

hw_bm_score_config = EndpointConfiguration(api, 'score', HWBenchmarkSchema)
@api.route('/' + hw_bm_score_config.path)
class HardwareBenchmarkScoreEndpoint(Resource):
    """ Endpoint for Hardware Benchmark overall Score
    Extends
        Resource (Restplus)
    """
    def get(self):
        """ GET-Request for BM-Overall Score
        Returns:
            score of average over all bm scores
        """
        return calc_overall_average(), 200

hw_bm_meta_config = EndpointConfiguration(api, 'meta', HWBenchmarkSchema)
@api.route('/' + hw_bm_meta_config.path)
class HardwareBenchmarkMetaEndpoint(Resource):
    """ Endpoint for Hardware Benchmark Meta
    Extends
        Resource (Restplus)
    """
    def get(self):
        """ GET-Request for BM-Meta
        Returns:
            Meta for e.g. dropdown
        """
        result = {'dropdowns': [{'name': 'Bot Types',
                                 'key': 'bot_type',
                                 'content': BOT_TYPES},
                                {'name': 'Battery Types',
                                 'key': 'battery_type',
                                 'content': BATTERY_TYPES},
                                {'name': 'Releases',
                                 'key': 'release',
                                 'content': RELEASES}]}
        return result, 200
