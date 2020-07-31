from tensorflow import keras
from pitchr import df_import
from pitchr import pitch_tagger
import tensorflow as tf
from tensorflow import keras
import numpy as np
from pitchr.music import *
import pandas as pd

def prepare_np(melody_np):
    """Converts and normalizes numpy array for prediction in model

        :param melody_np: (50x2) numpy array of melody notes
        :returns melody_tf: tensorflow object of melody notes
    """
    melody_np = melody_np.reshape(1, 50, 2)
    melody_tf = tf.convert_to_tensor(melody_np, dtype=tf.float32)
    melody_tf = melody_tf/50

    return melody_tf


def prepare_staff(staff):
    """Takes a staff and converts it into a numpy array of notes

        :param staff: Pitchr staff
        :returns notes_np: 50x2 numpy array (pads it with rests)
    """
    notes_np = []
    for measure in staff:
        for note in measure:
            if note.pitch_number == None:
                notes_np.append([-50])
            else:
                notes_np.append([note.pitch_number])
            print(type(note.pitch_number))

    notes_df = pd.DataFrame(notes_np, columns=['Pitch Number'])
    pitch_tagger.tag_pitch_interval(notes_df)
    print(notes_df.columns)
    print(notes_df)
    notes_np = np.asarray(notes_np)

    difference = notes_np.shape[0] - 50
    # harmony is too small
    if difference < 0:
        while difference != 0:
            notes_np = np.append(notes_np, [[-50, 0]], axis=0)
            difference += 1
    elif difference > 0:
        while difference != 0:
            notes_np = notes_np[:-1]
            difference -= 1

    notes_np.reshape(50, 2)
    return notes_np


def build_harmony(melody_staff):
    """Builds Harmony

        :param melody_staff: Pitchr staff
        :returns harmony_staff: staff of harmony notes
    """
    model = keras.models.load_model('saved_model/my_model')
    input = prepare_np(melody_np)
    output = model.predict(input, verbose=0)
    output = output*50
    output = output.reshape(50, 2)
    df_import.measures_from_dataframe()



measure1 = Measure()
measure1.append(Note("G7", 1))
measure1.append(Note("G#7", 1))
measure1.append(Note("C#7", 1))
measure1.append(Note("C4", 1))
measure2 = Measure()
measure2.append(Note("C5", .5))
measure2.append(Note("C6", .5))
measure2.append(Note("C7", .5))
measure2.append(Note("C8", .5))
measure2.append(Rest(1))
measure3 = Measure()
measure3.append(Note("B#8", .75))
measure3.append(Note("B#6", .5))
measure3.append(Note("B6", .5))
measure3.append(Note("B7", .5))
measure3.append(Note("B4", .5))
staff = Staff(measures=[measure1, measure2, measure3])
print("TESTING")
prepare_staff(staff)

#staff.play()