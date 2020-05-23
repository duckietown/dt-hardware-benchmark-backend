from flask_restplus import Api

from .hw_benchmark import api as hw_benchmark

authorizations = {
	'duckietown-token' :{
		'type': 'apiKey',
		'in': 'header',
		'name': 'X-DUCKIETOWN-TOKEN'
	}
}

api = Api(
    title='benchmark API',
    version='0.1',
    description='Benchmark API',
    authorizations=authorizations,
    # All API metadatas
)

api.add_namespace(hw_benchmark)
