from marshmallow import Schema, fields
import werkzeug
from flask_restplus import reqparse

class HWBenchmarkSchema(Schema):
    diagnostics_json = fields.Raw()
    meta_json = fields.Raw()
    sd_card_json = fields.Raw()
    latencies_bag = fields.Raw()
    meta = fields.Raw()

