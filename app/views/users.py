from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from models.engine import Session
from models import User
from views import app_views

@app_views.route('/users/', methods=['GET'])
def get_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return jsonify([user.serialize() for user in users]), 200

@app_views.route('/users/', methods=['POST'])
def create_user():
    email = request.json.get('email')
    password = request.json.get('password_hash')
    username = request.json.get('username')

    if not email or not password or not username:
        return jsonify({'error': 'Please provide email, password, and username'}), 400


    new_user = User(email=email, username=username)
    new_user.set_password(password)

    session = Session()
    session.add(new_user)
    session.commit()

    user_id = new_user.user_id

    session.close()

    return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201


@app_views.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()

    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        session.close()
        return jsonify({'error': 'User not found'}), 404

    try:
        session.delete(user)
        session.commit()
        session.close()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({'error': 'Failed to delete user', 'details': str(e)}), 500