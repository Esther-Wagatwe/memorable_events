from flask import request, redirect, url_for, render_template, jsonify
from views.decorators import login_required
from models import Vendor
from models.engine import Session
from views import app_views

@app_views.route('/vendors/')
# @login_required
def vendors_page():
    return render_template('vendor.html')
