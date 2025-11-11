from app.extensions import ma
from app.models import Matches


class MatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Matches
        include_fk=True
        # load_instance = True

match_schema = MatchSchema() 
matches_schema = MatchSchema(many=True) 
