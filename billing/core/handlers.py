from flask import jsonify

from billing.conversion.exceptions import MissingRate


def init_handlers(application):

    @application.errorhandler(MissingRate)
    def handle_missing_rate(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
