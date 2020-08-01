# tensorflow requires 64-bit python
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.models import Sequential

from pitchr import xml_parser


def load_data():
    """Loads data for training model

    :returns all_melody_np: 3D numpy array of melody notes
    :returns all_harmony_np: 3D numpy array of harmony notes
    """
    # Load data
    all_melody_dfs, all_harmony_dfs, all_melody_durations = xml_parser.get_all_data()

    # Converting all dataframes to numpy arrays
    all_melody_np = []
    all_harmony_np = []
    for df in all_melody_dfs:
        df = df[['Pitch Number', 'Pitch Interval']]
        temp_np = df.to_numpy()
        all_melody_np.append(temp_np)
    for df in all_harmony_dfs:
        df = df[['Pitch Number', 'Pitch Interval']]
        temp_np = df.to_numpy()
        all_harmony_np.append(temp_np)

    # normalize harmony sizes
    all_harmony_np = xml_parser.prepare_harmony(all_harmony_np)

    # convert dataframes to numpy arrays
    all_melody_np = np.asarray(all_melody_np)
    all_harmony_np = np.asarray(all_harmony_np)

    # convert rest notes to -50
    for array in all_melody_np:
        for note in array:
            if type(note[0]) == str:
                note[0] = float(-50)

    for array in all_harmony_np:
        for note in array:
            if type(note[0]) == str:
                note[0] = float(-50)

    return all_melody_np, all_harmony_np


def build_model():
    """Builds RNN-LSTM model

    :returns model: RNN-LSTM model
    """
    model = Sequential()

    # 1 LSTM layer
    model.add(LSTM(200, input_shape=(50, 2), return_sequences=True))
    model.add(Dropout(0.2))

    # Dense layers
    model.add(Dense(150, activation="tanh"))
    model.add(Dense(50))

    # Output Layer
    model.add(Dense(2))

    return model


def plot_model(trained_model):
    """Plots model training data

    :param trained_model: Trained model
    """
    plt.plot(trained_model.history['accuracy'])
    plt.plot(trained_model.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()
