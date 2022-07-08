from flask import Blueprint, request, jsonify
from golf_inventory.helpers import token_required
from golf_inventory.models import db, User, GolfClub, golf_club_schema, golf_club_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some':'value'}

# create golfclub endpoint
@api.route('/golf_club', methods = ['POST'])
@token_required
def add_golfclub(current_user_token):
    brand = request.json['brand']
    club_type = request.json['club_type']
    description = request.json['description']
    price = request.json['price']
    shaft = request.json['shaft']
    material = request.json['material']
    color = request.json['color']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    golf_club = GolfClub(brand, club_type, description, price, shaft, material, color, user_token = user_token)

    db.session.add(golf_club)
    db.session.commit()

    response = golf_club_schema.dump(golf_club)

    return jsonify(response)

# Retrieve all golfclub Endpoints
@api.route('/golfclubs', methods = ['GET'])
@token_required
def get_golf_clubs(current_user_token):
    owner = current_user_token.token
    golf_clubs = GolfClub.query.filter_by(user_token = owner).all()
    response = golf_club_schema.dump(golf_clubs)
    return jsonify(response)


# Retrieve ONE golfclub Endpoint
@api.route('/golfclubs/<id>', methods = ['GET'])
@token_required
def get_golfclubs(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        drone = GolfClub.query.get(id)
        response = golf_club_schema.dump(drone)
        return jsonify(response)
    else:
        return jsonify({'message': "Valid Token Required"}), 401

# update golfclubs
@api.route('/golfclubs/<id>', methods = ['POST', 'PUT'])
@token_required
def update_golfclub(current_user_token, id):
    golf_club = GolfClub.query.get(id)

    golf_club.brand = request.json['name']
    golf_club.club_type = request.json['club_type']
    golf_club.description = request.json['description']
    golf_club.price = request.json['price']
    golf_club.shaft = request.json['weight']
    golf_club.material = request.json['material']
    golf_club.color = request.json['material']
    golf_club.user_token = current_user_token.token

    db.session.commit()
    response = golf_club_schema.dump(golf_club)
    return jsonify(response)

# Delete golf club
@api.route('/golfclubs/<id>', methods=['DELETE'])
@token_required
def delete_golf_club(current_user_token, id):
    golfclub = GolfClub.query.get(id)
    db.session.delete(golfclub)
    db.session.commit()
    response = golf_club_schema.dump(golfclub)
    return jsonify(response)