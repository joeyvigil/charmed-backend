from app.blueprints.users import users_bp
from .schemas import user_schema, users_schema, login_schema
from app.models import Users, Messages, Matches, db
from app.blueprints.matches.schemas import matches_schema, match_schema
from app.blueprints.messages.schemas import messages_schema, message_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Users, Messages, Matches, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required


@users_bp.route('/login', methods=['POST']) 
def login():
    try:
        data = login_schema.load(request.json) # type: ignore
        user = db.session.query(Users).where(Users.email==data['email']).first()
        
        if user and check_password_hash(user.password, data['password']): 
            token = encode_token(user.id) 
            return jsonify({
                "message": f'Hello There {user.first_name}',
                "token" : token
            }), 200
        
        return jsonify({"message": "invalid email or password"}), 401
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400


# POST '/' : Creates a new User
@users_bp.route('', methods=['POST']) 
def create_user():
    try:
        data = user_schema.load(request.json) # type: ignore
        data['password'] = generate_password_hash(data['password']) #encrypts password
        new_user = Users(**data) 
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400
    
    
# GET '/': Retrieves all Users
@users_bp.route('', methods=['GET']) 
def read_users():
    try: 
        users = db.session.query(Users).all()
        return users_schema.jsonify(users), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400
    
# GET user at id
@users_bp.route('<int:user_id>', methods=['GET'])
def read_user(user_id):
    try:
        user = db.session.get(Users, user_id)
        return user_schema.jsonify(user), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400



@users_bp.route('/profile', methods=['GET'])
@token_required
def profile():
    try:
        user_id = request.user_id # type: ignore 
        #wow, the encoded request token contains the ID for the user?
        user = db.session.get(Users, user_id)
        return user_schema.jsonify(user), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400
    
    

# Assignment
# PUT '/<int:id>':  Updates a specific User based on the id passed in through the url.
@users_bp.route('/update', methods=['PUT'])
@token_required
def update_user():
    try:
        user_id = request.user_id # type: ignore 
        print(f"updating user {user_id}")
        user = db.session.get(Users, user_id) 
        if not user: 
            return jsonify({"message": "user not found"}), 404  
        
        user_data = user_schema.load(request.json)  # type: ignore

        for key, value in user_data.items():
            if value: #blank fields will not be updated
                if key !="password":
                    # print(f"user {user} key {key} value {value}")
                    setattr(user, key, value) 
                else:
                    setattr(user, key, generate_password_hash(value)) 
                    
        db.session.commit()
        return user_schema.jsonify(user), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400




# Assignment
# DELETE '/<int:id'>: Deletes a specific User based on the id passed in through the url.
@users_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_user():
    try:
        user_id = request.user_id # type: ignore 
        print(f"deleting user {user_id}")
        user = db.session.get(Users, user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Successfully deleted user {user_id}"}), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400


# get matches for a user
@users_bp.route('/matches', methods=['GET'])
@token_required
def get_matches():
    try:
        user_id = request.user_id # type: ignore 
        matches = db.session.query(Matches).filter(
            (Matches.user1_id == user_id) | (Matches.user2_id == user_id)
        ).all()
        matches_formated = [{
            "id": match.id,
            "user1_id": match.user1_id,
            "user2_id": match.user2_id,
            "status": match.status,
            "created_at": match.created_at
        } for match in matches]
        return jsonify(matches_formated), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400
    
#get messages between user sender and receiver
@users_bp.route('/messages/<int:receiver_id>/page/<int:page>', methods=['GET'])
@token_required
def get_messages(receiver_id, page):
    try:
        sender_id = request.user_id # type: ignore 
        messages = db.session.query(Messages).filter(
            (Messages.sender_id == sender_id) & (Messages.receiver_id == receiver_id) | (Messages.receiver_id == sender_id) & (Messages.sender_id == receiver_id)
        ).order_by(Messages.created_at.desc()).limit(20).offset((page-1)*20).all()
        messages_formated = [{
            "id": message.id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "content": message.content,
            "created_at": message.created_at
        } for message in messages]

        return jsonify(messages_formated), 200
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify(str(e)), 400
    
# search for users with criteria
@users_bp.route('/search', methods=['POST'])
@token_required
def search_users():
    try:
        user_id = request.user_id # type: ignore
        user = db.session.get(Users, user_id)
        search_criteria = request.json.get("criteria", {})
        location = request.json.get("location", {})
        # search_criteria = request.json
        # example criteria: {"city": "New York", "gender": "female"}
        users = db.session.query(Users).filter_by(**search_criteria).limit(50).all()
        # sort by distance if latitude and longitude provided
        if "latitude" in location and "longitude" in location:
            print("sorting by distance")
            print("user location:", user.latitude, user.longitude)
            lat = location["latitude"]
            lon = location["longitude"]
            users.sort(key=lambda user: (user.latitude - lat)**2 + (user.longitude - lon)**2)
        return users_schema.jsonify(users), 200
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify(str(e)), 400
    
# add match with token and user id
@users_bp.route('/match/<int:other_user_id>', methods=['POST'])
@token_required
def add_match(other_user_id):
    try:
        user_id = request.user_id # type: ignore
        new_match = Matches(user1_id=user_id, user2_id=other_user_id)
        db.session.add(new_match)
        db.session.commit()
        return jsonify(match_schema.dump(new_match)), 201
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400
    
# return my matches as users
@users_bp.route('/my_matches', methods=['GET'])
@token_required
def get_my_matches():
    try:
        user_id = request.user_id # type: ignore
        matches = db.session.query(Matches).filter(
            (Matches.user1_id == user_id) | (Matches.user2_id == user_id)
        ).all()
        users = []
        for match in matches:
            if match.user1_id == user_id:
                other_user = db.session.get(Users, match.user2_id)
            else:
                other_user = db.session.get(Users, match.user1_id)
            if other_user:
                users.append(user_schema.dump(other_user))
        return jsonify(users), 200
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify(str(e)), 400