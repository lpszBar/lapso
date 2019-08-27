import os
import sqlite3

import pytest


@pytest.fixture
def app_client():
    from app import app
    app = app.test_client()
    app.testing = True
    return app


@pytest.fixture(scope='function')
def db(tmpdir):
    file = os.path.join(tmpdir.strpath, "test.db")
    conn = sqlite3.connect(file)
    datafile = open("../../db/lapso.schema")
    sql = datafile.read()
    conn.executescript(sql)
    yield conn
    conn.close()


def test_logged_user_can_get_root_page_and_logout(app_client, db):
    row = db.execute(
        "SELECT email FROM users"
    ).fetchone()
    user = {"email": row[0]}
    response = app_client.post(
        '/login',
        data={'email': user.get('email'), 'password': 'password1'}
    )
    assert response.headers.get('location') == 'http://localhost/'
    response = app_client.get('/')
    assert response.status_code == 200
    response = app_client.get('/logout')
    assert response.status_code == 302
    response = app_client.get('/')
    assert response.status_code != 200


def test_badly_logged_user_cannot_get_root_page(app_client, db):
    row = db.execute(
        "SELECT email, password FROM users"
    ).fetchone()
    user = {"email": row[0]}
    response = app_client.post(
        '/login',
        data={'email': user.get('email'), 'password': 'BAD_PWD'}
    )
    assert response.headers.get('location') == 'http://localhost/login'
