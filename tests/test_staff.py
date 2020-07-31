import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pitchr import *


class TestStaff(unittest.TestCase):

    def test_init_defaults_clef_to_treble(self):
        self.assertEqual(Staff().clef, Clef.TREBLE)

    def test_init_defaults_voice_to_piano(self):
        self.assertEqual(Staff().voice, Voice.PIANO)

    def test_init_measures_passed_are_added(self):
        s = Staff(measures=[m := Measure()])
        self.assertEqual(s[0], m)

    def test_init_measures_passed_are_added(self):
        s = Staff(measures=[m := Measure()])

        self.assertEqual(s[0], m)

    def test_large_measure_index_appends_new_measures(self):
        s = Staff()

        def act():
            _ = s[100]

        try:
            act()
        except Exception:
            self.fail()

    def test_voice_is_gettable(self):
        s = Staff()

        def act():
            _ = s.voice

        try:
            act()
        except Exception:
            self.fail()

    def test_voice_is_settable(self):
        s = Staff()

        def act():
            s.voice = Voice.PIANO

        try:
            act()
        except Exception:
            self.fail()

    def test_clef_is_gettable(self):
        s = Staff()

        def act():
            _ = s.clef

        try:
            act()
        except Exception:
            self.fail()

    def test_clef_is_settable(self):
        s = Staff()

        def act():
            s.clef = Clef.BASS

        try:
            act()
        except Exception:
            self.fail()

    @patch('pitchr.playing.play_score')
    def test_play_calls_play_score(self, play_score):
        Staff().play()

        self.assertTrue(play_score.called)

    @patch('pitchr.lyexport.show_score_png')
    def test_show_calls_show_score_png(self, show_score):
        Staff().show()

        self.assertTrue(show_score.called)

    @patch('pitchr.lyexport.write_to_pdf')
    def test_save_calls_write_to_pdf(self, write_to_pdf):
        with TemporaryDirectory() as tempdirname:
            filepath = tempdirname + '/export.pdf'

            Staff().save(filepath)

        self.assertTrue(write_to_pdf.called)
