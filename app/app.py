from flask import Flask
from views import app_views
import secrets
from models import User
from models.engine import Session
from flask_login import LoginManager
from config import init_app


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

app.url_map.strict_slashes = False
app.register_blueprint(app_views)

mail = init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app_views.login'

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.close()
    return user

if __name__ == '__main__':
    # for rule in app.url_map.iter_rules():
    #     print(rule.endpoint)
    app.run(host='0.0.0.0', port='8000', debug=True)