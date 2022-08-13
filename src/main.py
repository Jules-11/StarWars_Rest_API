"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():

    people = Character.query.all()
    people_serialize = list(map(lambda x: x.serialize(), people))

    return jsonify( people_serialize), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):

    single_people = Character.query.get(people_id)
    single_people_serialize = serialize(single_people)

    return jsonify( single_people_serialize), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planet = Planet.query.all()
    planet_serialize = list(map(lambda x: x.serialize(), planet))

    return jsonify(planet_serialize), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):

    single_planet = Planet.query.get(planet_id)
    single_planet_serialize = serialize(single_planet)

    return jsonify(single_planet_serialize), 200

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    users_serialize = list(map(lambda x: x.serialize(), users))

    return jsonify(users_serialize), 200

@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):

    user_favorites = Favorite.query.filter_by(user_id=user_id)
    user_favorites_serialize = list(map(lambda x: x.serialize(), user_favorites))
    
    return jsonify(user_favorites_serialize), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def set_favorite_planet(planet_id):
    request_body = request.get_json(force=True)
    user_id = request_body["user_id"]

    favorite_planet = Favorite(user_id=user_id, planet_id=planet_id)

    db.session.add(favorite_planet)
    db.session.commit()
     
@app.route('/favorite/people/<int:character_id>', methods=['POST'])
def set_favorite_people(character_id):
    request_body = request.get_json(force=True)
    user_id = request_body["user_id"]

    favorite_character = Favorite(user_id=user_id, character_id=character_id)

    db.session.add(favorite_character)
    db.session.commit()


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    request_body = request.get_json(force=True)
    user_id = request_body["user_id"]

    delete_favorite_planet = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id)

    db.session.delete(delete_favorite_planet)
    db.session.commit()
     
@app.route('/favorite/people/<int:character_id>', methods=['DELETE'])
def delete_favorite_people(character_id):
    request_body = request.get_json(force=True)
    user_id = request_body["user_id"]

    delete_favorite_character = Favorite.query.filter_by(user_id=user_id, character_id=character_id)

    db.session.delete(delete_favorite_character)
    db.session.commit()



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
