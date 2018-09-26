from project.tests.base import BaseTestCase

from utils import create_test_user, empty_database
from mongoengine.errors import NotUniqueError
import unittest


class TestPeopleModel(BaseTestCase):

    def test_add_person(self):
        person = create_test_user()
        self.assertTrue(person.id)
        self.assertTrue(person.active)
        self.assertTrue(person.password)
        self.assertFalse(person.admin)

    def test_add_user_duplicate_username(self):
        with self.assertRaises(NotUniqueError):
            create_test_user()

    def test_passwords_are_random(self):
        user_one = create_test_user(
            username="userone",
            password='greaterthaneight')
        user_two = create_test_user(
            username="usertwo",
            password='greaterthaneight')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        empty_database()
        user = create_test_user()
        auth_token = user.encode_auth_token(user.username)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        empty_database()
        user = create_test_user()
        auth_token = user.encode_auth_token(user.username)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(user.decode_auth_token(auth_token), user.username)


if __name__ == '__main__':
    unittest.main()
