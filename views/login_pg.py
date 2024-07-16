from flask import Flask, request, session, redirect, url_for, render_template, jsonify, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.engine import Session
from views import app_views
from models import User

@app_views.route("/accounts/login", methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        session_db = Session()

        user_email = request.form['email']
        user_password = request.form['password']
        remember = request.form.get('remember') == 'on'

        user = session_db.query(User).filter_by(email=user_email).first()

        if user and user.check_password(user_password):
            login_user(user, remember=remember)

            flash('Logged in successfully!', 'success')
            return redirect(request.args.get('next') or url_for('app_views.dashboard'))
        else:
            session_db.close()
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html')

@app_views.route("/accounts/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('app_views.login'))