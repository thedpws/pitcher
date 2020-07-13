

import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
from pitchr import *

class TestNote(unittest.TestCase):

    def test_init_sets_pitch(self):
        n = Note('A4', 1.0)
        self.assertEqual(n.pitch, 'A4')

    def test_letter(self):
        n = Note('A', 1.0)
        self.assertEqual(n.letter, 'A')

    def test_octave(self):
        n = Note('A6', 1.0)
        self.assertEqual(n.octave, 6)

    def test_octave_is_settable(self):
        n = Note('A', 1.0)
        n.octave = 3
        self.assertEqual(n.octave, 3)

    def test_octave_defaults_to_4(self):
        n = Note('A', 1.0)
        self.assertEqual(n.octave, 4)

    def test_accidentals_none(self):
        n = Note('A', 1.0)
        self.assertEqual(n.accidentals, '')

    def test_accidentals_sharp(self):
        n = Note('A#', 1.0)
        self.assertEqual(n.accidentals, '#')

    def test_accidentals_flats(self):
        n = Note('Abb', 1.0)
        self.assertEqual(n.accidentals, 'bb')

    def test_accidentals_double_sharps(self):
        n = Note('Fx', 1.0)
        self.assertEqual(n.accidentals, 'x')

    def test_accidentals_simplify(self):
        n = Note('Fxbbxbbxbb', 1.0)
        self.assertEqual(n.accidentals, '')

    def test_accidentals_wrt_key_native_dont_return(self):
        n = Note('F#', 1.0)
        self.assertEqual(n.get_accidentals_wrt_key(Key.D_MAJOR), '')

    def test_accidentals_wrt_key_foreign_return(self):
        n = Note('F#', 1.0)
        self.assertEqual(n.get_accidentals_wrt_key(Key.C_MAJOR), '#')

    def test_pitch_is_settable(self):
        n = Note('A4', 1.0)
        n.pitch = 'A5'
        self.assertEqual(n.pitch, 'A5')

    def test_duration(self):
        n = Note('A4', 1.5)
        self.assertEqual(n.duration, 1.5)

    def test_duration_is_settable(self):
        n = Note('A4', 1.5)
        n.duration = 1.0
        self.assertEqual(n.duration, 1.0)

    def test_pitch_number_C4_is_0(self):
        n = Note('C4', 1.0)
        self.assertEqual(n.pitch_number, 0)

    def test_pitch_number_C5_is_12(self):
        n = Note('C5', 1.0)
        self.assertEqual(n.pitch_number, 12)

    def test_augment(self):
        n = Note('C4', 1.0)
        n.augment()
        self.assertEqual(n.pitch, 'C#4')

    def test_diminish(self):
        n = Note('C4', 1.0)
        n.diminish()
        self.assertEqual(n.pitch, 'Cb4')

    def test_transpose(self):
        n = Note('C4', 1.0)
        n.transpose('+12')
        self.assertEqual(n.pitch_number, Note('C5', 1.0).pitch_number)

    def test_octave_up(self):
        n = Note('C4', 1.0)
        n.octave_up()
        self.assertEqual(n.pitch, 'C5')

    def test_octave_down(self):
        n = Note('C4', 1.0)
        n.octave_down()
        self.assertEqual(n.pitch, 'C3')

    @patch('pitchr.playing.play_score')
    def test_play_calls_play_score(self, play_score):
        Note('A', 1.0).play()
        self.assertTrue(play_score.called)

    @patch('pitchr.lyexport.show_score_png')
    def test_show_calls_show_score(self, show_score):
        Note('A', 1.0).show()
        self.assertTrue(show_score.called)

    @patch('pitchr.lyexport.write_to_pdf')
    def test_save_calls_save_score(self, save_score):
        with TemporaryDirectory() as tempdirname:
            filepath = tempdirname + '/export.pdf'
            Note('A', 1.0).save(filepath)
        self.assertTrue(save_score.called)
