from flask import render_template
from flask_login import login_required
from models import Event, EventStatus
from views import app_views
from models.engine import Session

@app_views.route('/', methods=['GET'])
@login_required
def dashboard():
    session = Session()
    try:
        events = session.query(Event).filter(Event.status == EventStatus.ACTIVE).all()
        event_data = []
        for event in events:
            event_data.append({
                'id': event.event_id,
                'name': event.name,
                'date': event.date.strftime('%Y-%m-%d'),
                'total_guests': len(event.guests),
                'total_vendors': len(event.vendors),
                'status': event.status.name
            })
        total_events = len(events)
        return render_template('dashboard/dashboard.html', events=event_data, total_events=total_events)
    finally:
        session.close()
