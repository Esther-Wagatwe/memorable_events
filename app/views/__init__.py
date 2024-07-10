from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from views.dashboard import *
from views.event_pg import *
from views.decorators import *
from views.login import *
from views.task_pg import *
from views.vendors_pg import *
from views.guests_pg import *
from views.landing_pg import *
from views.signUp import *