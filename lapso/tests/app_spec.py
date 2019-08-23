from mamba import description, before, it
from expects import expect, equal
from app import app

with description('whatever') as self:

    with before.each:
        self.app = app.test_client()
        self.app.testing = True

    with it('GET / returns 403'):
        response = self.app.get('/')
        expect(response.status_code).to(equal(403))

    with it('POST / returns 405'):
        response = self.app.post('/')
        expect(response.status_code).to(equal(405))

    with it('GET /asdf) returns 404'):
        response = self.app.get('/asdf')
        expect(response.status_code).to(equal(404))

    with it('GET (/upload) returns 403'):
        response = self.app.get('/upload')
        expect(response.status_code).to(equal(403))

    with it('POST (/upload) with no payload returns 403'):
        response = self.app.post('/upload')
        expect(response.status_code).to(equal(403))

    with it('get (/delete/33) returns 403'):
        response = self.app.get('/delete/33')
        expect(response.status_code).to(equal(403))

    with it('post (/delete/33) returns 405'):
        response = self.app.post('/delete/33')
        expect(response.status_code).to(equal(405))

    with it('get (/delete/) returns 404'):
        response = self.app.get('/delete/')
        expect(response.status_code).to(equal(404))

    with it('get (/delete) returns 404'):
        response = self.app.get('/delete')
        expect(response.status_code).to(equal(404))
