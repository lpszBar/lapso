import os
import sqlite3

import pytest


@pytest.fixture(scope='function')
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
    datafile.close()
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
    assert app_client.get('/').status_code == 200
    assert app_client.get('/logout').status_code == 302
    assert app_client.get('/').status_code != 200


def test_badly_logged_user_cannot_get_root_page(app_client, db):
    row = db.execute(
        "SELECT email FROM users"
    ).fetchone()
    user = {"email": row[0]}
    response = app_client.post(
        '/login',
        data={'email': user.get('email'), 'password': 'BAD_PWD'}
    )
    assert response.headers.get('location') == 'http://localhost/login'


# def test_user_can_delete_its_own_image(app_client, db):
#     photo_of_user1 = db.execute(
#         "SELECT id FROM photos where user_id=?", (1,)
#     ).fetchone()[0]
#     response = app_client.post(
#         '/login',
#         data={'email': 'one@email.com', 'password': 'password1'}
#     )
#     assert response.headers.get('location') == 'http://localhost/'
#     assert app_client.get('/').status_code == 200
#     print("borrando", '/delete/%s' % photo_of_user1)
# #    assert app_client.get('/delete/%s' % photo_of_user1).status_code == 302
#     photo_of_user1 = db.execute(
#         "SELECT id FROM photos where user_id=?", (1,)
#     ).fetchone()
#     assert photo_of_user1 is None
