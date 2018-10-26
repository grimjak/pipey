import json
import unittest

from project.tests.base import BaseTestCase

from utils import empty_database, create_test_skill, login

class TestSkillService(BaseTestCase):
    def setUp(self):
        super(TestSkillService, self).setUp()
        empty_database()

    def test_skills(self):
        response = self.client.get('/skills/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])