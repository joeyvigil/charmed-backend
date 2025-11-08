from app.extensions import ma
from app.models import Matches


class MatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Matches

match_schema = MatchSchema() 
matches_schema = MatchSchema(many=True) 
