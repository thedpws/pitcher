
import pandas as pd
from pitchr.music import *


def tag_pitch(notes_df):

    pitch_df = notes_df[['Key', 'Letter', 'Octave', 'Accidental']]

    key = getattr(Key, pitch_df.iloc[0]['Key'] + '_MAJOR')


    print(key)
