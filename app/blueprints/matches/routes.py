from app.blueprints.matches import matches_bp
from .schemas import match_schema, matches_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Matches, Users, Messages, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required




# Assignment
# POST '/' : Creates a new match
@matches_bp.route('', methods=['POST']) 
def create_match():
    try:
        # data = match_schema.load(request.json) # type: ignore
        data = request.json
        new_match = Matches(**data) # type: ignore
        db.session.add(new_match)
        db.session.commit()
        return match_schema.jsonify(new_match), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400

# Assignment
# GET '/': Retrieves all Matches
@matches_bp.route('', methods=['GET']) 
def read_matches():
    try: 
        matches = db.session.query(Matches).all()
        return matches_schema.jsonify(matches), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400


# GET at id
@matches_bp.route('<int:match_id>', methods=['GET'])
def read_match(match_id):
    try:
        match = db.session.get(Matches, match_id)
        return match_schema.jsonify(match), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400

# Assignment
# DELETE '/<int:id'>: Deletes a specific Match based on the id passed in through the url.
@matches_bp.route('<int:match_id>', methods=['DELETE'])
# @token_required
def delete_match(match_id):
    try:
        match = db.session.get(Matches, match_id)
        db.session.delete(match)
        db.session.commit()
        return jsonify({"message": f"Successfully deleted match {match_id}"}), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400

# Assignment
# PUT '/<int:id>':  Updates a specific match based on the id passed in through the url.
@matches_bp.route('<int:match_id>', methods=['PUT'])
# @token_required
def update_match(match_id):
    try:
        match = db.session.get(Matches, match_id) 
        if not match: 
            return jsonify({"message": "match not found"}), 404  
        
        match_data = match_schema.load(request.json)  # type: ignore

        for key, value in match_data.items():
            if value: #blank fields will not be updated
                if key !="password":
                    # print(f"match {match} key {key} value {value}")
                    setattr(match, key, value) 
                else:
                    setattr(match, key, generate_password_hash(value)) 
                    
        db.session.commit()
        return match_schema.jsonify(match), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400
    