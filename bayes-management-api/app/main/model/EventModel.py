from .. import db, flask_bcrypt
import uuid
import datetime
from .TournamentModel import Tournament
# from .ScoreModel import Score
from elasticsearch_dsl.connections import connections
from ..utility.elasticSearchConnection import ElasticSearchConfig


# Define the UserRoles association table
class Event(db.Model):
    __tablename__ = 'events'

    # id = db.Column(db.Integer(), primary_key=True)
    id = db.Column(db.String(100), primary_key=True, autoincrement=False, unique=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(100), index=True)
    source = db.Column(db.String(500), index=True)
    url = db.Column(db.String(500), index=True)

    def save(self):
        db.session.add(self)
        db.session.commit()


# Define the UserRoles association table
class EventState(db.Model):
    __tablename__ = 'event_state'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.String(100), db.ForeignKey('events.id', ondelete='CASCADE'))
    event = db.relationship(Event, backref=db.backref('events'))
    tournament_id = db.Column(db.Integer(), nullable=True)
    tournament_rel_id = db.Column(db.Integer(), db.ForeignKey('tournament.id', ondelete='CASCADE'))
    tournament = db.relationship(Tournament, backref=db.backref('tournament'))
    bestof = db.Column(db.Integer())
    state = db.Column(db.Integer())
    date_start_text = db.Column(db.DateTime, nullable=True)

    def storeSearch(self):
        connections.create_connection(hosts=['elasticsearch'])
        ElasticSearchConfig.init()

        post = ElasticSearchConfig(meta={'id': self.id}, title=self.event.title,
                                   tags=[self.event.title])
        post.body = self.event.title + ' ' +self.tournament.name
        post.published_from = self.date_start_text
        post.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
