

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

        acts = [lambda: Key(*args) for args in [(0,0), (1, 0), (0,1)]]

        for act in acts:
            try:
                act()
            except Exception:
                self.fail(f'{act} raised an Exception')
    
    def test_key_str_c_major(self):

        k = str(Key.C_MAJOR)

        self.assertEqual(k, 'c \\major')

    def test_key_str_no_minors(self):

        k = str(Key.C_MINOR)

        self.assertEqual(k, 'e-flat \\major')

    def test_key_str_c_sharp_major(self):

        k = str(Key.C_SHARP_MAJOR)

        self.assertEqual(k, 'c-sharp \\major')

    def test_key_str_e_flat_major(self):

        k = str(Key.Eb_MAJOR)

        self.assertEqual(k, 'e-flat \\major')

    def test_key_equivalence(self):
        self.assertEqual(Key(sharps=6), Key(sharps=6))
