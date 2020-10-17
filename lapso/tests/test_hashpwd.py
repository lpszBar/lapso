import pytest
from hashpwd import hash_password, verify_password


def test_password_is_challenged_correctly():
    hashed_pwd = hash_password("example1")
    is_verified = verify_password(hashed_pwd, "example1")
    assert is_verified is True


def test_password_is_challenged_correctly_when_wrong():
    hashed_pwd = hash_password("example1")
    is_verified = verify_password(hashed_pwd, "example2")
    assert is_verified is not True
