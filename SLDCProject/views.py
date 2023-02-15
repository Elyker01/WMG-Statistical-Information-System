from flask import redirect, request, render_template, url_for, session, Blueprint
import os
import time
from flask import Flask
import sqlite3
import matplotlib.pyplot as plt
from routes import *
from models import *

viewsBP = Blueprint('viewsBP',__name__)
app = Flask(__name__)


#Homepage that will be displayed when user runs the application
@viewsBP.route('/')
def index():
    #Checks if the tutor or student is already logged in and gives respective access
    if 'user' in session:
        email = session['user']
        for user in users:
            if email in user:
                if user[email]['is_admin']:
                    return render_template('index.html', session="Tutor", time=time.time())
                elif not user[email]['is_admin']:
                    return render_template('index.html', session="Student", time=time.time())

    #If no one is logged, then it will create the sqlite tables and add sample data
    else:
        session.pop('user', None)
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


@viewsBP.route('/home')
def home():
    if 'user' in session:
        email = session['user']
        for user in users:
            if email in user:
                if user[email]['is_admin']:
                    return render_template('home.html', session="Tutor")
                elif not user[email]['is_admin']:
                    return render_template('home.html', session="Student")
    else:
        return render_template('home.html')


#Menu Page for the user to navigate the system
@viewsBP.route('/menu')
def menu():
    #Checks if user is logged in either as a tutor or student and if so,
    #the logout button will be present rather than login
    if 'user' in session:
        email = session['user']
        for user in users:
            if email in user:
                if user[email]['is_admin']:
                    return render_template('menu.html', session="Tutor")
                elif not user[email]['is_admin']:
                    return render_template('menu.html', session="Student")
    else:
        return render_template('menu.html')

@viewsBP.route('/inPersonClasses2019')
def inPersonClasses2019():
    #If the user is a tutor(admin), the page will load with the CRUD operations and they will able
    #to modify the data.
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        c.execute("SELECT * FROM statistic2019")
        data = c.fetchall()
        createChart2019(data)
        timestamp = int(time.time())
        return render_template('inPersonClasses2019.html', data=data, session="Tutor", timestamp=timestamp)
    
    
    #If the user is a student, the page will load without the CRUD operations and they will
    #only be able to view the data for the different years.
    elif 'user' in session and users[1].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        c.execute("SELECT * FROM statistic2019")
        data = c.fetchall()
        createChart2019(data)
        timestamp = int(time.time())
        return render_template('inPersonClasses2019.html', data=data, session="Student", timestamp=timestamp)
    else:
        return redirect(url_for('routesBP.login'))



@viewsBP.route('/inPersonClasses2020')
def inPersonClasses2020():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        c.execute("SELECT * FROM statistic2020")
        data = c.fetchall()
        createChart2020(data)
        timestamp = int(time.time())
        return render_template('inPersonClasses2020.html', data=data, session="Tutor", timestamp=timestamp)
    elif 'user' in session and users[1].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        c.execute("SELECT * FROM statistic2020")
        data = c.fetchall()
        createChart2020(data)
        timestamp = int(time.time())
        return render_template('inPersonClasses2020.html', data=data, session="Student", timestamp=timestamp)
    else:
        return redirect(url_for('routesBP.login'))

@viewsBP.route('/inPersonClasses2021')
def inPersonClasses2021():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        c.execute("SELECT * FROM statistic2021")
        data = c.fetchall()
        createChart2021(data)
        timestamp = int(time.time())
        return render_template('inPersonClasses2021.html', data=data, session="Tutor", timestamp=timestamp)
    elif 'user' in session and users[1].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        c.execute("SELECT * FROM statistic2021")
        data = c.fetchall()
        createChart2021(data)
        timestamp = int(time.time())
        return render_template('inPersonClasses2021.html', data=data, session="Student", timestamp=timestamp)
    else:
        return redirect(url_for('login'))

@viewsBP.route('/inPersonClasses2022')
def inPersonClasses2022():
    if 'user' in session and users[0].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        c.execute("SELECT * FROM statistic2022")
        data = c.fetchall()
        createChart2022(data)
        timestamp = int(time.time())
        return render_template('inPersonClasses2022.html', data=data, session="Tutor", timestamp=timestamp)
    elif 'user' in session and users[1].get(session['user']):
        conn = sqlite3.connect('wmgsisDB.db')
        c = conn.cursor()
    
        c.execute("SELECT * FROM statistic2022")
        data = c.fetchall()
        createChart2022(data)
        timestamp = int(time.time())
        return render_template('inPersonClasses2022.html', data=data, session="Student", timestamp=timestamp)
    else:
        return redirect(url_for('routesBP.login'))

