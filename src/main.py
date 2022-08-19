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
from models import db, User, People, Planets 
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

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_People():
    characters = [people.serialize() 
    for people in People.query.all()]
    return jsonify(characters), 200



@app.route('/people/<int:people_id>', methods=['GET'])
def detalle_people(people_id):
    people = People.query.get(people_id).serialize()
    return jsonify(people), 200



@app.route('/planets', methods=['GET'])
def get_Planets():
    planetas = [planets.serialize()
    for planets in Planets.query.all()]
    return jsonify(planetas), 200



@app.route('/planets/<int:planet_id>', methods=['GET'])
def detalle_Planets(planet_id):
    planets = Planets.query.get(planet_id).serialize()
    return jsonify(planets), 200


@app.route('/users', methods=['GET'])
def get_Users():
    usuarios = [usuario.serialize()
    for usuario in User.query.all()]
    return jsonify(usuarios), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_users_Fav():
    user = User.query.get(user_id)
    favoritos = [favorito.serialize () for favorito in user.fav_People + user.fav_Planets]
    return jsonify(favoritos), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_Planet(planet_id):
    body = request.json
    favorito = fav_Planets(
        user_id = body["user_id"] 
        if "user_id" in body else None, 
        planet_id = body["planets_id"] 
        if "planet_id" in body else None
        )
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.serialize()), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_People(people_id):
    body = request.json
    favorito = fav_People(
        user_id = body["user_id"] 
        if "user_id" in body else None, 
        people_id = body["people_id"] 
        if "people_id" in body else None
        )
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.serialize()), 201



@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def del_fav_Planet(planet_id):
    eliminarFav = fav_Planets.query.filter(fav_Planets.planets_id == planet_id).delete()
    return jsonify(eliminarFav), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def del_fav_People(people_id):
    eliminarFav = fav_People.query.filter(fav_People.people_id == people_id).delete()
    return jsonify(eliminarFav), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
