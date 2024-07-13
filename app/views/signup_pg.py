from flask import request, redirect, url_for, render_template, flash
from models import User
from models.engine import Session
from views import app_views

@app_views.route('/accounts/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        session_db = Session()
        if session_db.query(User).filter_by(username=username).first():
            session_db.close()
            flash('Username already exists.')
            return redirect(url_for('app_views.signup'))
        if session_db.query(User).filter_by(email=email).first():
            session_db.close()
            flash('Email already registered.')
            return redirect(url_for('app_views.signup'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        session_db.add(new_user)
        session_db.commit()
        session_db.close()
        flash('Registration successful. Please log in.')
        return redirect(url_for('app_views.login'))
    return render_template('signup.html')