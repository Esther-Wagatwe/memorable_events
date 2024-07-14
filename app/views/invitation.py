from flask import request, redirect, url_for, render_template, jsonify
from flask_login import login_required
from models import Guest, Event, Invitation
from models.engine import Session
from views import app_views
from .send_invite import send_email


@app_views.route('/invite/accept/<int:invitation_id>', methods=['GET'])
def accept_invitation(invitation_id):
    session = Session()
    invitation = session.query(Invitation).filter_by(invitation_id=invitation_id).first()
    if invitation:
        invitation.status = 'Accepted'
        guest = session.query(Guest).filter_by(guest_id=invitation.guest_id).first()
        guest.status = 'Accepted'
        session.commit()
    session.close()
    return "Invitation Accepted"

@app_views.route('/invite/decline/<int:invitation_id>', methods=['GET'])
def decline_invitation(invitation_id):
    session = Session()
    invitation = session.query(Invitation).filter_by(invitation_id=invitation_id).first()
    if invitation:
        invitation.status = 'Declined'
        guest = session.query(Guest).filter_by(guest_id=invitation.guest_id).first()
        guest.status = 'Declined'
        session.commit()
    session.close()
    return "Invitation Declined"

@app_views.route('/invite/<int:guest_id>/<int:event_id>', methods=['POST'])
def invite_guest(guest_id, event_id):
    session = Session()
    guest = session.query(Guest).filter_by(guest_id=guest_id).first()
    event = session.query(Event).filter_by(event_id=event_id).first()

    if guest and event:
        status = request.json.get('status', 'Pending')

        new_invitation = Invitation(status=status, guest_id=guest_id, event_id=event_id)
        session.add(new_invitation)
        session.commit()

        link = f"http://127.0.0.1/invite/accept/{new_invitation.invitation_id}"
        message = (f"You are invited to the following event:\n\n"
                   f"{event.description}\n\n"
                   f"Please accept or decline your invitation: {link}")

        send_email(guest.email, "Event Invitation", message)

    session.close()
    return redirect(url_for('app_views.landing'))