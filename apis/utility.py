"""Collection  of api utilities"""
from flask_restplus import fields
import marshmallow


def schemaToDict(schema):
    """Converts schema to dict"""
    sc_fields = schema._declared_fields
    model_info = {}
    for field_name in sc_fields:
        if not sc_fields[field_name].dump_only:
            marsh_type = type(sc_fields[field_name])
            if marsh_type == marshmallow.fields.String:
                model_info[field_name] = fields.String
            elif marsh_type == marshmallow.fields.Integer:
                model_info[field_name] = fields.Integer
            elif marsh_type == marshmallow.fields.DateTime:
                model_info[field_name] = fields.DateTime
            elif marsh_type == marshmallow.fields.Boolean:
                model_info[field_name] = fields.Boolean
            elif marsh_type == marshmallow.fields.Float:
                model_info[field_name] = fields.Float
            elif marsh_type == marshmallow.fields.Raw:
                model_info[field_name] = fields.Raw
    return model_info


queryDocumentation = {
    'where': "Filter criterion for database queries.",
    'sort': "Value by which the results are sorted by. TODO",
    'page': "Number of the resultspage to display. Per page a maximum of 25 entries are displayed.",
}
