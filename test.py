import unittest
from dotenv import load_dotenv
from unittest.mock import patch
from app import socketio

def mocked_db_create_all(flaskapp):
    pass

with patch('flask_sqlalchemy.SQLAlchemy.create_all', mocked_db_create_all):
    import app

class MockedQuery:

    def all(self):
        return []

class TestApp(unittest.TestCase):
    def setUp(self):
        self.create_event_mock_args = [
            {
                "input": {
                    "owner": "owner",
                    "title": "title",
                    "type": "type",
                    "location": "location",
                    "time": "time",
                    "description": "description"
                }
            }
        ]

        self.google_login_mock_args = [
            {
                "user": {
                    "email": "email",
                    "name": "name",
                    "bio": "bio",
                    "profile_picture": "profile_picture",
                    "token": "token",
                    "picture": "picture",
                }
            }
        ]

    def db_commit_mock(self):
        pass

    def db_query_mock(self, something):
        return MockedQuery()

    def test_example(self):
        for test in self.create_event_mock_args:
            with patch('sqlalchemy.orm.session.Session.commit', self.db_commit_mock):
                with patch('sqlalchemy.orm.session.Session.query', self.db_query_mock):
                    app.create_event(test["input"])

    def test_google_login(self):
        for test in self.google_login_mock_args:
            with patch('sqlalchemy.orm.session.Session.commit', self.db_commit_mock):
                with patch('sqlalchemy.orm.session.Session.query', self.db_query_mock):
                    app.on_google_login(test["user"])

class TestSocketIO(unittest.TestCase):
    def setUp(self):
        self.connect_user_mock = [
            {
                "data": {
                    "socketID": "socketid",
                    "name": "name"
                }
            }
        ]

    def test_connect(self):
        client1 = socketio.test_client(app.app)
        client2 = socketio.test_client(app.app)
        self.assertTrue(client1.is_connected())
        self.assertTrue(client2.is_connected())
        self.assertNotEqual(client1.sid, client2.sid)

    def test_disconnect(self):
        client = socketio.test_client(app.app)
        client.disconnect()

    def test_emit(self):
        socketio_test_client = socketio.test_client(app.app)
        for test in self.connect_user_mock:
            app.connect_user_id(test["data"])
            self.assertTrue(socketio_test_client.is_connected())


class LocationResponse:
    def __init__(self, location):
        self.location = location

class TimeResponse:
    def __init__(self, time):
        self.time = time

class DescriptionResponse:
    def __init__(self, description):
        self.description = description

if __name__ == "__main__":
    unittest.main()