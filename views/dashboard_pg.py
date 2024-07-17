from flask import render_template
from flask_login import login_required
from models import Event, EventStatus, Vendor
from views import app_views
from models.engine import Session
from flask_login import current_user
from models.dummy_data_gen import create_data


@app_views.route('/', methods=['GET'])
@login_required
def dashboard():
    
    # Generate random data
    # create_data()
    
    session = Session()
    context = {}
    try:
        
        # Get the events
        my_events = (
            session.query(Event)
            .filter(Event.owner_id == current_user.user_id)
            .all()
        )
        context['events'] = my_events
        
        # Get all available vendors
        top_vendors = (
            session.query(Vendor)
            .all()
        )
        top_vendors.sort(key=lambda x: x.average_review_score, reverse=True)
        context['top_vendors'] = top_vendors[:10]
        
        # Get mt upcoming events
        upcoming_events = (
            session.query(Event)
            .filter(Event.status == EventStatus.UPCOMING)
            .filter(Event.owner_id == current_user.user_id)
            .all()
        )
        context['upcoming_events'] = upcoming_events
        
        # Get mt total guests from upcoming events
        total_guests = sum(len(event.guests) for event in upcoming_events)
        context['total_guests'] = total_guests
        
        # Get my total vendors for upcoming events
        total_vendors = sum(len(event.vendors) for event in upcoming_events)
        context['total_vendors'] = total_vendors
        
        # Get the total cost for upcoming events
        total_cost = sum(event.get_event_total_cost() for event in upcoming_events)
        context['total_cost'] = f"Ksh.{total_cost:,.2f}"
        
        
        
        return render_template('dashboard/dashboard.html', **context)
    finally:
        session.close()
