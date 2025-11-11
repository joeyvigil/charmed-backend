from app.extensions import ma
from app.models import Users


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_fk=True

user_schema = UserSchema() 
users_schema = UserSchema(many=True) 
login_schema = UserSchema(exclude=['id', 'role', 'first_name', 'last_name', 'gender', 'birthdate', 'in_game_name', 'tagline', 'bio', 'city', 'state', 'country', 'created_at', 'latitude', 'longitude'])