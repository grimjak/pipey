from project.tests.base import BaseTestCase
from utils import create_test_skill, empty_database
from mongoengine.errors import NotUniqueError
import unittest


class TestSkillModel(BaseTestCase):

    def test_add_skill(self):
        skill = create_test_skill()
        self.assertTrue(skill.id)
        self.assertTrue(skill.name)
        self.assertTrue(skill.level)
        self.assertTrue(skill.description)

    def test_add_skill_duplicate(self):
        with self.assertRaises(NotUniqueError):
            create_test_skill()