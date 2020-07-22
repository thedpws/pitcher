import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pitchr import *


class TestChord(unittest.TestCase):

    def test_init_notes_passed_are_added(self):
        c = Chord(notes=[Note('A', 1.0)])

        self.assertTrue(Note('A', 1.0) in c.notes)

    def test_notes_returns_notes(self):
        c = Chord(notes=[Note('A', 1.0)])

        self.assertEqual(c.notes, [Note('A', 1.0)])

    def test_duration_is_duration_of_longest_note(self):
        c = Chord(notes=[
            Note('A', 1.0),
            Note('A', 10.0),
            Note('A', 2.0),
        ])

        self.assertEqual(c.duration, 10.0)

    def test_append_appends_note(self):
        c = Chord()

        c.append(n := Note('A', 1.0))

        self.assertTrue(n in c.notes)

    def test_remove_removes_note(self):
        c = Chord([Note('A', 1.0), Note('B', 1.0)])

        c.remove(Note('A', 1.0))

        self.assertEqual(c.notes, [Note('B', 1.0)])

    def test_clear_removes_all_notes(self):
        c = Chord([Note('A', 1.0)])
        c.clear()
        self.assertEqual(c.notes, [])

    def test_determine(self):
        c = Chord([Note('A', 1.0), Note('C5', 1.0)])
        self.assertEqual(c.determine(), ['minor third'])

    def test_major_triad(self):
        c = Chord.major_triad(Note('A', 1.5))
        self.assertEqual(c, Chord([Note('A', 1.5), Note('C#5', 1.5), Note('E5', 1.5)]))

    def test_minor_triad(self):
        c = Chord.minor_triad(Note('A', 1.5))
        self.assertEqual(c, Chord([Note('A', 1.5), Note('C5', 1.5), Note('E5', 1.5)]))

    def test_diminished_triad(self):
        c = Chord.diminished_triad(Note('A', 1.5))
        self.assertEqual(c, Chord([Note('A', 1.5), Note('C5', 1.5), Note('Eb5', 1.5)]))

    def test_augmented_triad(self):
        c = Chord.augmented_triad(Note('A', 1.5))
        self.assertEqual(c, Chord([Note('A', 1.5), Note('C#5', 1.5), Note('E#5', 1.5)]))

    def test_suspended_triad(self):
        c = Chord.suspended_triad(Note('A', 1.5))
        self.assertEqual(c, Chord([Note('A', 1.5), Note('D5', 1.5), Note('E5', 1.5)]))

    @patch('pitchr.playing.play_score')
    def test_play_calls_play_score(self, play_score):
        Chord().play()
        self.assertTrue(play_score.called)

    @patch('pitchr.lyexport.show_score_png')
    def test_show_calls_show_score(self, show_score):
        Chord().show()
        self.assertTrue(show_score.called)

    @patch('pitchr.lyexport.write_to_pdf')
    def test_save_calls_save_score(self, save_score):
        with TemporaryDirectory() as tempdirname:
            filepath = tempdirname + '/export.pdf'
            Chord().save(filepath)
        self.assertTrue(save_score.called)
