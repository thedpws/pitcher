import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pitchr import *


class TestMeasure(unittest.TestCase):

    def test_measure_init_notes_passed_are_added(self):
        m = Measure(notes=[n := Note('A', 1.0)])
        self.assertEqual(m[0], n)

    def test_measure_notes_are_indexed_by_start_beat(self):
        m = Measure(notes=[n1 := Note('A', 1.5), n2 := Note('A5', 1.5)])
        self.assertEqual(m[1.5], n2)

    def test_measure_empty_index_raises_KeyError(self):
        m = Measure(notes=[n1 := Note('A', 1.5), n2 := Note('A5', 1.5)])

        self.assertRaises(KeyError, lambda: m[2.0])

    def test_measure_duration_returns_duration_of_measure_in_beats(self):
        m = Measure(notes=[Note('A', 0.5), Note('B', 1.5)])

        self.assertEqual(m.duration, 2.0)

    """
    def test_measure_del_replaces_note_with_rest(self):
        m = Measure(notes=[Note('A', 0.5), Note('B', 1.5)])

        del m[0]

        self.assertEqual(m[0], Rest(0.5))
    """

    def test_measure_contains(self):
        m = Measure(notes=[Note('A', 0.5), Note('B', 1.5)])
        self.assertTrue(Note('A', 0.5) in m)

    def test_measure_append_appends_notes(self):
        m = Measure()

        m.append(Note('A', 1.0))

        self.assertEqual(m[0], Note('A', 1.0))

    def test_measure_extend(self):
        m = Measure()

        m.extend([Note('A', 1.0), Note('B', 1.0)])

        self.assertEqual(m[0], Note('A', 1.0))
        self.assertEqual(m[1], Note('B', 1.0))

    def test_measure_overfill_throws_exception(self):
        time(Time.COMMON_TIME)

        m = Measure()

        m.append(Note('C', 1.0))
        m.append(Note('C', 1.0))
        m.append(Note('C', 1.0))
        m.append(Note('C', 1.0))

        def act():
            m.append(Note('C', 1.0))

        self.assertRaises(Exception, act)

    @patch('pitchr.playing.play_score')
    def test_measure_play_calls_play_score(self, play_score):
        Measure().play()

        self.assertTrue(play_score.called)

    @patch('pitchr.lyexport.show_score_png')
    def test_measure_show_calls_show_score(self, show_score):
        Measure().show()

        self.assertTrue(show_score.called)

    @patch('pitchr.lyexport.write_to_pdf')
    def test_measure_save_calls_save_score(self, save_score):
        with TemporaryDirectory() as tempdirname:
            filepath = tempdirname + '/export.pdf'
            Measure().save(filepath)
        self.assertTrue(save_score.called)
