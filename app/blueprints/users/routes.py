from app.blueprints.users import users_bp
from .schemas import user_schema, users_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Users, Messages, Matches, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required



# @users_bp.route('/login', methods=['POST']) 
# def login():
#     try:
#         data = login_schema.load(request.json) # type: ignore
#         user = db.session.query(Users).where(Users.email==data['email']).first()
        
#         if user and check_password_hash(user.password, data['password']): 
#             token = encode_token(user.id) 
#             return jsonify({
#                 "message": f'Hello There {user.first_name}',
#                 "token" : token
#             }), 200
        
#         return jsonify({"message": "invalid email or password"}), 401
#     except ValidationError as e:
#         return jsonify(e.messages), 400 
#     except Exception as e:
#         return jsonify(str(e)), 400


# Assignment
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

# # Assignment
# # GET '/': Retrieves all Users
# @users_bp.route('', methods=['GET']) 
# def read_users():
#     try: 
#         users = db.session.query(Users).all()
#         return users_schema.jsonify(users), 200
#     except ValidationError as e:
#         return jsonify({"ValidationError": e.messages}), 400
#     except Exception as e:
#         return jsonify({"Exception": str(e)}), 400


# @users_bp.route('/profile', methods=['GET'])
# @token_required
# def read_user():
#     try:
#         user_id = request.user_id # type: ignore 
#         #wow, the encoded request token contains the ID for the user?
#         user = db.session.get(Users, user_id)
#         return user_schema.jsonify(user), 200
#     except ValidationError as e:
#         return jsonify(e.messages), 400 
#     except Exception as e:
#         return jsonify(str(e)), 400


# # gets all tickets assigned to the logged-in user based on the token provided in the request header
# @users_bp.route('my-tickets', methods=['GET'])
# @token_required
# def user_tickets():
#     try:
#         user_id = request.user_id  # type: ignore
#         service_tickets = db.session.query(ServiceUsers).filter(ServiceUsers.user_id == user_id).all()
#         tickets_list = [ticket.id for ticket in service_tickets]  # or serialize as needed
#         return jsonify({"tickets": tickets_list}), 200
#     except ValidationError as e:
#         return jsonify(e.messages), 400 
#     except Exception as e:
#         return jsonify(str(e)), 400



# # GET at id
# @users_bp.route('<int:user_id>', methods=['GET'])
# def read_user(user_id):
#     try:
#         user = db.session.get(Users, user_id)
#         return user_schema.jsonify(user), 200
#     except ValidationError as e:
#         return jsonify(e.messages), 400 
#     except Exception as e:
#         return jsonify(str(e)), 400

# # Assignment
# # DELETE '/<int:id'>: Deletes a specific User based on the id passed in through the url.
# @users_bp.route('<int:user_id>', methods=['DELETE'])
# @token_required
# def delete_user(user_id):
#     try:
#         user = db.session.get(Users, user_id)
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({"message": f"Successfully deleted user {user_id}"}), 200
#     except ValidationError as e:
#         return jsonify(e.messages), 400 
#     except Exception as e:
#         return jsonify(str(e)), 400

# # Assignment
# # PUT '/<int:id>':  Updates a specific User based on the id passed in through the url.
# @users_bp.route('<int:user_id>', methods=['PUT'])
# @token_required
# def update_user(user_id):
#     try:
#         user = db.session.get(Users, user_id) 
#         if not user: 
#             return jsonify({"message": "user not found"}), 404  
        
#         user_data = user_schema.load(request.json)  # type: ignore

#         for key, value in user_data.items():
#             if value: #blank fields will not be updated
#                 if key !="password":
#                     # print(f"user {user} key {key} value {value}")
#                     setattr(user, key, value) 
#                 else:
#                     setattr(user, key, generate_password_hash(value)) 
                    
#         db.session.commit()
#         return user_schema.jsonify(user), 200
#     except ValidationError as e:
#         return jsonify(e.messages), 400 
#     except Exception as e:
#         return jsonify(str(e)), 400
    