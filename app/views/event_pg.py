from views.decorators import login_required
from flask import request, redirect, url_for, render_template, jsonify
from models import Event
from views import app_views
from models.engine import Session

@app_views.route('/events', methods=['GET'])
# @login_required
def get_events():
    session = Session()
    try:
        events = session.query(Event).all()
        return render_template('event.html', events=events)
    finally:
        session.close()
    return render_template('event.html')

@app_views.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    session = Session()
    try:
        event = session.query(Event).get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        return jsonify(event.serialize()), 200
    finally:
        session.close()

@app_views.route('/events/', methods=['POST'])
def create_event():
    data = request.json
    session = Session()
    try:
        new_event = Event(
            location=data.get('location'),
            description=data.get('description'),
            date=data.get('date'),
            name=data.get('name'),
            owner_id=data.get('owner_id')
        )
        session.add(new_event)
        session.commit()
        return jsonify(new_event.serialize()), 201
    finally:
        session.close()

@app_views.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    session = Session()
    try:
        event = session.query(Event).get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        if 'location' in data:
            event.location = data['location']
        if 'description' in data:
            event.description = data['description']
        if 'date' in data:
            event.date = data['date']
        if 'name' in data:
            event.name = data['name']
        # if 'owner_id' in data:
        #     event.owner_id = data['owner_id']

        session.commit()
        return jsonify({'message': 'Event updated successfully', 'event': event.serialize()}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app_views.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    session = Session()
    try:
        event = session.query(Event).get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        session.delete(event)
        session.commit()
        return jsonify({'message': 'Event deleted'}), 200
    finally:
        session.close()