from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from .dashboard_pg import *
from .event_pg import *
from .login_pg import *
from .task_pg import *
from .vendors_pg import *
from .guests_pg import *
from .landing_pg import *
from .signup_pg import *
from .users import *
from .reviews import *
from .about_pg import *
from .invitation import *
# from .send_invite import *