import json
import unittest

from project.tests.base import BaseTestCase

from utils import empty_database, create_test_user, create_test_users


class TestPeopleService(BaseTestCase):
    def setUp(self):
        super(TestPeopleService, self).setUp()
        print("empty db")
        empty_database()

    def test_people(self):
        response = self.client.get('/api/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_person(self):
        with self.client:
            response = self.client.post(
                '/api/people',
                data=json.dumps({
                    'username': 'bh',
                    'firstname': 'Bob',
                    'lastname': 'Holmes',
                    'address': '77 Verulam Road',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('bh', data['username'])
            self.assertIn('Bob', data['firstname'])
            self.assertIn('Holmes', data['lastname'])
            self.assertIn('77 Verulam Road', data['address'])


    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/api/people',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Missing data for required field.',
                          data['firstname'])
            self.assertIn('Missing data for required field.',
                          data['lastname'])

    def test_add_user_invalid_json_keys(self):
        with self.client:
            response = self.client.post(
                '/api/people',
                data=json.dumps({
                    'firstname': 'Bob',
                    'address': '77 Verulam Road'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Missing data for required field.', data['lastname'])

    def test_add_user_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                '/api/people',
                data=json.dumps({
                    'username': 'bh',
                    'firstname': 'Bob',
                    'lastname': 'Holmes',
                    'address': '77 Verulam Road',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
    # add tests for duplicate data

    def test_get_all_users(self):
        people = create_test_users()
        with self.client:
            response = self.client.get(
                '/api/people',
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
                '/api/people/'+str(person.id),
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
                '/api/people/blah',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('The requested URL was not found on the server.',
                          data['message'])

    def test_edit_existing_single_user(self):
        person = create_test_user()
        with self.client:
            response = self.client.put(
                '/api/people/'+str(person.id),
                data=json.dumps({'firstname': 'Steve'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Steve', data['firstname'])
            self.assertIn(person.lastname, data['lastname'])
            self.assertIn(person.address, data['address'])

    def test_edit_existing_single_user_no_data(self):
        person = create_test_user()
        with self.client:
            response = self.client.put(
                '/api/people/'+str(person.id),
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(person.username, data['username'])
            self.assertIn(person.firstname, data['firstname'])
            self.assertIn(person.lastname, data['lastname'])
            self.assertIn(person.address, data['address'])

    def test_edit_existing_single_user_invalid_data(self):
        person = create_test_user()
        with self.client:
            response = self.client.put(
                '/api/people/'+str(person.id),
                data=json.dumps({'foo': 'bar'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(person.username, data['username'])
            self.assertIn(person.firstname, data['firstname'])
            self.assertIn(person.lastname, data['lastname'])
            self.assertIn(person.address, data['address'])
            self.assertFalse('foo' in data.keys())

    def test_edit_missing_single_user(self):
        create_test_user()  # ensure there are records
        with self.client:
            response = self.client.put(
                '/api/people/09',
                data=json.dumps({
                    'firstname': 'Bob',
                    'lastname': 'Holmes',
                    'address': '77 Verulam Road'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('The requested URL was not found on the server.',
                          data['message'])

    def test_delete_single_user(self):
        person = create_test_user()
        with self.client:
            response = self.client.delete(
                'api/people/'+str(person.id),
                content_type='application/json'
            )
            # data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            response = self.client.get(
                'api/people/'+str(person.id),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 404)

    def test_delete_missing_single_user(self):
        create_test_user()  # ensure there are records
        with self.client:
            response = self.client.delete(
                'api/people/09',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('The requested URL was not found on the server.',
                          data['message'])


if __name__ == '__main__':
    unittest.main()
