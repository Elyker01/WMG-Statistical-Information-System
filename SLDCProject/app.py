"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import sqlite3
from flask import redirect, request, render_template, url_for
from flask import Flask
import matplotlib.pyplot as plt
import time

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def hello():

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    createTable(conn,c)
    deleteTable(conn,c)

    c.execute("INSERT INTO statistic(moduleName,grade,percentage) values('SDLC', 80, 50)")
    c.execute("INSERT INTO statistic(moduleName,grade,percentage) values('Internet Of Things', 60, 70)")
    c.execute("INSERT INTO statistic(moduleName,grade,percentage) values('Applied Maths', 90, 25)")

    conn.commit()

    return render_template('index.html', time=time.time())


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/statistic')
def statistic():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM statistic")
    data = c.fetchall()
    createChart(data)
    timestamp = int(time.time())
    return render_template('statistic.html', data=data, timestamp=timestamp)


@app.route('/menu')
def menu():
    return render_template('menu.html')


def createChart(data):
    # Your data for in-person classes vs average grade

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic")
    data = c.fetchall()

    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    # Create the chart with the data inside the database
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
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    # Save the chart to a file
    fig.savefig(os.path.join(app.static_folder, 'chart.png'))


#Create the table the data will be stored in
def createTable(conn, cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    conn.commit()


def deleteTable(conn, cursor):
    cursor.execute("DELETE FROM statistic")
    conn.commit()


@app.route('/deleteData', methods=['POST'])
def deleteData():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("DELETE FROM statistic")
    c.execute("SELECT * FROM statistic")
    conn.commit()
    deletedData = c.fetchall()

    createChart(deletedData)
    conn.close()

    return redirect(url_for('statistic'))





#Update the data in the database which will then be displayed
@app.route('/updateData', methods=['POST'])
def updateData():

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    #c.execute("UPDATE statistic SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) LIKE ?", (moduleName, grade, percentage, moduleName))
    #conn.commit()
    #updatedData = c.fetchall()
    c.execute("SELECT * FROM statistic WHERE LOWER(moduleName) LIKE ?", (moduleName,))
    updatingModule = c.fetchone()
    if updatingModule:
        c.execute("UPDATE statistic SET moduleName=?, grade=?, percentage=? WHERE moduleName = ?", (moduleName, grade, percentage, moduleName))
        conn.commit()
        c.execute("SELECT * FROM statistic")
        updatedData = c.fetchall()
        createChart(updatedData)
        return redirect(url_for('statistic'))

    if not updatingModule:
        return render_template("statistic.html", error=True)
  
    conn.close()


@app.route('/addData', methods=['POST'])
def addData():
    module = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    # Insert the data into the table
    c.execute("INSERT INTO statistic (moduleName, grade, percentage) VALUES (?, ?, ?)", (module, grade, percentage))
    c.execute("SELECT * FROM statistic")
    conn.commit()
    data = c.fetchall()

    createChart(data)

    
    # Commit the changes and close the connection
    conn.close()

    return redirect(url_for('statistic'))

@app.route('/deleteModule', methods=['POST'])
def deleteModule():
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("SELECT * FROM statistic WHERE LOWER(moduleName) = ?", (moduleName,))
    deletingModule = c.fetchone()
    if deletingModule:
        c.execute("DELETE FROM statistic WHERE LOWER(moduleName) = ?", (moduleName,))
        c.execute("SELECT * FROM statistic")
        conn.commit()
        newData = c.fetchall()
        createChart(newData)
        return redirect(url_for('statistic'))

    if not deletingModule:
        c.execute("SELECT * FROM statistic")
        conn.commit()
        notChangedData = c.fetchall()
        createChart(notChangedData)
        return render_template("statistic.html", error=True, data=notChangedData)

    



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
