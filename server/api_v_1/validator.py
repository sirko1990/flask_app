import json
import os
from flask import Flask, request, abort
from functools import wraps
from jsonschema import validate, ValidationError
from neomodel import DoesNotExist

"""
    Validate resource according specification.
"""
def validate_schema(*expected_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = get_json_schema(expected_args[0])
            if request.json:
                req = request.get_json()
            else:
                bad_request("json body is required")

            if "data" not in req:
                bad_request("Data section is required")

            try:
                validate(req["data"], schema)
            except ValidationError as e:
                bad_request(e.message)

            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_404():
   def decorator(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           try:
               return func(*args, **kwargs)
           except DoesNotExist:
               abort(404, {"errors": {"code": "404", "status": "Not found"}})
       return wrapper
   return decorator



def get_schema_details(str):
    data = str.split('.')
    return {"name": data[0], "action": data[1]}

def get_json_schema(arg):
    conf = get_schema_details(arg)
    path = os.path.dirname(os.path.abspath(__file__)) + '/resourses/' + conf["name"] + '/schema.json'
    print path
    with open(path) as json_file:
        json_data = json.load(json_file)

    action = conf["action"]
    return json_data[action]

def bad_request(text):
     abort(400, {"errors": {"code": "400", "status": "Bad request", "title": text}})