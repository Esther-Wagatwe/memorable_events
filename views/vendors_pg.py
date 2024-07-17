from flask import request, redirect, url_for, render_template, jsonify
from flask_login import login_required
from models import Vendor, Event
from models.engine import Session
from views import app_views
from flask_login import current_user


@app_views.route('/vendors/', methods=['GET'])
@login_required
def list_vendors():
    session = Session()
    context = {}
    
    try:
        vendors = session.query(Vendor).all()
        context['vendors'] = vendors
    
        # return jsonify([vendor.serialize() for vendor in vendors])
        return render_template('vendors.html', **context)
    finally:
        session.close()


@app_views.route('/vendors/<int:vendor_id>', methods=['GET'])
@login_required
def get_vendor(vendor_id):
    session = Session()
    context = {}
    
    try:
        vendor = session.query(Vendor).get(vendor_id)
        context['vendor'] = vendor
        
        my_events = (
            session.query(Event)
            .filter(Event.owner_id == current_user.user_id)
            .all()
        )
        context['events'] = my_events
        
        if vendor:
            return render_template('vendor_details.html', **context)
        else:
            return jsonify({'error': 'Vendor not found'}), 404
    
    finally:
        session.close()


@app_views.route('/vendors/<int:vendor_id>/book-event', methods=['POST'])
@login_required
def book_event_vendor(vendor_id):

    session = Session()
    context = {}
    
    try:
        vendor = session.query(Vendor).get(vendor_id)
        context['vendor'] = vendor
        
        event_id = request.form.get('event')
        event = session.query(Event).get(event_id)
        context['event'] = event
        
        event.vendors.append(vendor)
        session.commit()
        
        if vendor:
            return redirect(f'/events/{event_id}')
        else:
            return jsonify({'error': 'Vendor not found'}), 404
    
    finally:
        session.close()


@app_views.route('/vendors/', methods=['POST'])
def add_vendor():
    data = request.json
    new_vendor = Vendor(
        name=data['name'],
        type=data['type'],
        description=data['description'],
        event_id=data['event_id'],
        image_path=data['image_path'],
        phone_number=data['phone_number'],
        email=data['email']
    )
    session = Session()
    session.add(new_vendor)
    session.commit()
    vendor_id = new_vendor.vendor_id
    session.close()
    return jsonify({'message': 'Vendor added successfully', 'vendor_id': new_vendor.vendor_id}), 201





@app_views.route('/vendors/<int:vendor_id>', methods=['PUT'])
def edit_vendor(vendor_id):
    session = Session()
    vendor = session.query(Vendor).get(vendor_id)
    if vendor:
        data = request.json
        if 'name' in data:
            vendor.name = data['name']
        if 'type' in data:
            vendor.type = data['type']
        if 'description' in data:
            vendor.description = data['description']
        if 'image_path' in data:
            vendor.image_path = data['image_path']
        if 'phone_number' in data:
            vendor.phone_number = data.get('phone_number', vendor.phone_number)
        if 'email' in data:
            vendor.email = data.get('email', vendor.email)

        session.commit()
        session.close()
        return jsonify({'message': 'Vendor updated successfully'})
    else:
        session.close()
        return jsonify({'error': 'Vendor not found'}), 404

@app_views.route('/vendors/<int:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    session = Session()
    vendor = session.query(Vendor).get(vendor_id)
    if vendor:
        session.delete(vendor)
        session.commit()
        session.close()
        return jsonify({'message': 'Vendor deleted successfully'})
    else:
        session.close()
        return jsonify({'error': 'Vendor not found'}), 404

