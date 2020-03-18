from ..model.TournamentModel import Tournament


class TournamentService:

    def set(data):
        try:
            tournament_obj = Tournament.query.filter_by(name=data).first()
            if not tournament_obj:
                new_tournament = Tournament(
                    name=data,
                )
                new_tournament.save()
                return new_tournament
            else:
                return tournament_obj
        except Exception as e:

            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!'
            }
            return response_object