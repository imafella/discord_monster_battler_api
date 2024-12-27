import json
import os
from datetime import datetime
from flask import Response

response_format = os.environ.get('response_format', 'application/json')


def obj_to_dict(obj=None):
    if obj is None:
        obj = {}
    return json.dumps(obj.__dict__)


def generate_id(header):
    return datetime.now().strftime(f'{header}-%Y%m%d%H%M%S')


def response_formatter(body: dict, status: int):
    return Response(json.dumps(body), status=status, mimetype=response_format, content_type=response_format)
