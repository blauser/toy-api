import propsapi.sources.housecanary as hc
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


class Props(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', required=True)
        args = parser.parse_args()

        sewer, error = hc.get_sewer(args['address'])

        if error:
            return {'error': error}
        else:
            return {'septic': is_septic(sewer)}, 200


def is_septic(sewer):
    if sewer == 'septic':
        return 'yes'
    elif sewer in (None, 'yes'):
        return 'unknown'
    else:
        return 'no'


api.add_resource(Props, '/props')
