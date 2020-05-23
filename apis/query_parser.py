from flask import request
from flask_restplus import abort
from marshmallow import Schema, fields

class QuerySchema(Schema):
    where = fields.Str()
    sort = fields.Str()
    page = fields.Int()


def queryParser():
    arguments = request.args.to_dict()
    schema = QuerySchema()
    query = schema.load(arguments)[0]
    args = {}
    if 'page' in query:
        args['page'] = query['page']

    return args
