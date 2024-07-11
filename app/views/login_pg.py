from flask import Flask, request, session, redirect, url_for, render_template, jsonify, flash
from models.engine import Session
from views import app_views
from models import User



@app_views.route("/accounts/login", methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        session_db = Session()

        user_email = request.form['email']
        user_password = request.form['password']
        remember = request.form.get('remember')  # Check if 'remember' checkbox is checked

        user = session_db.query(User).filter_by(email=user_email).first()

        if user and user.check_password(user_password):
            session['user_id'] = user.user_id
            session['username'] = user.username

            if remember:
                session.permanent = True  # Set session to be permanent

            session_db.close()
            flash('Logged in successfully!', 'success')
            return redirect(url_for('app_views.dashboard'))
        else:
            session_db.close()
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html')


@app_views.route("/accounts/logout")
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))