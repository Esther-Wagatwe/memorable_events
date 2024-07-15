from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.routes.events import *
from api.v1.routes.invitations import *
from api.v1.routes.guests import *
from api.v1.routes.vendors import *
from api.v1.routes.tasks import *
from api.v1.routes.models import *
