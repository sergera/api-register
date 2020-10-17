from flask import Flask
from route import Routes

app = Flask(__name__)

routes = Routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=8080) #run app in debug mode on port 5000