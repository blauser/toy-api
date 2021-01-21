"""
This is the simple API to determine if a property has a septic system.
"""
from typing import Optional, Tuple
from flask import Flask
from flask_restful import Resource, Api, reqparse
import propsapi.sources.hcapi as hc

app = Flask(__name__)
api = Api(app)

API_VERSION = 'v0'


class Props(Resource):
    """Handles the /props endpoint of our API."""

    @staticmethod
    def get() -> Tuple[dict, int]:
        """Handles the GET request method of the /props endpoint."""
        parser = reqparse.RequestParser()
        parser.add_argument('address', required=True)
        args = parser.parse_args()

        sewer, error = hc.get_sewer(args['address'])

        if error:
            return Props.error_response(error), 200
        else:
            return Props.success_response(sewer), 200

    @staticmethod
    def props_url() -> str:
        """Returns the url for the /props endpoint."""
        return '/' + API_VERSION + '/props'

    @staticmethod
    def error_response(error: str) -> dict:
        """Builds error response for the /props endpoint."""
        return {'props': dict(api_result='error', error=error)}

    @staticmethod
    def success_response(sewer: Optional[str]) -> dict:
        """Builds success response for the /props endpoint."""
        return {'props': dict(api_result='success', sewer=Props.is_septic(sewer))}

    @staticmethod
    def is_septic(sewer: Optional[str]) -> str:
        """Determines if the sewer type is a septic system (yes, no, or unknown)."""
        if sewer == 'septic':
            return 'yes'
        elif sewer in (None, 'yes'):
            return 'unknown'
        else:
            return 'no'


api.add_resource(Props, Props.props_url())
