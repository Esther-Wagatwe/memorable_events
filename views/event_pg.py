from flask_login import login_required
from flask import request, redirect, url_for, render_template, jsonify
from flask_login import current_user
from models import Event, EventStatus, Guest
from views import app_views
from sqlalchemy.orm import joinedload
from models.engine import Session
import json


@app_views.route('/events', methods=['GET'])
@login_required
def get_events():
    session = Session()
    context = {}
    
    try:
        my_events = session.query(Event).filter(Event.owner_id == current_user.user_id).all()
        context['my_events'] = my_events
        
        return render_template('event.html', **context)
    finally:
        session.close()


@app_views.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event_view():
    if request.method == 'POST':
        
        # Extract user input on event details
        print(request.form)
        event_name = request.form.get('event-name')
        category = request.form.get('event-type')
        date = request.form.get('event-date')
        time = request.form.get('event-time')
        location = request.form.get('event-location')
        description = request.form.get('event-description')
        guests = request.form.getlist('guest_detail')
        
        # Create the event object
        event = Event(
            name=event_name,
            # category=category,
            date=date,
            # time=time,
            location=location,
            description=description,
            owner_id=current_user.user_id
        )
        session = Session()
        session.add(event)
        session.commit()
        
        # Create the guests
        for guest in guests:
            data = json.loads(guest)
            new_guest = Guest(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                event_id=event.event_id
            )
            session.add(new_guest)
            session.commit()
        
        return redirect('/events')
        
    return render_template('event_new.html')


@app_views.route('/events/<int:event_id>', methods=['GET'])
@login_required 
def event_details(event_id):
    session = Session()
    context = {}
    
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