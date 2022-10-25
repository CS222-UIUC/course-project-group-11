""" Modules required to handle the tests """
import pytest
from app import app

@pytest.fixture(scope='module')
def test_client():
    """ Set up a client """
    flask_app = app
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client

def test_deadend_page_get(test_client):
    """ See if the '/temp' get request will take us to the dead-end page """
    res = test_client.get('/temp')
    assert res.status_code == 200
    assert b"Your Friends" in res.data
    assert b"ClassKonnect" in res.data

def test_deadend_page_post(test_client):
    """ See if the '/temp' post request will take us nowhere but the 405 error """
    res = test_client.post('/temp')
    assert res.status_code == 405
    assert b"Your Friends" not in res.data
    assert b"ClassKonnect" not in res.data

def test_home_page_get(test_client):
    """ See if the '/' get request will take us to the login/signup page """
    res = test_client.get('/')
    assert res.status_code == 200
    assert b"Welcome! Please log in or sign up!" in res.data
    assert b"If you already have signed up:" in res.data
    assert b"If you have not, please sign up from the form below!" in res.data
    assert b"Form" in res.data

def test_home_page_post(test_client):
    """ See if the '/' post request will take us nowhere but the 405 error """
    res = test_client.post('/')
    assert res.status_code == 405
    assert b"Your Friends" not in res.data
    assert b"ClassKonnect" not in res.data

def test_user_page_get(test_client):
    """ See if the '/main' get request will take us nowhere but the 405 error
    due to the nature of the website at the moment """
    res = test_client.get('/main')
    assert res.status_code == 405
    assert b"Your Friends" not in res.data
    assert b"ClassKonnect" not in res.data

def test_user_page_post(test_client):
    """ See if the '/main' post request will take us nowhere but the 400 error
    due to the nature of the website at the moment """
    res = test_client.post('/main')
    assert res.status_code == 400
    assert b"Your Friends" not in res.data
    assert b"ClassKonnect" not in res.data
