from mamba import description, before, it
from expects import expect, equal
from hashpwd import hash_password, verify_password

with description('hashpwd') as self:

    with it('password is hashed and challenged correctly'):
        hashed_pwd = hash_password("example1")
        is_verified = verify_password(hashed_pwd, "example1")
        expect(is_verified).to(equal(True))

    with it('password is hashed and challenged correctly when is wrong'):
        hashed_pwd = hash_password("example1")
        is_verified = verify_password(hashed_pwd, "example2")
        expect(is_verified).to(equal(False))
