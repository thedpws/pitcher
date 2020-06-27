import unittest
from music import _Pitch


class TestPitch(unittest.TestCase):
    def test_getters_work(self):
        # arrange

        p = _Pitch('A', 'bb', 4)

        # act
        l = p.letter
        accs = p.accidentals
        o = p.octave

        # assert
        self.assertEqual(l, 'A')
        self.assertEqual(accs, 'bb')
        self.assertEqual(o, 4)

    def test_pitch_to_int(self):
        # arrange
        p = _Pitch('A', 'bb', 4)

        # act
        i = int(p)

        # assert
        self.assertEqual(i, -5)

    def test_accidental_offset_flats(self):

        # arrange
        p = _Pitch('C', 'bbbbbbbbbb', 4)

        # act
        accidentals = p.accidentals

        # assert
        self.assertEqual(accidentals, 'bbbbbbbbbb')

    def test_accidental_offset_sharp(self):

        # arrange
        p = _Pitch('C', '#', 4)

        # act
        accidentals = p.accidentals

        # assert
        self.assertEqual(accidentals, '#')

    def test_accidental_offset_double_sharp(self):

        # arrange
        p = _Pitch('C', '##', 4)

        # act
        accidentals = p.accidentals

        # assert
        self.assertEqual(accidentals, 'X')
