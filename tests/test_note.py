import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pitchr import *
from pitchr.music import _Pitch

FLAT = _Pitch.FLAT
SHARP = _Pitch.SHARP
DOUBLE_SHARP = _Pitch.DOUBLE_SHARP


class TestNote(unittest.TestCase):

    def test_init_sets_pitch(self):
        pitch = 'A4'
        n = Note(pitch, 1.0)
        self.assertEqual(n.pitch, pitch)

    def test_letter(self):
        a = 'A'
        n = Note(a, 1.0)
        self.assertEqual(n.letter, a)

    def test_octave(self):
        octave = 6
        n = Note(f'A{octave}', 1.0)
        self.assertEqual(n.octave, octave)

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
        n = Note(f'A{SHARP}', 1.0)
        self.assertEqual(n.accidentals, SHARP)

    def test_accidentals_flats(self):
        dblflat = f"{FLAT}{FLAT}"
        n = Note(f'A{dblflat}', 1.0)
        self.assertEqual(n.accidentals, dblflat)

    def test_accidentals_double_sharps(self):
        n = Note(f'F{DOUBLE_SHARP}', 1.0)
        self.assertEqual(n.accidentals, DOUBLE_SHARP)

    def test_accidentals_simplify(self):
        n = Note('Fxbbxbbxbb', 1.0)
        self.assertEqual(n.accidentals, '')

    def test_accidentals_wrt_key_native_dont_return(self):
        n = Note(f'F{SHARP}', 1.0)
        self.assertEqual(n.get_accidentals_wrt_key(Key.D_MAJOR), '')

    def test_accidentals_wrt_key_foreign_return(self):
        n = Note(f'F{SHARP}', 1.0)
        self.assertEqual(n.get_accidentals_wrt_key(Key.C_MAJOR), SHARP)

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
        self.assertEqual(n.pitch, f'C{SHARP}4')

    def test_diminish(self):
        n = Note('C4', 1.0)
        n.diminish()
        self.assertEqual(n.pitch, f'C{FLAT}4')

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

    def test_set_pitch_number_sets(self):
        n = Note('C4', 1.0)

        self.assertEqual('C4', str(n.pitch))
        n.pitch_number = 3

        self.assertEqual('D#4', str(n.pitch))

    def test_constructor_pitch_number(self):
        n = Note(20, 1.0)

        self.assertEqual('G#5', str(n.pitch))

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

