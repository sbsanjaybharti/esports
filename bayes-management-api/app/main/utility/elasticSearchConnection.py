from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text


class ElasticSearchConfig(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Index:
        name = 'sports2'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(ElasticSearchConfig, self).save(** kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from