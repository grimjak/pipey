import unittest

from project import db
from project.tests.base import BaseTestCase

from utils import *

class TestPeopleModel(BaseTestCase):

    def test_add_person(self):
        person = create_test_user()
        self.assertTrue(person.id)
        self.assertTrue(person.active)