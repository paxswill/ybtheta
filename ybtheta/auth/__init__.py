from .views import blueprint, oauth, login_manager
from .models import User

# This is just to register the models with the database
from . import models as _models
