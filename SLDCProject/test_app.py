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
    response = client.post('/addData2022', data={'module': 'SDLC Tutor', 
                                                    'grade': '60', 
                                                    'percentage': '80'})

    c.execute("SELECT * FROM statistic2022 WHERE moduleName='SDLC Tutor'")
    insertData = c.fetchall()
    conn.commit()
    assert insertData[0][0] == "SDLC Tutor"
    assert len(insertData) > 0
    conn.close()




def test_updateData(client):
    with client.session_transaction() as session:
        session['user'] = "tutor@warwick.ac.uk"

    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("INSERT INTO statistic2019 (moduleName, grade, percentage) VALUES (?,?,?)", 
              ('Agile Project Management', 40, 30))
    conn.commit()
    conn.close()

    # Update the sample data
    response = client.post('/updateData2019', data={'module': 'Agile Project Management', 
                                                    'grade': '50', 
                                                    'percentage': '90'})
    assert response.status_code == 302

    # Verify the data was updated
    conn = sqlite3.connect('wmgsisDB.db')
    c = conn.cursor()
    c.execute("SELECT * FROM statistic2019 WHERE moduleName='Agile Project Management'")
    updatedData = c.fetchall()
    conn.commit()
    assert len(updatedData) > 0
    assert updatedData[0][0] == "Agile Project Management"
    assert updatedData[0][1] == 50
    assert updatedData[0][2] == 90
    conn.close()



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

    # Delete the sample data
    response = client.post('/deleteModule2022', data={'module': 'Internet of Things',
                                                     'grade': '60', 
                                                     'percentage': '80'})
    assert response.status_code == 302

    # Verify the data was deleted
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
    c.execute("DELETE FROM statistic2019")
    c.execute("SELECT * FROM statistic2019")
    clearedData = c.fetchall()
    assert len(clearedData) == 0
    conn.commit()
    conn.close()