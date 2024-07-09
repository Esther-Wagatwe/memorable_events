from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from models.engine import Session
from models import User
from views import app_views



@app_views.route("/accounts/login", methods=['GET', 'POST'], endpoint='login')
def login():

    if request.method == 'POST':
        print(request.form)

        # Extract user creds
        user_email = request.form['email']
        user_password = request.form['password']
    
    return render_template('auth/login.html')

@app_views.route('/users/', methods=['GET'])
def get_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return jsonify([user.serialize() for user in users]), 200

@app_views.route('/users/', methods=['POST'])
def create_user():
    # Parse JSON data from request
    email = request.json.get('email')
    password_hash = request.json.get('password_hash')
    username = request.json.get('username')

    # Validate data
    if not email or not password_hash or not username:
        return jsonify({'error': 'Please provide email, password_hash, and username'}), 400

    # Create a new user object
    new_user = User(email=email, password_hash=password_hash, username=username)

    # Assuming you have a session and commit the changes
    session = Session()
    session.add(new_user)
    session.commit()
    session.close()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.user_id}), 201