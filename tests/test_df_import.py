import unittest
import pandas as pd
from pitchr import Note, Score, Part, Measure
from pitchr.df_import import measures_from_dataframe

class TestDFImport(unittest.TestCase):

    def test_creates_score(self):

        harmony_df = pd.DataFrame([
            #   Pitch Number, Pitch Interval, Pitch Predictability
            [0, 0],
            [2, 2],
            [4, 2],
            [5, 1],
            [7, 2],
            [9, 2],
            [11, 2],
            [12, 1],
        ], columns=['Pitch Number', 'Pitch Interval'])

        durations = [1.0] * len(harmony_df)

        time_signature = '4/4'

        measures = [
            Measure([
                Note(0, 1.0),
                Note(2, 1.0),
                Note(4, 1.0),
                Note(5, 1.0),
            ]),

            Measure([
                Note(7, 1.0),
                Note(9, 1.0),
                Note(11, 1.0),
                Note(12, 1.0),
            ]),
        ]

        harmony_measures = measures_from_dataframe(harmony_df, durations, time_signature)

        self.assertEqual([n for measure in harmony_measures for n in measure], [n for measure in measures for n in measure])
