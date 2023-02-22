import app
import sqlite3
import pytest
import unittest
import os 
from flask import session




@pytest.fixture
def client(request):
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    def teardown():
        pass 

    request.addfinalizer(teardown)
    return client

def test_addData(client):
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()


    response = client.post('/addData2019', data={'module': 'Test Data', 
                                                    'grade': '60', 
                                                    'percentage': '80'})

    assert response.status_code == 302
    conn.commit()
    c.execute("SELECT * FROM statistic2019 WHERE moduleName='Test Data'")
    insertData = c.fetchall()
    assert len(insertData) > 0
    assert insertData[0][0] == "Test Data"

    conn.close()

    
def test_addDataInvalidPrivileges(client):
    with client.session_transaction() as session:
        session['user'] = "student@warwick.ac.uk"

    response = client.post('/addData2019', data={'module': 'module', 
                                                    'grade': '60', 
                                                    'percentage': '70'})

    assert response.status_code == 403




def test_updateData(client):
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("DELETE FROM statistic2019")

    c.execute("INSERT INTO statistic2019 (moduleName, grade, percentage) VALUES (?,?,?)", 
              ('Agile Project Management', 40, 30))
    conn.commit()

    response = client.post('/updateData2019', data={'module': 'Agile Project Management', 
                                                    'grade': '50', 
                                                    'percentage': '90'})
    assert response.status_code == 302



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

    assert response.status_code == 403


def test_deleteModuleInvalidPrivileges(client):
    with client.session_transaction() as session:
        session['user'] = "student@warwick.ac.uk"

    response = client.post('/deleteModule2019', data={'module': 'Agile Project Management', 
                                                    'grade': '60', 
                                                    'percentage': '70'})

    assert response.status_code == 403



def test_deleteModule(client):
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("INSERT INTO statistic2022 (moduleName, grade, percentage) VALUES (?,?,?)", 
              ('Internet of Things', 90, 75))
    c.execute("SELECT * FROM statistic2022 WHERE moduleName='Internet of Things'")
    insertData = c.fetchall()
    assert len(insertData) > 0
    conn.commit()
    conn.close()

  
    response = client.post('/deleteModule2022', data={'module': 'Internet of Things',
                                                     'grade': '90', 
                                                     'percentage': '75'})
    assert response.status_code == 302

   
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2022 WHERE moduleName='Internet of Things'")
    deletedData = c.fetchall()
    assert len(deletedData) == 0
    conn.close()


def test_deleteData(client):
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()

    response = client.post('/deleteData2019')

    assert response.status_code == 302

    c.execute("SELECT * FROM statistic2019")
    clearedData = c.fetchall()
    assert len(clearedData) == 0
    conn.close()

def test_deleteDataInvalidPrivileges(client):
    with client.session_transaction() as session:
        session['user'] = "student@warwick.ac.uk"

    response = client.post('/deleteData2019')

    assert response.status_code == 403