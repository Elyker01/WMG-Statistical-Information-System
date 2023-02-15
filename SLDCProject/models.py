import flask
import sqlite3
import matplotlib.pyplot as plt
import time
import os
import string
from flask import redirect, request, render_template, url_for, session, Blueprint

from routes import *
from views import *

modelsBP = Blueprint('modelsBP',__name__)
app = Flask(__name__)

#Create the table the data will be stored in
def createTable(conn, cursor):
    #Use the connection and cursor declared in the index method and carry out 
    #these SQLITE statements
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic2019 (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic2020 (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic2021 (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistic2022 (moduleName TEXT, grade INTEGER, percentage INTEGER)")
    conn.commit()

#Clear the previous data so sample data is displayed for demonstration purposes 
def deleteTable(conn, cursor):
    #Use the connection and cursor declared in the index method and carry out 
    #these SQLITE statements
    cursor.execute("DELETE FROM statistic2019")
    cursor.execute("DELETE FROM statistic2020")
    cursor.execute("DELETE FROM statistic2021")
    cursor.execute("DELETE FROM statistic2022")
    conn.commit()

#Deletes the entire data in the SQLITE table which will then
#reflect on the chart and table in the web page
@modelsBP.route('/deleteData2019', methods=['POST'])
def deleteData2019():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        #Carries out a delete statement which deletes everything in the table
        #and then a select to fetch the data inside which will be nothing
        c.execute("DELETE FROM statistic2019")
        c.execute("SELECT * FROM statistic2019")
        conn.commit()
        deletedData = c.fetchall()

        createChart2019(deletedData)
        conn.close()

        return redirect(url_for('viewsBP.inPersonClasses2019'))

@modelsBP.route('/deleteData2020', methods=['POST'])
def deleteData2020():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        c.execute("DELETE FROM statistic2020")
        c.execute("SELECT * FROM statistic2020")
        conn.commit()
        deletedData = c.fetchall()

        createChart2020(deletedData)
        conn.close()

        return redirect(url_for('viewsBP.inPersonClasses2020'))

@modelsBP.route('/deleteData2021', methods=['POST'])
def deleteData2021():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        c.execute("DELETE FROM statistic2021")
        c.execute("SELECT * FROM statistic2021")
        conn.commit()
        deletedData = c.fetchall()

        createChart2021(deletedData)
        conn.close()

        return redirect(url_for('viewsBP.inPersonClasses2021'))

@modelsBP.route('/deleteData2022', methods=['POST'])
def deleteData2022():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        c.execute("DELETE FROM statistic2022")
        c.execute("SELECT * FROM statistic2022")
        conn.commit()
        deletedData = c.fetchall()

        createChart2022(deletedData)
        conn.close()

        return redirect(url_for('viewsBP.inPersonClasses2022'))






#Update the data in the database which will then be displayed
#in the chart and the table in the web page
@modelsBP.route('/updateData2019', methods=['POST'])
def updateData2019():
    #Checks if the user is logged in and is a tutor(admin)
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
        
        #Fetches the data input into the form on the webpage and assigns
        #to the respective variable
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        #Cross checks what the user has input to see it is present in the database, ignoring case
        c.execute("SELECT * FROM statistic2019 WHERE LOWER(moduleName) LIKE ?", (moduleName.strip().lower(),))
        updatingModule = c.fetchone()
        
        #If the module is present, then update the table and create the chart again
        if updatingModule:
            #Capitalises each word of the module name if it has multiple words
            #Ignoring whitespace and case
            c.execute("UPDATE statistic2019 SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) = ?", (string.capwords(moduleName.strip()), grade, percentage, moduleName.strip().lower()))
            conn.commit()
            c.execute("SELECT * FROM statistic2019")
            updatedData = c.fetchall()
            createChart2019(updatedData)
            return redirect(url_for('viewsBP.inPersonClasses2019'))

        #If the module is not present and the name consists of only whitespace
        #then show an error on the web page
        elif not updatingModule and moduleName.strip() == "":
            conn.commit()
            c.execute("SELECT * FROM statistic2019")
            notChangedData = c.fetchall()
            createChart2019(notChangedData)
            return render_template("inPersonClasses2019.html", whiteSpaceError=True, session="Tutor", data=notChangedData)

        #If the module doesn't exist at all, then show an error on the web page
        elif not updatingModule:
            conn.commit()
            c.execute("SELECT * FROM statistic2019")
            notChangedData = c.fetchall()
            createChart2019(notChangedData)
            return render_template("inPersonClasses2019.html", error=True, session="Tutor", data=notChangedData)
  
        conn.close()

@modelsBP.route('/updateData2020', methods=['POST'])
def updateData2020():

    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

   
        c.execute("SELECT * FROM statistic2020 WHERE LOWER(moduleName) LIKE ?", (moduleName.strip().lower(),))
        updatingModule = c.fetchone()
        if updatingModule:
            c.execute("UPDATE statistic2020 SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) = ?", (string.capwords(moduleName.strip()), grade, percentage, moduleName.strip().lower()))
            conn.commit()
            c.execute("SELECT * FROM statistic2020")
            updatedData = c.fetchall()
            createChart2020(updatedData)
            return redirect(url_for('viewsBP.inPersonClasses2020'))

        elif not updatingModule and moduleName.strip() == "":
            conn.commit()
            c.execute("SELECT * FROM statistic2020")
            notChangedData = c.fetchall()
            createChart2020(notChangedData)
            return render_template("inPersonClasses2020.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
        elif not updatingModule:
            conn.commit()
            c.execute("SELECT * FROM statistic2020")
            notChangedData = c.fetchall()
            createChart2020(notChangedData)
            return render_template("inPersonClasses2020.html", error=True, session="Tutor", data=notChangedData)
  
        conn.close()

@modelsBP.route('/updateData2021', methods=['POST'])
def updateData2021():
    #Checks if the user is logged in and is a tutor(admin)
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        c.execute("SELECT * FROM statistic2021 WHERE LOWER(moduleName) LIKE ?", (moduleName.strip().lower(),))
        updatingModule = c.fetchone()
        if updatingModule:
            c.execute("UPDATE statistic2021 SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) = ?", (string.capwords(moduleName.strip()), grade, percentage, moduleName.strip().lower()))
            conn.commit()
            c.execute("SELECT * FROM statistic2021")
            updatedData = c.fetchall()
            createChart2021(updatedData)
            return redirect(url_for('viewsBP.inPersonClasses2021'))

        elif not updatingModule and moduleName.strip() == "":
            conn.commit()
            c.execute("SELECT * FROM statistic2021")
            notChangedData = c.fetchall()
            createChart2021(notChangedData)
            return render_template("inPersonClasses2021.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
        elif not updatingModule:
            conn.commit()
            c.execute("SELECT * FROM statistic2021")
            notChangedData = c.fetchall()
            createChart2021(notChangedData)
            return render_template("inPersonClasses2021.html", error=True, session="Tutor", data=notChangedData)
  
        conn.close()


@modelsBP.route('/updateData2022', methods=['POST'])
def updateData2022():

    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']


        c.execute("SELECT * FROM statistic2022 WHERE LOWER(moduleName) LIKE ?", (moduleName.strip().lower(),))
        updatingModule = c.fetchone()
        if updatingModule:
            c.execute("UPDATE statistic2022 SET moduleName=?, grade=?, percentage=? WHERE LOWER(moduleName) = ?", (string.capwords(moduleName.strip()), grade, percentage, moduleName.strip().lower()))
            conn.commit()
            c.execute("SELECT * FROM statistic2022")
            updatedData = c.fetchall()
            createChart2022(updatedData)
            return redirect(url_for('viewsBP.inPersonClasses2022'))

        elif not updatingModule and moduleName.strip() == "":
            conn.commit()
            c.execute("SELECT * FROM statistic2022")
            notChangedData = c.fetchall()
            createChart2021(notChangedData)
            return render_template("inPersonClasses2022.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
        elif not updatingModule:
            conn.commit()
            c.execute("SELECT * FROM statistic2022")
            notChangedData = c.fetchall()
            createChart2021(notChangedData)
            return render_template("inPersonClasses2022.html", error=True, session="Tutor", data=notChangedData)
  
        conn.close()


@modelsBP.route('/addData2019', methods=['POST'])
def addData2019():

    # Connect to the database
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
        #Fetches the data input into the form on the webpage and assigns
        #to the respective variable
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        #If the module name is empty or it consists of only whitespaces
        #the data will remain unchanged, and an error will be displayed on the web page
        if not moduleName or moduleName.isspace():
            c.execute("SELECT * FROM statistic2019")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2019(notChangedData)
            return render_template("inPersonClasses2019.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
    

        else:
            c.execute("SELECT * FROM statistic2019 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
            duplicateModule = c.fetchall()
            #If the moduleName is in the correct format, it will check if the module already exists
            #in the database, if so, it will display an error on the webapge.
            if duplicateModule:
                c.execute("SELECT * FROM statistic2019")
                conn.commit()
                notChangedData = c.fetchall()
                createChart2022(notChangedData)
                return render_template('inPersonClasses2019.html', moduleExistError=True, session="Tutor", data=notChangedData)

            #If the module name doesn't already exist, the data will be inserted into the database 
            #which will then be displayed on the chart and on the table.
            else:
                c.execute("INSERT INTO statistic2019 (moduleName, grade, percentage) VALUES (?, ?, ?)", (moduleName.strip(), grade, percentage))
                c.execute("SELECT * FROM statistic2019")
                conn.commit()
                data = c.fetchall()

                createChart2022(data)
                conn.close()

                return redirect(url_for('viewsBP.inPersonClasses2019'))
    elif 'user' in session and users[1].get(session['user']):
        return redirect('/unauthorised')

@modelsBP.route('/addData2020', methods=['POST'])
def addData2020():

    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        if not moduleName or moduleName.isspace():
            c.execute("SELECT * FROM statistic2020")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2020(notChangedData)
            return render_template("inPersonClasses2020.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
    
        else:
            c.execute("SELECT * FROM statistic2020 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
            duplicateModule = c.fetchall()
            if duplicateModule:
                c.execute("SELECT * FROM statistic2020")
                conn.commit()
                notChangedData = c.fetchall()
                createChart2022(notChangedData)
                return render_template('inPersonClasses2020.html', moduleExistError=True, session="Tutor", data=notChangedData)
            else:
                c.execute("INSERT INTO statistic2020 (moduleName, grade, percentage) VALUES (?, ?, ?)", (moduleName.strip(), grade, percentage))
                c.execute("SELECT * FROM statistic2020")
                conn.commit()
                data = c.fetchall()

                createChart2022(data)
                conn.close()

                return redirect(url_for('viewsBP.inPersonClasses2020'))

@modelsBP.route('/addData2021', methods=['POST'])
def addData2021():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        if not moduleName or moduleName.isspace():
            c.execute("SELECT * FROM statistic2021")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2021(notChangedData)
            return render_template("inPersonClasses2021.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
    
        else:
            c.execute("SELECT * FROM statistic2021 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
            duplicateModule = c.fetchall()
            if duplicateModule:
                c.execute("SELECT * FROM statistic2021")
                conn.commit()
                notChangedData = c.fetchall()
                createChart2022(notChangedData)
                return render_template('inPersonClasses2022.html', moduleExistError=True, session="Tutor", data=notChangedData)
            else:
                c.execute("INSERT INTO statistic2021 (moduleName, grade, percentage) VALUES (?, ?, ?)", (moduleName.strip(), grade, percentage))
                c.execute("SELECT * FROM statistic2021")
                conn.commit()
                data = c.fetchall()

                createChart2022(data)
                conn.close()

                return redirect(url_for('viewsBP.inPersonClasses2021'))

@modelsBP.route('/addData2022', methods=['POST'])
def addData2022():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']



        if not moduleName or moduleName.isspace():
            c.execute("SELECT * FROM statistic2022")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2022(notChangedData)
            return render_template("inPersonClasses2022.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
    
        else:
            c.execute("SELECT * FROM statistic2022 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
            duplicateModule = c.fetchall()
            if duplicateModule:
                c.execute("SELECT * FROM statistic2022")
                conn.commit()
                notChangedData = c.fetchall()
                createChart2022(notChangedData)
                return render_template('inPersonClasses2022.html', moduleExistError=True, session="Tutor", data=notChangedData)
            else:
                c.execute("INSERT INTO statistic2022 (moduleName, grade, percentage) VALUES (?, ?, ?)", (moduleName.strip(), grade, percentage))
                c.execute("SELECT * FROM statistic2022")
                conn.commit()
                data = c.fetchall()

                createChart2022(data)
                conn.close()

                return redirect(url_for('viewsBP.inPersonClasses2022'))



@modelsBP.route('/deleteModule2019', methods=['POST'])
def deleteModule2019():

    # Connect to the database
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        #Fetches the data input into the form on the webpage and assigns
        #to the respective variable
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        c.execute("SELECT * FROM statistic2019 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
        deletingModule = c.fetchone()

        #If the module is present, then delete it from the database and create the chart again
        if deletingModule:
            c.execute("DELETE FROM statistic2019 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
            c.execute("SELECT * FROM statistic2019")
            conn.commit()
            newData = c.fetchall()
            createChart2019(newData)
            return redirect(url_for('viewsBP.inPersonClasses2019'))

        #If the module name is empty or it consists of only whitespaces
        #the data will remain unchanged, and an error will be displayed on the web page
        elif not deletingModule and moduleName.strip() == "":
            c.execute("SELECT * FROM statistic2019")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2019(notChangedData)
            return render_template("inPersonClasses2019.html", whiteSpaceError=True, session="Tutor", data=notChangedData)

        #If the module doesn't exist at all, the data will remain unchanged,
        #and an error will be displayed on the web page
        elif not deletingModule:
            c.execute("SELECT * FROM statistic2019")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2019(notChangedData)
            return render_template("inPersonClasses2019.html", error=True, session="Tutor", data=notChangedData)


@modelsBP.route('/deleteModule2020', methods=['POST'])
def deleteModule2020():
    # Connect to the database
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        #Fetches the data input into the form on the webpage and assigns
        #to the respective variable
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        c.execute("SELECT * FROM statistic2020 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
        deletingModule = c.fetchone()
        if deletingModule:
            c.execute("DELETE FROM statistic2020 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
            c.execute("SELECT * FROM statistic2020")
            conn.commit()
            newData = c.fetchall()
            createChart2020(newData)
            return redirect(url_for('viewsBP.inPersonClasses2020'))

        elif not deletingModule and moduleName.strip() == "":
            c.execute("SELECT * FROM statistic2020")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2020(notChangedData)
            return render_template("inPersonClasses2020.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
        elif not deletingModule:
            c.execute("SELECT * FROM statistic2020")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2019(notChangedData)
            return render_template("inPersonClasses2020.html", error=True, session="Tutor", data=notChangedData)


@modelsBP.route('/deleteModule2021', methods=['POST'])
def deleteModule2021():
    # Connect to the database
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        #Fetches the data input into the form on the webpage and assigns
        #to the respective variable
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        c.execute("SELECT * FROM statistic2021 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
        deletingModule = c.fetchone()
        if deletingModule:
            c.execute("DELETE FROM statistic2021 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
            c.execute("SELECT * FROM statistic2021")
            conn.commit()
            newData = c.fetchall()
            createChart2021(newData)
            return redirect(url_for('viewsBP.inPersonClasses2021'))

        elif not deletingModule and moduleName.strip() == "":
            c.execute("SELECT * FROM statistic2021")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2021(notChangedData)
            return render_template("inPersonClasses2021.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
        elif not deletingModule:
            c.execute("SELECT * FROM statistic2021")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2019(notChangedData)
            return render_template("inPersonClasses2021.html", error=True, session="Tutor", data=notChangedData)


@modelsBP.route('/deleteModule2022', methods=['POST'])
def deleteModule2022():
    # Connect to the database
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()

        #Fetches the data input into the form on the webpage and assigns
        #to the respective variable
        moduleName = request.form['module']
        grade = request.form['grade']
        percentage = request.form['percentage']

        c.execute("SELECT * FROM statistic2022 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
        deletingModule = c.fetchone()
        if deletingModule:
            c.execute("DELETE FROM statistic2022 WHERE LOWER(moduleName) = ?", (moduleName.strip().lower(),))
            c.execute("SELECT * FROM statistic2022")
            conn.commit()
            newData = c.fetchall()
            createChart2022(newData)
            return redirect(url_for('viewsBP.inPersonClasses2022'))

        elif not deletingModule and moduleName.strip() == "":
            c.execute("SELECT * FROM statistic2022")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2022(notChangedData)
            return render_template("inPersonClasses2022.html", whiteSpaceError=True, session="Tutor", data=notChangedData)
        elif not deletingModule:
            c.execute("SELECT * FROM statistic2022")
            conn.commit()
            notChangedData = c.fetchall()
            createChart2019(notChangedData)
            return render_template("inPersonClasses2022.html", error=True, session="Tutor", data=notChangedData)

    #Creates chart using the matplotlib library
def createChart2019(data):
    
    #Connect to the database and carry out a select all to fetch all data
    #And store it into the data variable
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2019")
    data = c.fetchall()

    #Assign variables for each row of the database data
    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    # Create the chart with the data inside the database
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade 2019')
    #Set limit to 115 to make it more aesthetically pleasning
    ax.set_ylim(0, 115)
    ax.set_xlim(0, 115)

    #Loop through each module in the chart and annotate
    #the name of the module on top based on the bar's height
    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    # Save the chart to the static folder of the solution
    fig.savefig(os.path.join(app.static_folder, 'chart2019.png'))
   

def createChart2020(data):
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2020")
    data = c.fetchall()

    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade 2020')
    ax.set_ylim(0, 115)
    ax.set_xlim(0, 115)

    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 5),
            textcoords='offset points',
            ha='center', va='bottom')
            

    fig.savefig(os.path.join(app.static_folder, 'chart2020.png'))

def createChart2021(data):
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2021")
    data = c.fetchall()

    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade 2021')
    ax.set_ylim(0, 115)
    ax.set_xlim(0, 115)

    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    fig.savefig(os.path.join(app.static_folder, 'chart2021.png'))


def createChart2022(data):
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2022")
    data = c.fetchall()

    moduleName = [row[0] for row in data]
    grades = [row[1] for row in data]
    percentage = [row[2] for row in data]
    
    fig, ax = plt.subplots()
    bar = ax.bar(percentage, grades)
    ax.set_xlabel('Percentage of In-Person Classes (%)')
    ax.set_ylabel('Average Grade (out of 100)')
    ax.set_title('In-person Classes vs Average Grade 2022')
    ax.set_ylim(0, 115)
    ax.set_xlim(0, 115)

    for i, b in enumerate(bar):
        height = b.get_height()
        ax.annotate(moduleName[i],
            xy=(b.get_x() + b.get_width()/2, height),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center', va='bottom')

    fig.savefig(os.path.join(app.static_folder, 'chart2022.png'))