"""HW Benchmark schema, will be used for Mysqldb- communication"""
from marshmallow import Schema, fields

class HWBenchmarkSchema(Schema):
    """Expected schema, WIP
    """
    diagnostics_json = fields.Raw()
    meta_json = fields.Raw()
    sd_card_json = fields.Raw()
    latencies_bag = fields.Raw()
    meta = fields.Raw()
