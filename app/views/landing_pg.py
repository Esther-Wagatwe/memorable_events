from flask import request, redirect, url_for, render_template, jsonify
from models.engine import Session
from views import app_views

@app_views.route('/landing')
def landing_page():
    return render_template('landing.html')
