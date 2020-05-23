from marshmallow import Schema, fields
import werkzeug
from flask_restplus import reqparse

class HWBenchmarkSchema(Schema):
    hw_benchmark_uuid = fields.UUID(dump_only = True)
    diagnostics = fields.Raw()
    meta = fields.Raw()
    sdCard = fields.Raw()
    bot_bag = fields.Raw()

