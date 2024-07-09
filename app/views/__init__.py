from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from views.dashboard import *
from views.event_pg import *
from views.decorators import *
from views.login import *
from views.task_pg import *