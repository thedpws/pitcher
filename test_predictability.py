import unittest
from pitchr.music import *

import pandas as pd

from pitchr.predict import predict

class TestPredictability(unittest.TestCase):

    def test_predictability(self):


        melody = [
            Note('C', 1.0), # Predictability: 0.0 
            Note('D', 1.0), # 0.0
            Note('E', 1.0), # 0.0

            Note('C', 1.0), # 0.0
            Note('D', 1.0), # 1.0
            Note('E', 1.0), # 1.0

            Note('C', 1.0), # 1.0
            Note('D', 1.0), # 1.0
            Note('G', 1.0), # 0.0
            Note('F', 1.0), # 0.0
            Note('E', 1.0), # 0.0

            Note('C', 1.0), # 1.0
            Note('D', 1.0), # 1.0
            Note('E', 1.0), # 0.67
            Note('C', 1.0), # 1.0
            Note('D', 1.0), # 1.0
            Note('G', 1.0), # 0.33
            Note('C5', 1.0) # 0.0
        ]

        df = pd.DataFrame([
            {
                'Key': 'C',
                'Clef': 'G',
                'Letter': n.letter,
                'Octave': n.octave,
                'Accidental': n.accidentals,
                'Duration': n.duration
            } for n in melody
        ])

        # Act
        prediction = predict(df)

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
            2/3,
            1.,
            1.,
            1/3,
            0,
        ])
