import json
import unittest

from project.tests.base import BaseTestCase

from utils import empty_database, create_test_skill, create_test_skills, login

class TestSkillService(BaseTestCase):
    def setUp(self):
        super(TestSkillService, self).setUp()
        empty_database()

    @login(admin=True)
    def test_add_skill(token, self):
        with self.client:
            response = self.client.post(
                '/people/skills',
                data=json.dumps({
                    'name': 'lighting',
                    'level': 'junior',
                    'description': 'lighting individual shots'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('lighting', data['name'])
            self.assertIn('junior', data['level'])
            self.assertIn('lighting individual shots', data['description'])

    @login(admin=True)
    def test_add_skill_invalid_json(token, self):
        with self.client:
            response = self.client.post(
                '/people/skills',
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Missing data for required field.',
                          data['name'])
            self.assertIn('Missing data for required field.',
                          data['level'])

    @login(admin=True)
    def test_add_skill_invalid_json_keys(token, self):
        with self.client:
            response = self.client.post(
                '/people/skills',
                data=json.dumps({
                    'name': 'lighting',
                    'description': 'lighting individual shots'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Missing data for required field.', data['level'])

    @login(active=False)
    def test_add_skill_inactive(token, self):
        with self.client:
            response = self.client.post(
                '/people/skills',
                data=json.dumps({
                    'name': 'lighting',
                    'level': 'junior',
                    'description': 'lighting individual shots'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    @login
    def test_add_skill_not_admin(token, self):
        with self.client:
            response = self.client.post(
                '/people/skills',
                data=json.dumps({
                    'name': 'lighting',
                    'level': 'junior',
                    'description': 'lighting individual shots'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'You do not have permission to do that.')
            self.assertEqual(response.status_code, 401)

    def test_get_all_skills(self):
        skills = create_test_skills()
        with self.client:
            response = self.client.get(
                '/people/skills',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)
            for skill, d in zip(skills, data):
                self.assertIn(skill.name, d['name'])
                self.assertIn(skill.level, d['level'])
                self.assertIn(skill.name, d['name'])
                self.assertIn(skill.level, d['level'])


if __name__ == '__main__':
    unittest.main()
