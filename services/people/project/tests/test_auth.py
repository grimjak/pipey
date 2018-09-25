import json

from project.tests.base import BaseTestCase
from project.tests.utils import create_test_user, empty_database

from flask import current_app


class TestAuthBlueprint(BaseTestCase):
    def setUp(self):
        super(TestAuthBlueprint, self).setUp()
        empty_database()

    def test_registered_user_login(self):
        with self.client:
            create_test_user(username='test', password='test')
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_registered_user_login_bad_password(self):
        with self.client:
            create_test_user(username='test', password='test')
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'wrong'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Password does not match')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertIn('The requested URL was not found on the server.',
                          data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        with self.client:
            create_test_user(username='test', password='test')
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(response_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        with self.client:
            create_test_user(username='test', password='test')
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(response_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        create_test_user(username='test', password='test')

        with self.client:
            resp_login = self.client.post(
                'auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            print(resp_login.data.decode())
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            print(data)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'test')
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': 'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive(self):
        create_test_user(username='test', password='test', active=False)

        with self.client:
            resp_login = self.client.post(
                'auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            print(resp_login.data.decode())
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            print(data)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_status_inactive(self):
        create_test_user(username='test', password='test', active=False)

        with self.client:
            resp_login = self.client.post(
                'auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)
