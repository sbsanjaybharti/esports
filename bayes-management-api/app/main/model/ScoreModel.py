from .. import db
import uuid
from .TeamModel import Team
from .EventModel import EventState


class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.String(100), primary_key=True, autoincrement=False, unique=True, default=str(uuid.uuid4()))
    event_state_id = db.Column(db.Integer(), db.ForeignKey('event_state.id', ondelete='CASCADE'))
    event_state = db.relationship(EventState, backref=db.backref('event_state'))
    team_id = db.Column(db.Integer(), nullable=True)
    team_rel_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))
    team = db.relationship(Team, backref=db.backref('teams'))

    score = db.Column(db.Integer(), nullable=True)
    winner = db.Column(db.Boolean, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
