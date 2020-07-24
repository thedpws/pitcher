import unittest
from pitchr.music import *

import pandas as pd

from pitchr.predict import tag_predictability


class TestPredictability(unittest.TestCase):

    def test_predictability(self):

        melody = [
            Note('C', 1.0),  # Predictability: 0.0
            Note('D', 1.0),  # 0.0
            Note('E', 1.0),  # 0.0

            Note('C', 1.0),  # 0.0
            Note('D', 1.0),  # 1.0
            Note('E', 1.0),  # 1.0

            Note('C', 1.0),  # 1.0
            Note('D', 1.0),  # 1.0
            Note('G', 1.0),  # 0.0
            Note('F', 1.0),  # 0.0
            Note('E', 1.0),  # 0.0

            Note('C', 1.0),  # 1.0
            Note('D', 1.0),  # 1.0
            Note('E', 1.0),  # 0.67
            Note('C', 1.0),  # 1.0
            Note('D', 1.0),  # 1.0
            Note('G', 1.0),  # 0.25
            Note('C5', 1.0)  # 0.0
        ]

        df = pd.DataFrame([
            {
                'Key': 'C',
                'Clef': 'G',
                'Letter': n.letter,
                'Octave': n.octave,
                'Accidental': n.accidentals,
                'Duration': n.duration,
                'Pitch Number': n.pitch_number
            } for n in melody
        ])

        # Act
        tag_predictability(df)

        # Assert

        self.assertEqual(list(df['Pitch Predictability']), [
            0.,
            0.,
            0.,

            0.,
            1.,
            1.,

            1.,
            1.,
            0.,
            0.,
            0.,

            1.,
            1.,
            0.67,
            1.,
            1.,
            0.25,
            0,
        ])
