import unittest
import json

from app import app


APP_URL = 'http://127.0.0.1:5000'


class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_app_working(self):
        with self.app.app_context():
            response = self.client.get(APP_URL + '/')
            self.assertEqual(response.status_code, 200)

    def test_sport_not_exist(self):
        with self.app.app_context():
            response = self.client.get(APP_URL + '/sport/madeup')
            self.assertEqual(response.status_code, 404)

    def test_event_not_exist(self):
        with self.app.app_context():
            response = self.client.get(APP_URL + '/event/madeup')
            self.assertEqual(response.status_code, 404)

    def test_selection_not_exist(self):
        with self.app.app_context():
            response = self.client.get(APP_URL + '/selection/madeup')
            self.assertEqual(response.status_code, 404)

    def test_invalid_event_date_field(self):
        with self.app.app_context():
            response = self.client.post(APP_URL + '/event/test_event', data={'name': ['test'],
                                                                             'active': [0],
                                                                             'type': [1],
                                                                             'sport': [1],
                                                                             'status': [1],
                                                                             'scheduled_start': ['2022']})
            self.assertEqual(response.status_code, 400)

    def test_invalid_enum_value(self):
        with self.app.app_context():
            response = self.client.post(APP_URL + '/event/test_event', data={'name': ['test'],
                                                                             'active': [0],
                                                                             'type': [1],
                                                                             'sport': [1],
                                                                             'status': [12]})
            self.assertEqual(response.status_code, 400)

    def test_update_active(self):
        with self.app.app_context():
            response = self.client.put(APP_URL + '/selection/4', data={'active': [1]})
            response_event = self.client.get(APP_URL + '/event/search?id=3&active=0')
            response_sport = self.client.get(APP_URL + '/sport/search?id=2&active=0')
            response1 = response.status_code
            event_is_active_response1 = response_event.status_code
            sport_is_active_response1 = response_sport.status_code

            response = self.client.put(APP_URL + '/selection/4', data={'active': [0]})
            response_event = self.client.get(APP_URL + '/event/search?id=3&active=1')
            response_sport = self.client.get(APP_URL + '/sport/search?id=2&active=1')
            response2 = response.status_code
            event_is_active_response2 = response_event.status_code
            sport_is_active_response2 = response_sport.status_code

            self.assertEqual(response1, 200)
            self.assertEqual(response2, 200)
            self.assertEqual(event_is_active_response1, 404)
            self.assertEqual(event_is_active_response2, 404)
            self.assertEqual(sport_is_active_response1, 404)
            self.assertEqual(sport_is_active_response2, 404)


if __name__ == "__main__":
    unittest.main()