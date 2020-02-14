import pytest


@pytest.fixture
def app_client():
    from app import app
    app = app.test_client()
    app.testing = True
    return app


def test_root_page_needs_login(app_client):
    assert app_client.get('/').status_code == 302


def test_root_page_does_not_accept_post(app_client):
    assert app_client.post('/').status_code == 405


def test_invalid_url_is_not_found(app_client):
    assert app_client.post('/sadfasdf').status_code == 404


def test_get_upload_page_needs_login(app_client):
    assert app_client.get('/upload').status_code == 302


def test_post_upload_page_needs_login(app_client):
    assert app_client.post('/upload').status_code == 302


def test_get_delete_page_needs_login(app_client):
    assert app_client.get('/delete/123').status_code == 302


def test_get_delete_page_needs_login(app_client):
    assert app_client.post('/delete/123').status_code == 405


def test_get_delete_wrong_url_is_not_found(app_client):
    assert app_client.get('/delete/').status_code == 404
    assert app_client.get('/delete').status_code == 404
