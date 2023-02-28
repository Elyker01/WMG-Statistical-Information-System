import app
import sqlite3
import pytest
import unittest
import os 
from flask import session, url_for



@pytest.fixture
def client(request):
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    def teardown():
        pass 

    request.addfinalizer(teardown)
    return client

def test_addData(client):

    #Open new session with the test client 
    with client.session_transaction() as session:
        #Set the session as a tutor so they have the appropriate privileges
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    #Add test data 
    response = client.post('/addData2019', data={'module': 'Test Data', 
                                                    'grade': '60', 
                                                    'percentage': '80'})

    #Ensure the user has been redirected, meaning the insert was successful
    assert response.status_code == 302
    conn.commit()
    #Ensure the data has been added into the database 
    c.execute("SELECT * FROM statistic2019 WHERE moduleName='Test Data'")
    insertData = c.fetchall()
    #Ensure there is an entry for Test Data
    assert len(insertData) > 0
    assert insertData[0][0] == "Test Data"

    conn.close()

    
def test_addDataInvalidPrivileges(client):
    with client.session_transaction() as session:
        session['user'] = "student@warwick.ac.uk"

    response = client.post('/addData2019', data={'module': 'module', 
                                                    'grade': '60', 
                                                    'percentage': '70'})

    #Ensure user is forbidden from carrying out CRUD function
    assert response.status_code == 403




def test_updateData(client):
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("DELETE FROM statistic2019")
    
    #Insert Test Data to be updated 
    c.execute("INSERT INTO statistic2019 (moduleName, grade, percentage) VALUES (?,?,?)", 
              ('Agile Project Management', 40, 30))
    conn.commit()

    #Update the test data 
    response = client.post('/updateData2019', data={'module': 'Agile Project Management', 
                                                    'grade': '50', 
                                                    'percentage': '90'})
    assert response.status_code == 302


    #Ensure the test data was updated correctly
    c.execute("SELECT * FROM statistic2019 WHERE moduleName='Agile Project Management'")
    updatedData = c.fetchall()
    assert len(updatedData) > 0
    assert updatedData[0][0] == "Agile Project Management"
    assert updatedData[0][1] == 50
    assert updatedData[0][2] == 90

    c.execute("DELETE FROM statistic2019 WHERE moduleName='Agile Project Management'")
    conn.commit()
    conn.close()

def test_updateDataInvalidPrivileges(client):
    with client.session_transaction() as session:
        session['user'] = "student@warwick.ac.uk"

    response = client.post('/updateData2019', data={'module': 'Agile Project Management', 
                                                    'grade': '60', 
                                                    'percentage': '70'})

    #Ensure user is forbidden from carrying out CRUD function
    assert response.status_code == 403


def test_deleteModuleInvalidPrivileges(client):
    with client.session_transaction() as session:
        session['user'] = "student@warwick.ac.uk"

    response = client.post('/deleteModule2019', data={'module': 'Agile Project Management', 
                                                    'grade': '60', 
                                                    'percentage': '70'})

    #Ensure user is forbidden from carrying out CRUD function
    assert response.status_code == 403



def test_deleteModule(client):
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    #Insert test data to be deleted
    c.execute("INSERT INTO statistic2022 (moduleName, grade, percentage) VALUES (?,?,?)", 
              ('Internet of Things', 90, 75))
    c.execute("SELECT * FROM statistic2022 WHERE moduleName='Internet of Things'")
    insertedData = c.fetchall()
    assert len(insertedData) > 0
    conn.commit()
    conn.close()

    #Delete the test data
    response = client.post('/deleteModule2022', data={'module': 'Internet of Things',
                                                     'grade': '90', 
                                                     'percentage': '75'})
    assert response.status_code == 302

   
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    #Ensure the test data was deleted
    c.execute("SELECT * FROM statistic2022 WHERE moduleName='Internet of Things'")
    deletedData = c.fetchall()
    assert len(deletedData) == 0
    conn.close()


def test_deleteData(client):
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    #Clear the data
    response = client.post('/deleteData2019')

    assert response.status_code == 302

    c.execute("SELECT * FROM statistic2019")
    clearedData = c.fetchall()

    #Ensure the data has been deleted from the table
    assert len(clearedData) == 0
    conn.close()

def test_deleteDataInvalidPrivileges(client):
    with client.session_transaction() as session:
        session['user'] = "student@warwick.ac.uk"

    response = client.post('/deleteData2019')

    #Ensure user is forbidden from carrying out CRUD function
    assert response.status_code == 403



def test_signIn(client):
    with client:
        response = client.post('/signIn', data={'email': 'tutor@warwick.ac.uk', 'password': '1111'})
        #Login using correct credentials
        assert response.status_code == 200
        assert 'user' in session
        assert session['user'] == 'tutor@warwick.ac.uk'

def test_signInInvalidCredentials(client):
    with client:
        response = client.post('/signIn', data={'email': 'tutor@warwick.ac.uk', 'password': 'incorrectPassword'})
        #Login using invalid credentials
        assert b'Error: Incorrect E-Mail and/or password' in response.data
        assert 'user' not in session

def test_InPersonClassesPage(client):
    #Set the session as a tutor
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    response = client.get('/inPersonClasses2019')
    #Page loads up OK
    assert response.status_code == 200
    

    with client.session_transaction() as session:
        #Set the session as a student
        session['user'] = "student@warwick.ac.uk"

    response = client.get('/inPersonClasses2019')
    #Page loads up OK
    assert response.status_code == 200
    
    with client.session_transaction() as session:
        #Set invalid credentials
        session['user'] = "invalidCredentials@warwick.ac.uk"

    response = client.get('/inPersonClasses2019')
    #User is redirected to the login page
    assert response.status_code == 302
    assert response.location.endswith('/login')

    

        


