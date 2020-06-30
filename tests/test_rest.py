

import unittest
from unittest.mock import patch
from pitchr import *

class TestNote(unittest.TestCase):

    def test_init_sets_duration(self):
        r = Rest(1.0)
        self.assertEqual(r.duration, 1.0)

    def test_letter_is_none(self):
        r = Rest(1.0)
        self.assertEqual(r.letter, None)

    def test_set_letter_raises_exception(self):
        r = Rest(1.0)
        def act():
            r.letter = 'A'
        self.assertRaises(PitcherException, act)

    def test_octave_is_none(self):
        r = Rest(1.0)
        self.assertEqual(r.octave, None)

    def test_set_octave_raises_exception(self):
        r = Rest(1.0)
        def act():
            r.octave = 4
        self.assertRaises(PitcherException, act)

    def test_accidentals_is_none(self):
        r = Rest(1.0)
        self.assertEqual(r.accidentals, None)

    def test_set_accidentals_raises_exception(self):
        r = Rest(1.0)
        def act():
            r.accidentals = '#'
        self.assertRaises(PitcherException, act)

    def test_pitch_number_is_none(self):
        r = Rest(1.0)
        self.assertEqual(r.pitch_number, None)

    def test_augment_raises_exception(self):
        r = Rest(1.0)
        self.assertRaises(PitcherException, r.augment)

    def test_diminish_raises_exception(self):
        r = Rest(1.0)
        self.assertRaises(PitcherException, r.diminish)

    def test_octave_up_raises_exception(self):
        r = Rest(1.0)
        self.assertRaises(PitcherException, r.octave_up)

    def test_octave_down_raises_exception(self):
        r = Rest(1.0)
        self.assertRaises(PitcherException, r.octave_down)

    def test_transpose_raises_exception(self):
        r = Rest(1.0)
        self.assertRaises(PitcherException, lambda: r.transpose('+1'))

    def test_accidentals_none(self):
        r = Rest(1.0)
        self.assertEqual(r.accidentals, '')

    def test_accidentals_sharp(self):
        r = Rest(1.0)
        self.assertEqual(r.accidentals, '#')

    def test_accidentals_flats(self):
        r = Rest(1.0)
        self.assertEqual(r.accidentals, 'bb')

    def test_accidentals_double_sharps(self):
        r = Rest(1.0)
        self.assertEqual(r.accidentals, 'x')

    def test_accidentals_simplify(self):
        r = Rest(1.0)
        self.assertEqual(r.accidentals, '')

    def test_pitch_is_settable(self):
        r = Rest(1.0)
        r.pitch = 'A5'
        self.assertEqual(r.pitch, 'A5')

    def test_duration(self):
        r = Rest(1.5)
        self.assertEqual(r.duration, 1.5)

    def test_duration_is_settable(self):
        r = Rest(1.5)
        r.duratior = 1.0
        self.assertEqual(r.duration, 1.5)

    def test_pitch_number_C4_is_0(self):
        r = Rest(1.0)
        self.assertEqual(r.pitch_number, 0)

    def test_pitch_number_C5_is_12(self):
        r = Rest(1.0)
        self.assertEqual(r.pitch_number, 12)

    def test_augment(self):
        r = Rest(1.0)
        r.augment()
        self.assertEqual(r.pitch, 'C#4')

    def test_diminish(self):
        r = Rest(1.0)
        r.diminish()
        self.assertEqual(r.pitch, 'Cb4')

    def test_transpose(self):
        r = Rest(1.0)
        r.transpose(12)
        self.assertEqual(r.pitch, 'C5')

    def test_octave_up(self):
        r = Rest(1.0)
        r.octave_up()
        self.assertEqual(r.pitch, 'C5')

    def test_octave_down(self):
        r = Rest(1.0)
        r.octave_down()
        self.assertEqual(r.pitch, 'C3')

    @patch('pitchr.playing.play_score')
    def test_play_calls_play_score(self, play_score):
        Rest(1.0).play()
        self.assertTrue(play_score.called)

    @patch('pitchr.lyexport.show_score_png')
    def test_show_calls_show_score(self, show_score):
        Rest(1.0).show()
        self.assertTrue(show_score.called)

    @patch('pitchr.lyexport.write_to_pdf')
    def test_save_calls_save_score(self, save_score):
        with TemporaryDirectory() as tempdirname:
            filepath = tempdirname + '/export.pdf'
            Rest(1.0).save(filepath)
        self.assertTrue(save_score.called)
