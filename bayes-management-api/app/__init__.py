# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.indexController import api as index

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API for Bayes-eSports',
          version='1.0',
          description='Api in flask to complete code challenge for Bayes-eSports'
          )

api.add_namespace(index, path='/index')