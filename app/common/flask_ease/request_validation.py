from flask_restful import reqparse, abort
from flask import request


def validate_request(*req_elements):
    try:
        details_args = reqparse.RequestParser()
        for elements in req_elements:
            details_args.add_argument(f"{elements}", type=str, help=f"{elements} is required", required=True)
        det = details_args.parse_args()
        return det
    except Exception as e:
        abort(400, message="Something went wrong in request validation...")
        raise


def validate_apiKey():
    key = request.headers.get('api_key')
    if key is not None:
        return True
    else:
        return False
