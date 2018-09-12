from project.tests.base import BaseTestCase

from utils import create_test_user
from mongoengine.errors import NotUniqueError
import unittest


class TestPeopleModel(BaseTestCase):

    def test_add_person(self):
        person = create_test_user()
        self.assertTrue(person.id)
        self.assertTrue(person.active)
        self.assertTrue(person.password)

    def test_add_user_duplicate_username(self):
        with self.assertRaises(NotUniqueError):
            create_test_user()

    def test_passwords_are_random(self):
        user_one = create_test_user(username="userone", password='greaterthaneight')
        user_two = create_test_user(username="usertwo", password='greaterthaneight')
        self.assertNotEqual(user_one.password, user_two.password)


if __name__ == '__main__':
    unittest.main()
