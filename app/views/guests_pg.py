from flask import request, redirect, url_for, render_template, jsonify
from views.decorators import login_required
from models import Guest
from models.engine import Session
from views import app_views

@app_views.route('/guests/')
# @login_required
def guests_page():
    return render_template('guest.html')