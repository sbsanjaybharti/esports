import logging
import pika
import ast

import json
from collections import namedtuple
from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from ..service.EventService import EventService

from ..config import Config as config


class RabbitMq():

    def __init__(self):
        """ Configure Rabbit Mq Server  """
        # logging.basicConfig(level=logging.INFO)
        credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
        parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=config.RABBITMQ_QUEUE)

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        response = EventService.set(data['data'], data['source'])

        ##################################################################
        # # Add data to ElasticSearch
        ##################################################################
        # connections.create_connection(hosts=['elasticsearch'])
        # ElasticSearchConfig.init()
        # print(response['data']['title'])
        # print(response['data']['id'])
        # post = ElasticSearchConfig(meta={'id': response['data']['id']}, title=response['data']['title'], tags=[response['data']['tags']])
        # post.body = json.dumps(response['data']['body'])
        # post.published_from = datetime.now()
        # post.save()

    def publish(self, payload={}):
        """
        :param payload: JSON payload
        :return: None
        """

        self._channel.basic_publish(exchange=config.RABBITMQ_EXCHANGE,
                                    routing_key=config.RABBITMQ_ROUTINGKEY,
                                    body=str(payload))

        print("Published Message: {}".format(payload))
        self._connection.close()

    def startserver(self):
        self._channel.basic_consume(
            queue=config.RABBITMQ_QUEUE,
            on_message_callback=self.callback,
            auto_ack=True)
        self._channel.start_consuming()


class ElasticSearchConfig(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Index:
        name = 'sports'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(ElasticSearchConfig, self).save(** kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from

# class ElasticData(object):
#
#     def __init__(self, id, title, body, tags):
#         self.id = id
#         self.title = title
#         self.body = body
#         self.tags = tags
#
#     def set(self):
#
#         ElasticSearch.init()
#         post = ElasticSearch(meta={'id': self.id}, title=self.title, tags=self.tags)
#         post.body = self.body
#         post.published_from = datetime.now()
#         post.save()
