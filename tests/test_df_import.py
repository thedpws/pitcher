import unittest
import pandas as pd
from pitchr import Note, Score, Part, Measure, Rest
from pitchr.df_import import measures_from_ml_output

class TestDFImport(unittest.TestCase):

    def test_creates_score(self):

        pitches = [0, 2, 4, 5, 7, 9, 11, 12]

        durations = [1.0] * len(pitches)
        durations[5] *= -1

        time_signature = '4/4'


        # Act
        harmony_measures = measures_from_ml_output(pitches, durations, time_signature)

        # Assert
        measures = [
            Measure([
                Note(0, 1.0),
                Note(2, 1.0),
                Note(4, 1.0),
                Note(5, 1.0),
            ]),

            Measure([
                Note(7, 1.0),
                Rest(1.0),
                Note(11, 1.0),
                Note(12, 1.0),
            ]),
        ]

        self.assertEqual([n for measure in harmony_measures for n in measure], [n for measure in measures for n in measure])
