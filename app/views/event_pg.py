from flask_login import login_required
from flask import request, redirect, url_for, render_template, jsonify
from flask_login import current_user
from models import Event, EventStatus 
from views import app_views
from sqlalchemy.orm import joinedload
from models.engine import Session


@app_views.route('/events', methods=['GET'])
@login_required
def get_events():
    session = Session()
    try:
        events = session.query(Event).filter(Event.status == EventStatus.ACTIVE).all()
        event_data = []
        for event in events:
            event_data.append({
                'id': event.event_id,
                'name': event.name,
                'date': event.date.strftime('%Y-%m-%d'),
                'status': event.status.name
            })
        return render_template('event.html', events=event_data)
        # return jsonify([event.serialize() for event in events])
    finally:
        session.close()

@app_views.route('/events/<int:event_id>', methods=['GET'])
@login_required 
def event_details(event_id):
    session = Session()
    try:
        event = session.query(Event).options(
            joinedload(Event.guests),
            joinedload(Event.vendors),
            joinedload(Event.tasks)
        ).filter(Event.event_id == event_id, Event.status == EventStatus.ACTIVE).first()

        if not event:
            return jsonify({'error': 'Event not found'}), 404

        return render_template('event_details.html', event=event, user_id=current_user.user_id)
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
        return jsonify({'success': True, 'message': 'Event updated successfully', 'event': event.serialize()}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
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