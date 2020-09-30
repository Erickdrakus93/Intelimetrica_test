from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from restaurants_app.Models import Restaurant_table, SchemaRestaurant
from restaurants_app.config import app_config
import geopandas as gpd

# This is the main function to call the app in a main file as run in this proyect
db = SQLAlchemy()


def create_app(config_name):
    """This the creation of the app with context and routing"""
    app = Flask(config_name, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Here we can define a temporary route

    @app.route('/', methods=['GET'])
    def hello():
        return 'Hello World!'

    @app.route('/restaurants', methods=['GET'])
    def index():
        """This function is for consulting all the restaurants"""
        get_restaurants = Restaurant_table.query.all()
        restaurant_schema = SchemaRestaurant(many=True)
        restaurants, errors = restaurant_schema.dump(get_restaurants)
        return make_response(jsonify({"restaurants": restaurants}))

    @app.route('/restaurants', methods=['POST'])
    def create_restaurant():
        data = request.get_json()
        restaurant_schema = SchemaRestaurant()
        restaurants, error = restaurant_schema.load(data)
        result = restaurant_schema.dump(restaurants.create())
        return make_response(jsonify({"restaurants": result}), 201)

    @app.route('/restaurants/<restaurant_id>', methods=['POST', 'GET'])
    def get_restaurant_by_id(restaurant_id):
        get_restaurant = Restaurant_table.query.get(restaurant_id)
        restaurant_schema = SchemaRestaurant()
        restaurant, error = restaurant_schema.dump(get_restaurant)
        return make_response(jsonify({"restaurant": restaurant}))

    @app.route('/restaurants/<restaurant_id>', methods=['GET', 'POST'])
    def delete_restaurant_by_id(restaurant_id):
        get_restaurant = Restaurant_table.query.get(restaurant_id)
        db.session.delete(get_restaurant)
        db.session.commit()
        return make_response("", 204)

    @app.route('/restaurants/<restaurant_id>', methods=['GET', 'POST'])
    def update_restaurant_id(restaurant_id):
        data = request.get_json()
        get_restaurant = Restaurant_table.query.get(restaurant_id)
        if data.get('name'):
            get_restaurant.name = data['name']
        if data.get('site'):
            get_restaurant.site = data['site']
        db.session.add(get_restaurant)
        db.session.commit()
        restaurant_schema = SchemaRestaurant(only=['restaurant_id', 'name',
                                                   'site'])
        restaurant, error = restaurant_schema.dump(get_restaurant)
        return make_response(jsonify({"restaurant": restaurant}), 204)

    return app
