import datetime

from app.main import db
from flask import current_app
from ..model.EventModel import Event, EventState
from ..model.TournamentModel import Tournament
from ..service.TournamentService import TournamentService
from ..service.TeamService import TeamService
from ..service.ScoreService import ScoreService
from ..utility.responseHandler import getException
class EventService:

    def set(data, source):
        try:
            print('es_1')

            event_obj = Event.query.filter_by(id=data['id']).first()

            if not event_obj:
                new_event = Event(
                    id=data['id'],
                    title=data['title'],
                    source=source,
                    url=data['url']
                )
                new_event.save()
            else:
                new_event = event_obj
            new_event.save()

            if isinstance(data['tournament'], dict):
                tournament = data['tournament']['name']
                new_eventState = EventState(
                    event=new_event,
                    tournament_id=data['tournament']['id'],
                    tournament=TournamentService.set(tournament),
                    bestof=data['bestof'],
                    state=data['state'],
                    date_start_text=data['date_start_text'],
                )
            else:
                tournament = data['tournament']
                new_eventState = EventState(
                    event=new_event,
                    tournament=TournamentService.set(tournament),
                    bestof=data['bestof'],
                    state=data['state'],
                    date_start_text=data['date_start_text'],
                )
            new_eventState.save()
            team = TeamService.set(data['teams'])
            score = ScoreService.set(data['scores'], team, new_eventState)
            new_eventState.storeSearch()
            print('ss')
            response_object = {
                'code': 200,
                'type': 'Success',
                'message': 'Successfully registered!',
                'data': {
                    'id': new_event,
                    'title': data['title'],
                    'body': {'tournament': tournament, 'team': team, 'scores': data['scores']},
                    'tags': tournament
                }
            }
            return response_object
        except Exception as e:
            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!'
            }
            return response_object

    def list(args):

        try:
            if 'page' in args and args['page'] is not None:
                page = args['page']
            else:
                page = 1
            # Search default
            match_list = EventState.query

            # Search state
            if 'state' in args and args['state'] is not None:
                state_int = str(args['state']).lower().strip()
                match_list = match_list.filter_by(state=state_int)

            # Search grater than date
            if 'date_start__gte' in args and args['date_start__gte'] is not None:
                date_start__gte = args['date_start__gte']
                match_list = match_list.filter(EventState.date_start_text >= date_start__gte)

            # Search less than date
            if 'date_start__lte' in args and args['date_start__lte'] is not None:
                date_start__lte = args['date_start__lte']
                match_list = match_list.filter(EventState.date_start_text <= date_start__lte)

            # Search title
            if 'title' in args and args['title'] is not None:
                title_str = str(args['title']).lower().strip()
                title_str = "%" + title_str + "%"
                match_list = match_list.join(Event).filter(Event.title.like(title_str))

            # Search tournament
            if 'tournament' in args and args['tournament'] is not None:
                tournament_str = str(args['tournament']).lower().strip()
                tournament_str = "%" + tournament_str + "%"
                match_list = match_list.join(Tournament).filter(Tournament.name.like(tournament_str))

            match_list = match_list.paginate(int(page), per_page=current_app.config['DATA_PERPAGE'])

            if match_list:
                result = [
                    {
                        'id': match.id,
                        'title': match.event.title,
                        'tournament': match.tournament.name,
                        'bestof': match.bestof,
                        'state': match.state,
                        'date': match.date_start_text,
                        'score': ScoreService.getScore(match.id)
                    } for match in match_list.items]

                response_object = {
                    'code': 200,
                    'type': 'Success',
                    'message': 'Task found',
                    'data': result,
                    'paginate': {
                        'pages': match_list.pages,
                        'page': match_list.page,
                        'per_page': match_list.per_page,
                        'total': match_list.total,
                        'prev_num': match_list.prev_num,
                        'next_num': match_list.next_num,
                        'has_prev': match_list.has_prev,
                        'has_next': match_list.has_next
                    }
                }
                return response_object
            else:
                response_object = {
                    'code': 404,
                    'type': 'Not Found',
                    'message': 'Match Not Found!'
                }
                return response_object
        except Exception as e:
            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!',
                'exception': getException()
            }
            return response_object

    def view(id):

        try:
            match = EventState.query.filter_by(id=id).first()

            if match:
                result = {
                    'id': match.id,
                    'title': match.event.title,
                    'tournament': match.tournament.name,
                    'bestof': match.bestof,
                    'state': match.state,
                    'score': ScoreService.getScore(match.id)
                }

                response_object = {
                    'code': 200,
                    'type': 'Success',
                    'message': 'Task found',
                    'data': result
                }
                return response_object
            else:
                response_object = {
                    'code': 404,
                    'type': 'Not Found',
                    'message': 'Match Not Found!'
                }
                return response_object
        except Exception as e:
            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!',
                'exception': getException()
            }
            return response_object
