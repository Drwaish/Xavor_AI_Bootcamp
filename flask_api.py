"""
Main module of flask API.
"""
# Third party modules
import os
from typing import Any
from functools import wraps
from dotenv import load_dotenv

import pandas as pd
from flask import (
    Flask, request,
    json, make_response, Response
)
from flask_cors import CORS, cross_origin
from asgiref.wsgi import WsgiToAsgi

from llm_prompt import create_llm_chain
from prompting import prompt_maker


# Module
app = Flask(__name__)
cors = CORS(app)
#asgi_app = WsgiToAsgi(app)
api_cors = {
  "origins": ["*"],
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Content-Type"]
}
#app.config['PROPAGATE_EXCEPTIONS'] = True
CHAIN = create_llm_chain()

def authorize(token: str)-> bool:
    """
    method take header token as input and check valid ot not.

    Parameters:
    ----------
    toekn: str 
        token pass by the user in header.

    Return:
    ------
        return True if the toekn is valid otherwise return False.

    """
    load_dotenv()
    my_key = os.getenv('api-key')
    if token != my_key:
        return True
    return False

def token_required(func: Any)-> Any:
    """
    method token required will perform the authentication based on taoken.

    Parameters:
    ----------
    func: Any
        arguement ass to the function from request header.

    Return:
    ------
        return the the response of the token authentication.

    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'api-key' in request.headers:
            token = request.headers['api-key']
        if not token:
            result = make_response(json.dumps(
            {'message'  : 'Token Missing',
            'category' : 'Authorization error',}),
            401)
            return result
        if authorize(token):
            result = make_response(
            json.dumps(
            {'message'  : 'UnAuthorized',
            'category' : 'Authorization error',}),
            401)
            return result
        return func(*args, **kwargs)
    return decorated


def validate_text_request(request_api: Any)-> bool:
    """
    Method will take a json request and perform all validations if the any error 
    found then return error response with status code if data is correct then 
    return data in a list.

    Parameters
    ----------
    request_api: Request
        contain the request data in file format.

    Return
    ------
    bool
        return True or False.

    """
    data = request_api.get_json()
    if "name_space" in data:
        if data["name_space"] == '':
            return False
    else: 
        return False
    if "description" in data:
        if data["description"] == '':
            return False
    else:
        return False
    if 'body_vitals' in data:
        if data["body_vitals"] == '':
            return False
    else:    
        return False
    return True
    


def make_bad_params_value_response()-> Response:
    """
    Method will make a error response a return it back.

    Parameters:
    ----------
    None

    Return:
    ------
    Response
        return a response message.

    """
    result = make_response(json.dumps(
        {'message'  : 'data key error',
        'category' : 'Bad Params',}),
        400)
    return result


@app.route('/query', methods=['POST'])
@cross_origin(**api_cors)
def create_answer():
    """
    Method will take the text as input and return the response generated
    by the openai.

    Parameters:
    ----------
    None

    Return:
    ------
    str
        return the response.

    """
    try:
        if request.method == "POST":
            if token_required(request):
                if validate_text_request(request_api=request):
                    data = request.get_json()
                    name_space = data['name_space']
                    description = data['description']
                    history = data['history']
                    body_vitals = data['body_vitals']
                    query = f'History : \n {history} \n Description : \n {description} \n Body Vitals :\n {body_vitals}'
                    prompt_query = prompt_maker(query=query, name_space=name_space)
                    response = CHAIN.run(prompt_query)
                    result = make_response(json.dumps({
                        'message': eval(response),
                        'Status': 'OK',
                    }), 200)
                    return result
                else:
                    return make_bad_params_value_response()
            else:
                result = make_response(json.dumps({
                    'message': 'Invalid Request',
                    'Status': 'Bad',
                }), 401)
                return result
        else:
            result = make_response(json.dumps({
                    'message': 'Invalid HTTPS Method',
                    'Status': 'Bad',
                }), 405)
            return result
    except Exception as exception:
        result = make_response(json.dumps({
            'message': str(exception),
            'category': 'Internal server error',
        }), 500)
        return result


if __name__=='__main__':
    app.run(debug = True, host="0.0.0.0", port = 5000)