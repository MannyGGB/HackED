from flask import Flask,session
from datetime import timedelta
#importing the database will allow us to access the data from the db_connector
from db_connector import database
import sys

if sys.argv.__len__() > 1:
    port = sys.argv[1]
    print("Api running on port : {}".format(port))
#define database
db = database()
#port for deployment
port = 5100


#initialise flask app
app = Flask(__name__)
app.secret_key = "67" #session management
app.permanent_session_lifetime = timedelta(minutes=2)

import routes

if __name__ == '__main__':
  #  app.run(debug=True) # run flask in debug mode
    app.run(host="0.0.0.0", port=port)