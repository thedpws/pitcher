import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pitchr import *


class TestPart(unittest.TestCase):

    def test_part_init_keysig_defaults_to_global(self):
        key(Key.F_MAJOR)

        p = Part()

        self.assertEqual(p.key_signature, Key.F_MAJOR)

    def test_part_init_keysig_sets(self):
        p = Part(key_signature=Key.G_MAJOR)

        self.assertEqual(p.key_signature, Key.G_MAJOR)

    def test_part_keysig_is_settable(self):
        p = Part(key_signature=Key.F_MAJOR)

        p.key_signature = Key(sharps=1)
        self.assertEqual(p.key_signature, Key(sharps=1))

    def test_part_init_timesig_defaults_to_global(self):
        time(Time.CUT_TIME)

        p = Part()

        self.assertEqual(p.time_signature, Time.CUT_TIME)

    def test_part_init_timesig_sets(self):
        p = Part(time_signature=Time.CUT_TIME)
        self.assertEqual(p.time_signature, Time.CUT_TIME)

    def test_part_timesig_is_settable(self):
        p = Part(time_signature=Time.CUT_TIME)

        p.time_signature = Time('5/4')
        self.assertEqual(p.time_signature, Time('5/4'))

    def test_part_init_defaults_tempo_to_60(self):
        p = Part()
        self.assertEqual(p.tempo, 60)

    def test_part_init_sets_tempo(self):
        p = Part(tempo=96)
        self.assertEqual(p.tempo, 96)

    def test_part_tempo_is_settable(self):
        p = Part(tempo=96)

        p.tempo = 90

        self.assertEqual(p.tempo, 90)

    def test_part_init_pass_staffs_adds_staffs(self):
        p = Part(staffs=[s := Staff()])
        self.assertEqual(p[0], s)

    @patch('pitchr.playing.play_score')
    def test_play_calls_play_score(self, play_score):
        p = Part()

        p.play()

        self.assertTrue(play_score.called)

    @patch('pitchr.lyexport.show_score_png')
    def test_show_calls_show_score(self, show_score):
        p = Part()

        p.show()

        self.assertTrue(show_score.called)

    @patch('pitchr.lyexport.write_to_pdf')
    def test_save_calls_save_score(self, save_score):
        p = Part()

        with TemporaryDirectory() as tempdirname:
            filepath = tempdirname + '/export.pdf'
            p.save(filepath)

            self.assertTrue(save_score.called)

    def test_add_staff_adds_staffs(self):
        p = Part()

        p.add_staff(s := Staff())

        self.assertEqual(p[0], s)
