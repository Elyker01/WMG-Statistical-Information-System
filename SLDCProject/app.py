"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
from flask import render_template



app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/statistic')
def statistic():
    return render_template('statistic.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')



#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
