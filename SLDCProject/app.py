"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
from flask import render_template
import matplotlib.pyplot as plt



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
    data = [('Module 1', 60, 80), ('Module 2',40, 90), ('Module 3', 70, 85)]
    create_chart()
    return render_template('statistic.html', data=data)


@app.route('/menu')
def menu():
    return render_template('menu.html')


def create_chart():
    # Your data for in-person classes vs average grade
    classes = ['Module 1', 'Module 2', 'Module 3']
    grades = [80, 90, 85]
    percentage = [30, 50, 70]
    
    # Create the chart
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade')
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 100)

    # Add labels to the bars
    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(classes[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    # Save the chart to a file
    fig.savefig(os.path.join(app.static_folder, 'chart.png'))



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
