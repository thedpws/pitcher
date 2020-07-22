import unittest

from pitchr import *


class TestKey(unittest.TestCase):

    def test_key_fails_on_bad_key_signature_both_flats_and_sharps(self):
        act = lambda: Key(flats=1, sharps=1)

        self.assertRaises(PitcherException, act)

    def test_key_fails_more_than_7_flats(self):
        act = lambda: Key(flats=8)
        self.assertRaises(PitcherException, act)

    def test_key_fails_more_than_7_sharps(self):
        act = lambda: Key(sharps=8)
        self.assertRaises(PitcherException, act)

    def test_key_fails_on_less_than_0_flats(self):
        act = lambda: Key(flats=-1)
        self.assertRaises(PitcherException, act)

    def test_key_fails_on_less_than_0_sharps(self):
        act = lambda: Key(sharps=-1)
        self.assertRaises(PitcherException, act)

    def test_key_allows_good_key_signatures(self):

        acts = [lambda: Key(*args) for args in [(0, 0), (1, 0), (0, 1)]]

        for act in acts:
            try:
                act()
            except Exception:
                self.fail(f'{act} raised an Exception')

    def test_key_str_c_major(self):

        k = str(Key.C_MAJOR)

        self.assertEqual(k, 'C major')

    def test_key_str_no_minors(self):

        k = str(Key.C_MINOR)

        self.assertEqual(k, 'Eb major')

    def test_key_str_c_sharp_major(self):

        k = str(Key.C_SHARP_MAJOR)

        self.assertEqual(k, 'C# major')

    def test_key_str_e_flat_major(self):

        k = str(Key.Eb_MAJOR)

        self.assertEqual(k, 'Eb major')

    def test_key_equivalence(self):
        self.assertEqual(Key(sharps=6), Key(sharps=6))

    def test_major_scale(self):
        scale = Key.Eb_MAJOR.major_scale
        self.assertEqual(scale, ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D', 'Eb'])

    def test_major_tonic(self):
        self.assertEqual(Key.C_MAJOR.major_tonic, 'C')
        self.assertEqual(Key.D_MAJOR.major_tonic, 'D')
        self.assertEqual(Key.Db_MAJOR.major_tonic, 'Db')
        self.assertEqual(Key.G_MAJOR.major_tonic, 'G')
        self.assertEqual(Key.A_MINOR.major_tonic, 'C')

    def test_contains_letter(self):
        self.assertTrue('E' in Key.C_MAJOR)

    def test_contains_letter_with_octave(self):
        self.assertTrue('E5' in Key.C_MAJOR)

    def test_contains_letter_with_accidental(self):
        self.assertFalse('C#' in Key.C_MAJOR)
        self.assertTrue('C#' in Key.A_MAJOR)

    def test_contains_letter_with_accidental_and_octave(self):
        self.assertFalse('C#5' in Key.C_MAJOR)
        self.assertTrue('C#5' in Key.A_MAJOR)

    def test_contains_note(self):
        self.assertFalse(Note('C#5', 1.0) in Key.C_MAJOR)
        self.assertTrue(Note('C#5', 1.0) in Key.A_MAJOR)
