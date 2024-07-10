from flask import request, redirect, url_for, render_template, jsonify
from views.decorators import login_required
#from models import Vendor
from models.engine import Session
from views import app_views

@app_views.route('/landing/')
# @login_required
def landing_page():
    return render_template('landing.html')
