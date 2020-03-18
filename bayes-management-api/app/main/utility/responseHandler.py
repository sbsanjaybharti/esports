import linecache
import sys

from flask import jsonify, Flask
from flask import Flask, request, jsonify, make_response

def getException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def responseData(data):
    try:
        if not data:
            response_object = {
                'code': '444',
                'type': 'No Response',
                'message': 'There is no response data to display'
            }
            return jsonify(response_object), 444
        else:
            response = data
            return make_response(jsonify(response), response['code'])

    except Exception as e:
        response_object = {
            'code': '500',
            'type': 'Internal Server Error',
            'message': 'The server encountered an unexpected condition which prevented it from fulfilling the request',
            'exception': getException()
        }
        return jsonify(response_object), 500