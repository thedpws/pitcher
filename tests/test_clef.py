import unittest

from pitchr import *


class TestClef(unittest.TestCase):

    def test_treble_clef_value_is_0(self):
        v = Clef.TREBLE.value

        self.assertEqual(v, 0)

    def test_bass_clef_value_is_1(self):
        v = Clef.BASS.value

        self.assertEqual(v, 1)
