from views.decorators import login_required
from flask import request, redirect, url_for, render_template, jsonify
from views.decorators import login_required
from models import Event
from views import app_views
from models.engine import Session

@app_views.route('/events/', methods=['GET', 'POST', 'PUT', 'DELETE'])
#@login_required
def all_events():
    session = Session()
    
    if request.method == 'GET':
        events = session.query(Event).all()
        session.close()
        return render_template('event.html', events=events)
    
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        location = data.get('location')
        date = data.get('date')
        owner_id = request.json.get('owner_id')

        if not name or not description or not location or not date or not owner_id: 
            return jsonify({'error': 'Missing data'}), 400
        
        new_event = Event(name=name, description=description, location=location, date=date, owner_id=owner_id)
        session.add(new_event)
        session.commit()
        
        session.close()
        return jsonify({'message': 'Event created successfully'}), 201
    
    elif request.method == 'PUT':
        data = request.get_json()
        event_id = data.get('event_id')
        event = session.query(Event).get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        event.name = data.get('name', event.name)
        event.description = data.get('description', event.description)
        event.location = data.get('location', event.location)
        event.date = data.get('date', event.date)
        
        session.commit()
        session.close()
        return jsonify({'message': 'Event updated successfully'})
    
    elif request.method == 'DELETE':
        event_id = request.args.get('event_id')
        event = session.query(Event).get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        session.delete(event)
        session.commit()
        
        session.close()
        return jsonify({'message': 'Event deleted successfully'})

    else:
        return jsonify({'error': 'Method not allowed'}), 405
