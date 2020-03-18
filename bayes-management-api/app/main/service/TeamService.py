from ..model.TeamModel import Team


class TeamService:

    def set(data):
        team ={}
        try:
            for row in data:
                team_obj = Team.query.filter_by(name=row['name']).first()
                if not team_obj:
                    new_team = Team(
                        name=row['name'],
                    )
                    new_team.save()
                    team[int(row['id'])] = new_team
                else:
                    team[int(row['id'])] = team_obj
            return team
        except Exception as e:

            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!'
            }
            return response_object