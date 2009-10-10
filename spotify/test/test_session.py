
import unittest
import threading

from spotify import client
from spotify import _mockspotify
from spotify._mockspotify import mock_track, mock_album

client.spotify = _mockspotify

class BaseMockClient(client.Client):

    cache_location = "/foo"
    settings_location = "/foo"
    application_key = "appkey_good"
    user_agent = "user_agent_foo"
    username = "username_good"
    password = "password_good"

    def __init__(self):
        self.awoken = threading.Event() # used to block until awoken

class TestSession(unittest.TestCase):

    def test_initialisation(self):
        class MockClient(BaseMockClient):
            def logged_in(self, session, error):
                print "MockClient: logged_in"
                username = session.username()
                self.found_username = username
                session.logout()
                self.disconnect()

        c = MockClient()
        c.connect()
        self.assertEqual(c.username, c.found_username)

    def test_load(self):
        class MockClient(BaseMockClient):
            def logged_in(self, session, error):
                print "MockClient: logged_in"
                track = mock_track("foo", 0, mock_album(), 0, 0, 0, 0, 0, 1)
                session.load(track)
                session.play(True)
                session.logout()
                self.disconnect()

            def music_delivery(self, sess, mformat, frames):
                print "MUSIC!"

        c = MockClient()
        c.connect()


