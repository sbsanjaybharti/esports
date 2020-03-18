from flask_restplus import Namespace, fields


class IndexDto:
    api = Namespace('Index', description='index is the home page of application')