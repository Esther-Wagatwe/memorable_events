#!/usr/bin/python3
"""A module for viewing User objects."""
from api.v1.routes import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from api.v1.routes.models import User, db


@app_views.route('/users/', methods=['GET'])
def get_users():
    """Lists all the users"""
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app_views.route('/users/', methods=['POST'])
def create_user()
    """Creates a new user"""
    req_data = request.get_json()

    if not req_data:
        abort(400, "Not a JSON")
    if 'username' not in req_data or 'email' not in req_data or 'password_hash' not in req_data or 'role' not in req_data:
        abort(400, "Missing required fields")

    new_user = User(
        role=req_data['role'],
        email=req_data['email'],
        password_hash=req_data['password_hash'],
        username=req_data['username']
    )
    db.session.add(new_user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email or Username already exists'}), 400

    return jsonify(new_user.serialize()), 201
