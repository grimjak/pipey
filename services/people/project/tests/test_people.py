import json
import unittest

from project.tests.base import BaseTestCase

from utils import empty_database, create_test_user, create_test_users, login


class TestPeopleService(BaseTestCase):
    def setUp(self):
        super(TestPeopleService, self).setUp()
        empty_database()

    def test_people(self):
        response = self.client.get('/people/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    @login(admin=True)
    def test_add_person(token, self):
        with self.client:
            response = self.client.post(
                '/people/people',
                data=json.dumps({
                    'username': 'bh',
                    'firstname': 'Bob',
                    'lastname': 'Holmes',
                    'address': '77 Verulam Road',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('bh', data['username'])
            self.assertIn('Bob', data['firstname'])
            self.assertIn('Holmes', data['lastname'])
            self.assertIn('77 Verulam Road', data['address'])

    @login(True)
    def test_add_user_invalid_json(token, self):
        with self.client:
            response = self.client.post(
                '/people/people',
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Missing data for required field.',
                          data['firstname'])
            self.assertIn('Missing data for required field.',
                          data['lastname'])

    @login(admin=True)
    def test_add_user_invalid_json_keys(token, self):
        with self.client:
            response = self.client.post(
                '/people/people',
                data=json.dumps({
                    'firstname': 'Bob',
                    'address': '77 Verulam Road'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Missing data for required field.', data['lastname'])

    @login(admin=True)
    def test_add_user_invalid_json_keys_no_password(token, self):
        with self.client:
            response = self.client.post(
                '/people/people',
                data=json.dumps({
                    'username': 'bh',
                    'firstname': 'Bob',
                    'lastname': 'Holmes',
                    'address': '77 Verulam Road',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])

    @login(active=False)
    def test_add_user_inactive(token, self):
        with self.client:
            response = self.client.post(
                '/people/people',
                data=json.dumps({
                    'username': 'bh',
                    'firstname': 'Bob',
                    'lastname': 'Holmes',
                    'address': '77 Verulam Road',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    @login
    def test_add_user_not_admin(token, self):
        with self.client:
            response = self.client.post(
                '/people/people',
                data=json.dumps({
                    'username': 'bh',
                    'firstname': 'Bob',
                    'lastname': 'Holmes',
                    'address': '77 Verulam Road',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'You do not have permission to do that.')
            self.assertEqual(response.status_code, 401)

    def test_get_all_users(self):
        people = create_test_users()
        with self.client:
            response = self.client.get(
                '/people/people',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)
            for person, d in zip(people, data):
                self.assertIn(person.username, d['username'])
                self.assertIn(person.firstname, d['firstname'])
                self.assertIn(person.lastname, d['lastname'])
                self.assertIn(person.address, d['address'])

    def test_get_single_user(self):
        person = create_test_user()
        with self.client:
            response = self.client.get(
                '/people/people/'+str(person.id),
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(person.username, data['username'])
            self.assertIn(person.firstname, data['firstname'])
            self.assertIn(person.lastname, data['lastname'])
            self.assertIn(person.address, data['address'])

    def test_get_single_user_no_id(self):
        with self.client:
            response = self.client.get(
                '/people/people/blah',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('The requested URL was not found on the server.',
                          data['message'])

    @login(admin=True)
    def test_edit_existing_single_user(token, self):
        person = create_test_user()
        with self.client:
            response = self.client.put(
                '/people/people/'+str(person.id),
                data=json.dumps({'firstname': 'Steve'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Steve', data['firstname'])
            self.assertIn(person.lastname, data['lastname'])
            self.assertIn(person.address, data['address'])

    @login(admin=True)
    def test_edit_existing_single_user_no_data(token, self):
        person = create_test_user()
        with self.client:
            response = self.client.put(
                '/people/people/'+str(person.id),
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(person.username, data['username'])
            self.assertIn(person.firstname, data['firstname'])
            self.assertIn(person.lastname, data['lastname'])
            self.assertIn(person.address, data['address'])

    @login(admin=True)
    def test_edit_existing_single_user_invalid_data(token, self):
        person = create_test_user()
        with self.client:
            response = self.client.put(
                '/people/people/'+str(person.id),
                data=json.dumps({'foo': 'bar'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(person.username, data['username'])
            self.assertIn(person.firstname, data['firstname'])
            self.assertIn(person.lastname, data['lastname'])
            self.assertIn(person.address, data['address'])
            self.assertFalse('foo' in data.keys())

    @login(admin=True)
    def test_edit_missing_single_user(token, self):
        create_test_user()  # ensure there are records
        with self.client:
            response = self.client.put(
                '/people/people/09',
                data=json.dumps({
                    'firstname': 'Bob',
                    'lastname': 'Holmes',
                    'address': '77 Verulam Road'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('The requested URL was not found on the server.',
                          data['message'])

    @login(admin=True)
    def test_delete_single_user(token, self):
        person = create_test_user()
        with self.client:
            response = self.client.delete(
                'people/people/'+str(person.id),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            # data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            response = self.client.get(
                'people/people/'+str(person.id),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 404)

    @login(admin=True)
    def test_delete_missing_single_user(token, self):
        create_test_user()  # ensure there are records
        with self.client:
            response = self.client.delete(
                'people/people/09',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('The requested URL was not found on the server.',
                          data['message'])


if __name__ == '__main__':
    unittest.main()
