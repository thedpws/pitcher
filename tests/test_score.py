import os
import tempfile
import unittest
from unittest.mock import patch

from pitchr import *


class TestScore(unittest.TestCase):

    def test_composer_is_property(self):
        s = Score(author='AZ Vasquez')

        composer = s.composer

        self.assertEqual(composer, 'AZ Vasquez')

        def act():
            s.composer = 'AZ Velasquez'

        self.assertRaises(Exception, act)

    def test_author_is_property(self):
        s = Score(author='AZ Vasquez')

        author = s.author

        self.assertEqual(author, 'AZ Vasquez')

        def act():
            s.author = 'AZ Velasquez'

        self.assertRaises(Exception, act)

    def test_title_is_property(self):
        s = Score(title='AZ Vasquez')

        title = s.title

        self.assertEqual(title, 'AZ Vasquez')

        def act():
            s.title = 'AZ Velasquez'

        self.assertRaises(Exception, act)

    def test_add_parts_adds_part(self):
        s = Score()
        s.add_part(p := Part())

        self.assertEqual(s[0], p)

    def test_init_parts_passed_adds_part(self):
        s = Score(parts=[p := Part()])

        self.assertEqual(s[0], p)

    @patch('pitchr.playing.play_score')
    def test_play_calls_play_score(self, play_score):
        s = Score()
        s.play()

        self.assertTrue(play_score.called)

    @patch('pitchr.lyexport.show_score_png')
    def test_show_calls_show_score(self, show_score_png):
        s = Score()
        s.show()

        self.assertTrue(show_score_png.called)

    def test_save_creates_pdf(self):
        s = Score()
        s.add_part(Part([Staff([Measure([Note('A', 1.0)])])]))
        with tempfile.TemporaryDirectory() as tempdirname:
            filepath = tempdirname + '/export.pdf'
            s.save(filepath)
            self.assertTrue(os.path.exists(filepath))
