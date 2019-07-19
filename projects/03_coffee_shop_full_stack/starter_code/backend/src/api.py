import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound
import json
from flask_cors import CORS
from flask_cors import cross_origin

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    return jsonify({
        "success": True,
        'drinks': list(
            map(lambda drink: drink.short(), Drink.query.all()))
    }), 200


'''
implement endpoint
'''
@app.route('/drinks-detail', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth("get:drinks-detail")
def get_drinks_detail(jwt):
    return jsonify({
        "success": True,
        'drinks': list(
            map(lambda drink: drink.long(), Drink.query.all()))
    }), 200


'''
implement endpoint
'''


@app.route('/drinks', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth("post:drinks")
def add_drinks(jwt):
    title = request.json.get("title")
    recipe = request.json.get("recipe")
    if type(recipe) is not list:
        recipe = [recipe]
    drink = Drink(title=title, recipe=json.dumps(recipe))
    drink.insert()
    return jsonify({
        "success": True,
        "drink": drink.long()
    }), 200


'''
implement endpoint
    PATCH /drinks/<id>
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth("patch:drinks")
def update_drinks(jwt, id):
    try:
        drink = Drink.query.filter_by(id=id).one()
    except NoResultFound:
        abort(404)
    # get data from json or current data
    drink.title = request.json.get("title") or drink.title
    recipe = request.json.get("recipe")
    if recipe:
        drink.recipe = json.dumps(recipe)
    drink.update()
    return jsonify({
        "success": True,
        "drink": drink.long()
    }), 200


'''
@TODO implement endpoint
    DELETE /drinks/<id>
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth("delete:drinks")
def drinks_delete(jwt, id):
    try:
        drink = Drink.query.filter_by(id=id).one()
        drink.delete()
        return jsonify({"success": True, "delete": id}), 200
    except NoResultFound:
        abort(404)


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
implement error handlers
'''


'''
implement error handler for 404
'''


@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


'''
implement error handler for AuthError
'''
@app.errorhandler(AuthError)
def not_authorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "not authorized"
    }), 401
