from flask import request, redirect, url_for, render_template, jsonify
from views.decorators import login_required
# from models import Vendor
from models.engine import Session
from views import app_views

@app_views.route('/accounts/signup/')
# @login_required
def signup():
    return render_template('signup.html')
