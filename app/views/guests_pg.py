from flask import request, redirect, url_for, render_template, jsonify
from flask_login import login_required
from models import Guest, Event, Invitation
from models.engine import Session
from views import app_views

@app_views.route('/events/<int:event_id>/guests/', methods=['GET'])
def list_guests(event_id):
    session = Session()
    guests = (
        session.query(Guest, Invitation.status)
        .outerjoin(Invitation)
        .filter(Guest.event_id == event_id)
        .all()
    )
    return jsonify([
    {
        "guest_id": guest.guest_id,
        "name": guest.name,
        "email": guest.email,
        "phone": guest.phone,
        # "status": invitation_status if invitation_status else guest.status  # Default to guest status
        "status": guest.status
    }
    for guest, invitation_status in guests
])

@app_views.route('/guests/', methods=['POST'])
def add_guest():
    data = request.get_json()
    session = Session()
    new_guest = Guest(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        status=data.get('status'),
        event_id=data.get('event_id')
    )
    try:
        session.add(new_guest)
        session.commit()
        return jsonify(new_guest.serialize()), 201
    except Exception as e:
        session.rollback()
        print(f"Error adding guest: {e}")
        return jsonify({"error": "Failed to add guest"}), 500
    finally:
        session.close()

@app_views.route('/guests/<int:guest_id>', methods=['DELETE'])
def delete_guest(guest_id):
    session = Session()
    guest = session.query(Guest).get(guest_id)
    if guest:
        session.delete(guest)
        session.commit()
        return jsonify({"message": "Guest deleted"}), 204
    return jsonify({"error": "Guest not found"}), 404