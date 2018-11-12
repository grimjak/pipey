from project.tests.base import BaseTestCase

from utils import create_test_task, empty_database
from mongoengine.errors import NotUniqueError
import unittest


class TestPeopleModel(BaseTestCase):

    def test_add_task(self):
        task = create_test_task()
        self.assertTrue(task.id)
        self.assertTrue(task.status)
        self.assertTrue(task.description)
        self.assertTrue(task.name)


if __name__ == '__main__':
    unittest.main()
