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

    #Add sample data to be inserted in the database and displayed in the chart and table
    c.execute("INSERT INTO statistic2019(moduleName,grade,percentage) values('SDLC', 80, 50)")
    c.execute("INSERT INTO statistic2019(moduleName,grade,percentage) values('Internet Of Things', 60, 70)")
    c.execute("INSERT INTO statistic2019(moduleName,grade,percentage) values('Applied Maths', 90, 25)")

    c.execute("INSERT INTO statistic2020(moduleName,grade,percentage) values('Applied Maths II', 80, 50)")
    c.execute("INSERT INTO statistic2020(moduleName,grade,percentage) values('IBMO', 40, 70)")
    c.execute("INSERT INTO statistic2020(moduleName,grade,percentage) values('Networking', 80, 25)")

    c.execute("INSERT INTO statistic2021(moduleName,grade,percentage) values('ISBP', 80, 70)")
    c.execute("INSERT INTO statistic2021(moduleName,grade,percentage) values('Cyber Security', 60, 90)")
    c.execute("INSERT INTO statistic2021(moduleName,grade,percentage) values('Web Development I', 90, 55)")

    c.execute("INSERT INTO statistic2022(moduleName,grade,percentage) values('Web Development II', 80, 90)")
    c.execute("INSERT INTO statistic2022(moduleName,grade,percentage) values('Mobile Applications', 45, 50)")
    c.execute("INSERT INTO statistic2022(moduleName,grade,percentage) values('Agile Project Management', 60, 25)")

    conn.commit()

    return render_template('index.html', time=time.time())


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/inPersonClasses2019')
def inPersonClasses2019():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM statistic2019")
    data = c.fetchall()
    createChart2019(data)
    timestamp = int(time.time())
    return render_template('inPersonClasses2019.html', data=data, timestamp=timestamp)



@app.route('/inPersonClasses2020')
def inPersonClasses2020():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM statistic2020")
    data = c.fetchall()
    createChart2020(data)
    timestamp = int(time.time())
    return render_template('inPersonClasses2020.html', data=data, timestamp=timestamp)

@app.route('/inPersonClasses2021')
def inPersonClasses2021():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM statistic2021")
    data = c.fetchall()
    createChart2021(data)
    timestamp = int(time.time())
    return render_template('inPersonClasses2021.html', data=data, timestamp=timestamp)

@app.route('/inPersonClasses2022')
def inPersonClasses2022():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM statistic2022")
    data = c.fetchall()
    createChart2022(data)
    timestamp = int(time.time())
    return render_template('inPersonClasses2022.html', data=data, timestamp=timestamp)

@app.route('/search', methods=['GET'])
def search():
    pageNames = ['inPersonClasses2019', 'menu', 'home']
    search_query = request.args.get('search').lower()
    for page in pageNames:
        if search_query.replace(" ","") in page.lower():
            return redirect(url_for(page))
            
    return "No matching page found. Please try again."


@app.route('/menu')
def menu():
    return render_template('menu.html')




def createChart2019(data):
    # Your data for in-person classes vs average grade

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2019")
    data = c.fetchall()

    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    # Create the chart with the data inside the database
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade 2019')
    ax.set_ylim(0, 115)
    ax.set_xlim(0, 115)

    # Add labels to the bars
    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    # Save the chart to a file
    fig.savefig(os.path.join(app.static_folder, 'chart2019.png'))

def createChart2020(data):
# Your data for in-person classes vs average grade
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2020")
    data = c.fetchall()

    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    # Create the chart with the data inside the database
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade 2020')
    ax.set_ylim(0, 115)
    ax.set_xlim(0, 115)

    # Add labels to the bars
    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    # Save the chart to a file
    fig.savefig(os.path.join(app.static_folder, 'chart2020.png'))

def createChart2021(data):
# Your data for in-person classes vs average grade
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2021")
    data = c.fetchall()

    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    # Create the chart with the data inside the database
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade 2021')
    ax.set_ylim(0, 115)
    ax.set_xlim(0, 115)

    # Add labels to the bars
    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    # Save the chart to a file
    fig.savefig(os.path.join(app.static_folder, 'chart2021.png'))

def createChart2022(data):
# Your data for in-person classes vs average grade
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2022")
    data = c.fetchall()

    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    # Create the chart with the data inside the database
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade 2022')
    ax.set_ylim(0, 115)
    ax.set_xlim(0, 115)

    # Add labels to the bars
    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    # Save the chart to a file
    fig.savefig(os.path.join(app.static_folder, 'chart2022.png'))






#Create the table the data will be stored in
def createTable(conn, cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic2019 (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic2020 (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic2021 (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic2022 (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    conn.commit()


def deleteTable(conn, cursor):
    cursor.execute("DELETE FROM statistic2019")
    cursor.execute("DELETE FROM statistic2020")
    cursor.execute("DELETE FROM statistic2021")
    cursor.execute("DELETE FROM statistic2022")
    conn.commit()







@app.route('/deleteData2019', methods=['POST'])
def deleteData2019():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("DELETE FROM statistic2019")
    c.execute("SELECT * FROM statistic2019")
    conn.commit()
    deletedData = c.fetchall()

    createChart2019(deletedData)
    conn.close()

    return redirect(url_for('inPersonClasses2019'))

@app.route('/deleteData2020', methods=['POST'])
def deleteData2020():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("DELETE FROM statistic2020")
    c.execute("SELECT * FROM statistic2020")
    conn.commit()
    deletedData = c.fetchall()

    createChart2020(deletedData)
    conn.close()

    return redirect(url_for('inPersonClasses2020'))

@app.route('/deleteData2021', methods=['POST'])
def deleteData2021():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("DELETE FROM statistic2021")
    c.execute("SELECT * FROM statistic2021")
    conn.commit()
    deletedData = c.fetchall()

    createChart2021(deletedData)
    conn.close()

    return redirect(url_for('inPersonClasses2021'))

@app.route('/deleteData2022', methods=['POST'])
def deleteData2022():
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("DELETE FROM statistic2022")
    c.execute("SELECT * FROM statistic2022")
    conn.commit()
    deletedData = c.fetchall()

    createChart2022(deletedData)
    conn.close()

    return redirect(url_for('inPersonClasses2022'))






#Update the data in the database which will then be displayed
@app.route('/updateData2019', methods=['POST'])
def updateData2019():

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    #c.execute("UPDATE statistic SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) LIKE ?", (moduleName, grade, percentage, moduleName))
    #conn.commit()
    #updatedData = c.fetchall()
    c.execute("SELECT * FROM statistic2019 WHERE LOWER(moduleName) LIKE ?", (moduleName,))
    updatingModule = c.fetchone()
    if updatingModule:
        c.execute("UPDATE statistic2019 SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) = ?", (moduleName, grade, percentage, moduleName))
        conn.commit()
        c.execute("SELECT * FROM statistic2019")
        updatedData = c.fetchall()
        createChart2019(updatedData)
        return redirect(url_for('inPersonClasses2019'))

    if not updatingModule:
        return render_template("inPersonClasses2019.html", error=True)
  
    conn.close()

@app.route('/updateData2020', methods=['POST'])
def updateData2020():

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    #c.execute("UPDATE statistic SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) LIKE ?", (moduleName, grade, percentage, moduleName))
    #conn.commit()
    #updatedData = c.fetchall()
    c.execute("SELECT * FROM statistic2020 WHERE LOWER(moduleName) LIKE ?", (moduleName,))
    updatingModule = c.fetchone()
    if updatingModule:
        c.execute("UPDATE statistic2020 SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) = ?", (moduleName, grade, percentage, moduleName))
        conn.commit()
        c.execute("SELECT * FROM statistic2020")
        updatedData = c.fetchall()
        createChart2020(updatedData)
        return redirect(url_for('inPersonClasses2020'))

    if not updatingModule:
        return render_template("inPersonClasses2020.html", error=True)
  
    conn.close()

@app.route('/updateData2021', methods=['POST'])
def updateData2021():

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    #c.execute("UPDATE statistic SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) LIKE ?", (moduleName, grade, percentage, moduleName))
    #conn.commit()
    #updatedData = c.fetchall()
    c.execute("SELECT * FROM statistic2021 WHERE LOWER(moduleName) LIKE ?", (moduleName,))
    updatingModule = c.fetchone()
    if updatingModule:
        c.execute("UPDATE statistic2021 SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) = ?", (moduleName, grade, percentage, moduleName))
        conn.commit()
        c.execute("SELECT * FROM statistic2021")
        updatedData = c.fetchall()
        createChart2021(updatedData)
        return redirect(url_for('inPersonClasses2021'))

    if not updatingModule:
        return render_template("inPersonClasses2021.html", error=True)
  
    conn.close()


@app.route('/updateData2022', methods=['POST'])
def updateData2022():

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    #c.execute("UPDATE statistic SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) LIKE ?", (moduleName, grade, percentage, moduleName))
    #conn.commit()
    #updatedData = c.fetchall()
    c.execute("SELECT * FROM statistic2022 WHERE LOWER(moduleName) LIKE ?", (moduleName,))
    updatingModule = c.fetchone()
    if updatingModule:
        c.execute("UPDATE statistic2022 SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) = ?", (moduleName, grade, percentage, moduleName))
        conn.commit()
        c.execute("SELECT * FROM statistic2022")
        updatedData = c.fetchall()
        createChart2022(updatedData)
        return redirect(url_for('inPersonClasses2022'))

    if not updatingModule:
        return render_template("inPersonClasses2022.html", error=True)
  
    conn.close()


@app.route('/addData2019', methods=['POST'])
def addData2019():
    module = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    # Insert the data into the table
    c.execute("INSERT INTO statistic2019 (moduleName, grade, percentage) VALUES (?, ?, ?)", (module, grade, percentage))
    c.execute("SELECT * FROM statistic2019")
    conn.commit()
    data = c.fetchall()

    createChart2019(data)

    
    # Commit the changes and close the connection
    conn.close()

    return redirect(url_for('inPersonClasses2019'))

@app.route('/addData2020', methods=['POST'])
def addData2020():
    module = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    # Insert the data into the table
    c.execute("INSERT INTO statistic2020 (moduleName, grade, percentage) VALUES (?, ?, ?)", (module, grade, percentage))
    c.execute("SELECT * FROM statistic2020")
    conn.commit()
    data = c.fetchall()

    createChart2020(data)

    
    # Commit the changes and close the connection
    conn.close()

    return redirect(url_for('inPersonClasses2020'))

@app.route('/addData2021', methods=['POST'])
def addData2021():
    module = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    # Insert the data into the table
    c.execute("INSERT INTO statistic2021 (moduleName, grade, percentage) VALUES (?, ?, ?)", (module, grade, percentage))
    c.execute("SELECT * FROM statistic2021")
    conn.commit()
    data = c.fetchall()

    createChart2021(data)

    
    # Commit the changes and close the connection
    conn.close()

    return redirect(url_for('inPersonClasses2019'))

@app.route('/addData2022', methods=['POST'])
def addData2022():
    module = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    # Insert the data into the table
    c.execute("INSERT INTO statistic2022 (moduleName, grade, percentage) VALUES (?, ?, ?)", (module, grade, percentage))
    c.execute("SELECT * FROM statistic2022")
    conn.commit()
    data = c.fetchall()

    createChart2022(data)

    
    # Commit the changes and close the connection
    conn.close()

    return redirect(url_for('inPersonClasses2022'))



@app.route('/deleteModule2019', methods=['POST'])
def deleteModule2019():
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("SELECT * FROM statistic2019 WHERE LOWER(moduleName) = ?", (moduleName.lower(),))
    deletingModule = c.fetchone()
    if deletingModule:
        c.execute("DELETE FROM statistic2019 WHERE LOWER(moduleName) = ?", (moduleName.lower(),))
        c.execute("SELECT * FROM statistic2019")
        conn.commit()
        newData = c.fetchall()
        createChart2019(newData)
        return redirect(url_for('inPersonClasses2019'))

    if not deletingModule:
        c.execute("SELECT * FROM statistic2019")
        conn.commit()
        notChangedData = c.fetchall()
        createChart2019(notChangedData)
        return render_template("inPersonClasses2019.html", error=True, data=notChangedData)


@app.route('/deleteModule2020', methods=['POST'])
def deleteModule2020():
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("SELECT * FROM statistic2020 WHERE LOWER(moduleName) = ?", (moduleName.lower(),))
    deletingModule = c.fetchone()
    if deletingModule:
        c.execute("DELETE FROM statistic2020 WHERE LOWER(moduleName) = ?", (moduleName.lower(),))
        c.execute("SELECT * FROM statistic2020")
        conn.commit()
        newData = c.fetchall()
        createChart2020(newData)
        return redirect(url_for('inPersonClasses2020'))

    if not deletingModule:
        c.execute("SELECT * FROM statistic2020")
        conn.commit()
        notChangedData = c.fetchall()
        createChart2020(notChangedData)
        return render_template("inPersonClasses2020.html", error=True, data=notChangedData)


@app.route('/deleteModule2021', methods=['POST'])
def deleteModule2021():
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("SELECT * FROM statistic2021 WHERE LOWER(moduleName) = ?", (moduleName.lower(),))
    deletingModule = c.fetchone()
    if deletingModule:
        c.execute("DELETE FROM statistic2021 WHERE LOWER(moduleName) = ?", (moduleName.lower(),))
        c.execute("SELECT * FROM statistic2021")
        conn.commit()
        newData = c.fetchall()
        createChart2021(newData)
        return redirect(url_for('inPersonClasses2021'))

    if not deletingModule:
        c.execute("SELECT * FROM statistic2021")
        conn.commit()
        notChangedData = c.fetchall()
        createChart2021(notChangedData)
        return render_template("inPersonClasses2021.html", error=True, data=notChangedData)


@app.route('/deleteModule2022', methods=['POST'])
def deleteModule2022():
    moduleName = request.form['module']
    grade = request.form['grade']
    percentage = request.form['percentage']

    # Connect to the database
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    c.execute("SELECT * FROM statistic2022 WHERE LOWER(moduleName) = ?", (moduleName.lower(),))
    deletingModule = c.fetchone()
    if deletingModule:
        c.execute("DELETE FROM statistic2022 WHERE LOWER(moduleName) = ?", (moduleName.lower(),))
        c.execute("SELECT * FROM statistic2022")
        conn.commit()
        newData = c.fetchall()
        createChart2022(newData)
        return redirect(url_for('inPersonClasses2022'))

    if not deletingModule:
        c.execute("SELECT * FROM statistic2022")
        conn.commit()
        notChangedData = c.fetchall()
        createChart2022(notChangedData)
        return render_template("inPersonClasses2022.html", error=True, data=notChangedData)



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
