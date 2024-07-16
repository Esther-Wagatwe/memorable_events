from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from models.engine import Session
from models import User, Event, Guest, Invitation, Task, Reviews, Vendor
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
    
    user = session.get(User, user_id)
    
    if not user:
        session.close()
        return jsonify({'error': 'User not found'}), 404
    
    try:
        with session.no_autoflush:
            events = session.query(Event).filter(Event.owner_id == user_id).all()
            
            for event in events:
                guests = session.query(Guest).filter_by(event_id=event.event_id).all()
                for guest in guests:
                    session.delete(guest)

                vendors = session.query(Vendor).filter_by(event_id=event.event_id).all()
                for vendor in vendors:
                    session.delete(vendor)

                tasks = session.query(Task).filter_by(event_id=event.event_id).all()
                for task in tasks:
                    session.delete(task)

                invitations = session.query(Invitation).filter_by(event_id=event.event_id).all()
                for invitation in invitations:
                    session.delete(invitation)

                reviews = session.query(Reviews).filter(Reviews.vendor_id.in_(
                    session.query(Vendor.vendor_id).filter_by(event_id=event.event_id)
                )).all()
                for review in reviews:
                    session.delete(review)

                session.delete(event)

        session.delete(user)
        session.commit()
        
        return jsonify({'message': 'User and associated records deleted successfully'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Failed to delete user', 'details': str(e)}), 500
    finally:
        session.close()
