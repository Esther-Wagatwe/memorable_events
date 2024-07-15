#!/usr/bin/python3
"""A module for viewing Event objects."""
from api.v1.routes import app_views
from flask import jsonify, request
from api.v1.routes.models import Event, db


@app_views.route('/events/', methods=['GET'])
def get_events():
    """Lists all the events"""
    events = Event.query.all()
    events_json = [event.serialize() for event in events]
    return jsonify(events_json)


@app_views.route('/events/<int:event_id>/', methods=['GET'])
def get_event(event_id):
    """List the event with that ID"""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    return jsonify(event.serialize())


@app_views.route('/events/', methods=['POST'])
def create_event():
    """Create an event"""
    req_data = request.get_json()

    if not req_data:
        abort(400, "Not a JSON")
    if 'name' not in req_data or 'location' not in req_data or 'date' not in req_data or 'owner_id' not in req_data:
        abort(400, "Missing required fields")

    new_event = Event(
        location=req_data['location'],
        description=req_data['description', None],
        date=req_data['date'],
        name=req_data['name'],
        owner_id=req_data['owner_id']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.serialize()), 201
