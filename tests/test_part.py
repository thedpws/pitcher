

import unittest
from pitchr import *

class TestPart(unittest.TestCase):
    
    def test_part_init_keysig_defaults_to_global(self):

        key(Key.F_MAJOR)

        p = Part()

        self.assertEqual(p.key_signature, Key.F_MAJOR)

    def test_part_init_keysig_sets(self):

        p = Part(key_signature=Key.G_MAJOR)

        self.assertEqual(p.key_signature, Key.G_MAJOR)

    def test_part_init_timesig_defaults_to_global(self):

        time(Time.CUT_TIME)

        p = Part()

        self.assertEqual(p.time_signature, Time.CUT_TIME)

    def test_part_init_timesig_sets(self):
        p = Part(time_signature=Time.CUT_TIME)
        self.assertEqual(p.time_signature, Time.CUT_TIME)

    def test_part_init_defaults_tempo_to_40(self):
        p = Part()
        self.assertEqual(p.tempo, 40)

    def test_part_init_sets_tempo(self):
        p = Part(tempo=96)
        self.assertEqual(p.tempo, 96)

    def test_part_init_pass_staffs_adds_staffs(self):
        p = Part(staffs=[s := Staff()])
        self.assertEqual(p[0], s)
