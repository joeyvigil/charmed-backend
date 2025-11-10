from app.blueprints.messages import messages_bp
from .schemas import message_schema, messages_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Messages, Users, Matches, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required



# Assignment
# POST '/' : Creates a new Message
@messages_bp.route('', methods=['POST']) 
def create_message():
    try:
        # data = message_schema.load(request.json) # type: ignore
        data = request.json
        new_message = Messages(**data) # type: ignore
        db.session.add(new_message)
        db.session.commit()
        return message_schema.jsonify(new_message), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400

# Assignment
# GET '/': Retrieves all Messages
@messages_bp.route('', methods=['GET']) 
def read_messages():
    try: 
        messages = db.session.query(Messages).all()
        return messages_schema.jsonify(messages), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400



# GET at id
@messages_bp.route('<int:message_id>', methods=['GET'])
def read_message(message_id):
    try:
        message = db.session.get(Messages, message_id)
        return message_schema.jsonify(message), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400

# Assignment
# DELETE '/<int:id'>: Deletes a specific Message based on the id passed in through the url.
@messages_bp.route('<int:message_id>', methods=['DELETE'])
# @token_required
def delete_message(message_id):
    try:
        message = db.session.get(Messages, message_id)
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": f"Successfully deleted message {message_id}"}), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400

# Assignment
# PUT '/<int:id>':  Updates a specific Message based on the id passed in through the url.
@messages_bp.route('<int:message_id>', methods=['PUT'])
# @token_required
def update_message(message_id):
    try:
        message = db.session.get(Messages, message_id) 
        if not message: 
            return jsonify({"message": "message not found"}), 404  
        
        # message_data = message_schema.load(request.json)  # type: ignore
        message_data = request.json 
        for key, value in message_data.items():   # type: ignore
            if value: #blank fields will not be updated
                if key !="password":
                    # print(f"message {message} key {key} value {value}")
                    setattr(message, key, value) 
                else:
                    setattr(message, key, generate_password_hash(value)) 
                    
        db.session.commit()
        return message_schema.jsonify(message), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400
    