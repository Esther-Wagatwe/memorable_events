from flask import render_template
from flask import Flask

from views import app_views
from views.decorators import login_required

@app_views.route("/", endpoint='dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')
