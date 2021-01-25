from flask import Flask

from .controllers.user_controller import app_user
from .views.exception_handler import app_error_handler

app = Flask(__name__)
app.register_blueprint(app_user)
app.register_blueprint(app_error_handler)