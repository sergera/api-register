from flask import Flask

from .controllers.user_controller import app_user
from .views.exception_handler import app_error_handler

app = Flask(__name__)
app.register_blueprint(app_user)
app.register_blueprint(app_error_handler)

if __name__ == '__main__':
    app.run(debug=True, port=8080) #run app in debug mode on port 5000