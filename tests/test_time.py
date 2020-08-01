import unittest

from pitchr import *


class TestTime(unittest.TestCase):

    def test_time_init_raises_PitcherException_on_bad_time_signature(self):

        act = lambda: Time('44')

        self.assertRaises(PitcherException, act)

    def test_time_init_accepts_good_time_signature(self):

        acts = [lambda: Time(s) for s in ['4/4', '6/4', '3/4']]

        for act in acts:
            try:
                act()
            except Exception:
                self.fail(f'{act} raised an Exception')

    def test_time_equality(self):
        self.assertEqual(Time('4/4'), Time('4/4'))
