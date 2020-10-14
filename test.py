from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('times_played'))
            self.assertIn(b'<h4>Times Played:', response.data)
            self.assertIn(b'Highscore:', response.data)

    def test_word_check(self):
        """Test to make sure the word validation is functioning as expected"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

        response = self.client.get('/check-word?word=dog')
        self.assertEqual(response.json['result'], 'not-on-board')
        
        response = self.client.get('/check-word?word=sdiwjai9djaw8dh1289d')
        self.assertEqual(response.json['result'], 'not-word')


            
