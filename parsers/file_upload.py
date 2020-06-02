from werkzeug.datastructures import FileStorage

upload_parser = api.parser()
upload_parser.add_argument('diagnostics_json', location='files', type=FileStorage, required=True)