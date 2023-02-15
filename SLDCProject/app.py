"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import sqlite3
from flask import redirect, request, render_template, url_for, session, Blueprint
from flask import Flask
import matplotlib.pyplot as plt
import time
import os 
import string

from routes import *
from views import *
from models import *

app = Flask(__name__)
app.register_blueprint(viewsBP)
app.register_blueprint(modelsBP)
app.register_blueprint(routesBP)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#Secret key for session management
app.secret_key = 'This is my secret key'


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
