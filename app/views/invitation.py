from flask import request, redirect, url_for, render_template, jsonify
from flask_login import login_required
from models import Guest, Event, Invitation
from models.engine import Session
from views import app_views



@app_views.route('/invitations/<int:invitation_id>/respond', methods=['GET'])
def respond_to_invitation(invitation_id):
    from .send_invite import send_email
    session = Session()
    invitation = session.query(Invitation).filter_by(invitation_id=invitation_id).first()
    
    if not invitation:
        return jsonify({"error": "Invitation not found"}), 404


    status = request.args.get('status')
    if status not in ["Accepted", "Declined"]:
        return jsonify({"error": "Invalid status"}), 400

    invitation.status = status

    guest = session.query(Guest).filter_by(guest_id=invitation.guest_id).first()
    guest.status = status

    session.commit()

    # guest = session.query(Guest).filter_by(guest_id=invitation.guest_id).first()
    event = session.query(Event).filter_by(event_id=invitation.event_id).first()
    subject = f"Your response to the invitation for {event.name}"
    body = (f"Dear {guest.name},\n\n"
            f"You have {status.lower()} the invitation to {event.name}.\n\n"
            f"Best regards,\n"
            f"Memorable Events Team")
    send_email(guest.email, subject, body)

    session.close()
    # return jsonify({"message": "Invitation response recorded"}), 200
    return render_template('response.html', message="Your response was received. Thank you!")

@app_views.route('/events/<int:event_id>/<int:guest_id>/invitations', methods=['GET'])
def get_invitation(event_id, guest_id):
    session = Session()
    invitation = session.query(Invitation).filter_by(event_id=event_id, guest_id=guest_id).first()

    if not invitation:
        return jsonify({'error': 'Invitation not found'}), 404
    
    return jsonify(invitation.serialize()), 200



@app_views.route('/events/<int:event_id>/<int:guest_id>/invitations', methods=['POST'])
def send_invitation(event_id, guest_id):
    from .send_invite import send_email
    session = Session()
    guest = session.query(Guest).filter_by(guest_id=guest_id).first()
    event = session.query(Event).filter_by(event_id=event_id).first()
    
    if not event or not guest:
        return jsonify({"error": "Event or Guest not found"}), 404

    invitation = Invitation(status="Pending", event_id=event_id, guest_id=guest_id)
    session.add(invitation)
    session.commit()

    accept_url = url_for('app_views.respond_to_invitation', invitation_id=invitation.invitation_id, status='Accepted', _external=True)
    decline_url = url_for('app_views.respond_to_invitation', invitation_id=invitation.invitation_id, status='Declined', _external=True)

    subject = f"You're invited to {event.name}"
    body = (f"Dear {guest.name},\n\n"
            f"You are invited to {event.name} on {event.date}.\n\n"
            f"Please respond to this invitation by clicking one of the links below:\n"
            f"Accept: {accept_url}\n"
            f"Decline: {decline_url}\n\n"
            f"Best regards,\n"
            f"Memorable Events Team")
    send_email(guest.email, subject, body)
    session.close()
    return jsonify({"message": "Invitation sent successfully"}), 201

