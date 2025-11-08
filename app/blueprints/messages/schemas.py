from app.extensions import ma
from app.models import Messages


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Messages

message_schema = MessageSchema() 
messages_schema = MessageSchema(many=True) 
