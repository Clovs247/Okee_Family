from flask_app import app
from flask_app.controllers import MainController, users, cars, gears

if __name__ == "__main__":
    app.run(debug=True)