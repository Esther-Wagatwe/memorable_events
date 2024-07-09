from flask import session, redirect, url_for, render_template

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('app_views.login'))
    return wrapper