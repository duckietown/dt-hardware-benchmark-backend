from flask_restplus import fields
import marshmallow

def schemaToDict(schema):
	sc_fields = schema._declared_fields
	modelInfo = {}
	for field_name in sc_fields:
		if not sc_fields[field_name].dump_only:
			marshType = type(sc_fields[field_name])
			if marshType == marshmallow.fields.String:
				modelInfo[field_name] = fields.String
			elif marshType == marshmallow.fields.Integer:
				modelInfo[field_name] = fields.Integer
			elif marshType == marshmallow.fields.DateTime:
				modelInfo[field_name] = fields.DateTime
			elif marshType == marshmallow.fields.Boolean:
				modelInfo[field_name] = fields.Boolean
			elif marshType == marshmallow.fields.Float:
				modelInfo[field_name] = fields.Float
			elif marshType == marshmallow.fields.Raw:
				modelInfo[field_name] = fields.Raw
	return modelInfo


queryDocumentation = {
    'where': "Filter criterion for database queries.",
    'sort': "Value by which the results are sorted by. TODO",
    'page': "Number of the resultspage to display. Per page a maximum of 25 entries are displayed.",
}
