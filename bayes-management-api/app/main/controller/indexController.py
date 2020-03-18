from flask import request,  jsonify
from flask_restplus import Resource
from ..dto.index import IndexDto
from ..utility.connection import RabbitMq
from ..service.EventService import EventService
from ..utility.responseHandler import responseData
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

api = IndexDto.api

@api.route('/')
class index(Resource):
    @api.doc('Bayes home page')
    def get(self):
        """Home page"""

        server = RabbitMq()
        server.startserver()

        response_object = {
            'code': '200',
            'type': 'Response',
            'message': 'RadditMQ server started'
        }
        return jsonify(response_object)


@api.route('/list')
class list(Resource):
    @api.doc(params={'page': 'Pagination no. of page',
                     'title': 'Name of the event',
                     'tournament': 'Tournament name',
                     'state': 'State(integer)',
                     'date_start__gte': 'YYYY-MM-DD',
                     'date_start__lte': 'YYYY-MM-DD'})
    def get(self):

        args = request.args
        return responseData(EventService.list(args))

@api.route('/view/<id>')
class view(Resource):
    def get(self, id):
        return responseData(EventService.view(id))


@api.route('/search')
class search(Resource):
    @api.doc(params={'search': 'Search text',
                     'date_start__gte': 'YYYY-MM-DD',
                     'date_start__lte': 'YYYY-MM-DD'})
    def get(self):
        args = request.args
        print(args['search'])
        client = Elasticsearch('elasticsearch')

        s = Search(using=client, index="sports2")

        # Search grater than date
        if 'date_start__gte' in args and args['date_start__gte'] is not None:
            s = s.filter('range', published_from={'gte': args['date_start__gte'], 'lte': args['date_start__lte']})

        s = s.query('multi_match', fields=[ "title", "body" ], query=args['search'], type='phrase_prefix')

        response = s.execute()
        response = response.to_dict()

        response_object = {
            'code': '200',
            'type': 'No Response',
            'message': 'There is no response data to display',
            'data': response
        }
        return jsonify(response_object)