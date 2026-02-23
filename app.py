from flask import Flask,session
from datetime import timedelta
#importing the database will allow us to access the data from the db_connector
from db_connector import database

#define database
db = database()

#initialise flask app
app = Flask(__name__)
app.secret_key = "67" #session management
app.permanent_session_lifetime = timedelta(minutes=2)

import routes

if __name__ == '__main__':
    app.run(debug=True) # run flask in debug mode