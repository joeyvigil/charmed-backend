from app.extensions import ma
from app.models import Messages


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Messages
        include_fk=True

message_schema = MessageSchema() 
messages_schema = MessageSchema(many=True) 
