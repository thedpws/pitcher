import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

from pitchr import df_import
from pitchr import pitch_tagger
from pitchr import xml_parser
from pitchr.music import *
import os
import requests
import shutil


try:
    PITCHR_PATH = os.environ["PITCHR_PATH"]
except KeyError:
    print('Environment variable "PITCHR_PATH" is unset. Using default path "~/.pitchr"')
    PITCHR_PATH = '~/.pitchr'


def prepare_np(melody_np):
    """Converts and normalizes numpy array for prediction in model

    :param melody_np: (50x2) numpy array of melody notes
    :returns melody_tf: tensorflow object of melody notes
    """
    difference = melody_np.shape[0] - 50
    # melody is too small
    if difference < 0:
        while difference != 0:
            melody_np = np.append(melody_np, [[-50, 0]], axis=0)
            difference += 1
    # melody is too large
    elif difference > 0:
        while difference != 0:
            melody_np = melody_np[:-1]
            difference -= 1
    melody_np = melody_np.reshape(1, 50, 2)
    melody_tf = tf.convert_to_tensor(melody_np, dtype=tf.float32)
    melody_tf = melody_tf / 50

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


def _get_durations(melody_staff):
    # Replace rest durations with its negative
    durations = []
    for measure in melody_staff:
        for note in measure:
            if type(note) == Rest:
                durations.append(-note.duration)
            else:
                durations.append(note.duration)
    return durations


def build_harmony(melody_staff):
    """Builds Harmony

    :param melody_staff: Pitchr melody staff
    :returns harmony_staff: Pitchr harmony staff
    """

    # Create list of durations. Negative indicates a rest. This will be used for decoding back to Pitchr
    durations = _get_durations(melody_staff)

    # Replace Rests with temp notes. Pitch is from previous note
    previous_note = None
    for note in [n for measure in melody_staff for n in measure]:
        if note.pitch:
            previous_note = note
            break
    else:
        raise PitcherException('Cannot generate harmony for an empty staff')

    for measure in melody_staff:
        for start_count, note in measure._notes.items():
            if note.pitch is None:
                rest = note
                measure[start_count] = Note(previous_note.pitch, rest.duration)

    melody_df = pd.DataFrame(
        columns=['Key', 'Clef', 'Letter', 'Octave', 'Accidental', 'Duration'],
        data=[['C', 'G', n.letter, str(n.octave), n.accidentals, n.duration] for measure in melody_staff for n in
              measure],
    )

    # Tag with more columns
    xml_parser.tag_df(melody_df)

    # Turn into NumPy arrays of the predictors
    melody_np = np.array(
        melody_df[['Pitch Number', 'Pitch Interval']]
    )

    zeros = np.zeros((50, 2))
    zeros[:len(melody_np)] = melody_np

    verify_model()
    model = keras.models.load_model(PITCHR_PATH + '/saved_model/my_model')
    input = prepare_np(zeros)
    output = model.predict(input, verbose=0)
    output = output * 50
    output = output.reshape(50, 2)

    harmony_measures = df_import.measures_from_ml_output(
        pitches=output.T[0],
        durations=durations,
        time_signature=str(melody_staff[0].time_signature)
    )

    harmony_staff = Staff(harmony_measures)
    return harmony_staff

def verify_model():
    MODEL_PATH = PITCHR_PATH + '/saved_model/my_model'

    if not os.path.exists(MODEL_PATH):
        print('Downloading required models...')
        os.makedirs(MODEL_PATH, exist_ok=True)
        os.makedirs(MODEL_PATH + '/variables/', exist_ok=True)

        try:
            variables_data = requests.get('https://github.com/thedpws/pitcher/blob/master/pitchr/saved_model/my_model/variables/variables.data-00000-of-00001?raw=true').content
            variables_index = requests.get('https://github.com/thedpws/pitcher/blob/master/pitchr/saved_model/my_model/variables/variables.index?raw=true').content
            saved_model = requests.get('https://github.com/thedpws/pitcher/blob/master/pitchr/saved_model/my_model/saved_model.pb?raw=true').content

            with open(MODEL_PATH + '/variables/variables.data-00000-of-00001', 'wb') as f:
                f.write(variables_data)

            with open(MODEL_PATH + '/variables/variables.index', 'wb') as f:
                f.write(variables_index)

            with open(MODEL_PATH + '/saved_model.pb', 'wb') as f:
                f.write(saved_model)

        except Exception as e:
            shutil.rmtree(MODEL_PATH)
            raise PitcherException('Could not download saved model. Harmony generation will be unavailable.' + str(e))



