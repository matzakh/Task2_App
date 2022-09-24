import unittest

from app import app


APP_URL = 'localhost:5000'


class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

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


if __name__ == "__main__":
    unittest.main()