import uuid
from ..model.ScoreModel import Score


class ScoreService:

    def set(data, team, event_state):

        try:
            for row in data:
                id = str(uuid.uuid4())
                key = int(row['team'])
                new_score = Score(
                    id=id,
                    event_state=event_state,
                    team_id=row['team'],
                    team=team[key],
                    score=row['score'],
                    winner=row['winner']
                )
                new_score.save()
        except Exception as e:

            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!',
            }
            return response_object

    def getScore(match_id):
        team_score = Score.query.filter_by(event_state_id=match_id)

        if team_score:
            result = [
                {
                    'team': score.team.name,
                    'score': score.score,
                    'winner': score.winner,
                } for score in team_score]
            return result
        return None
