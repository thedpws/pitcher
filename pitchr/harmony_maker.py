# tensorflow requires 64-bit python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np
from pitchr import xml_parser
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def load_data():
    """Loads data and splits it into train, validation, and test sets.

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
            for i in range(0, 2):
                if type(note[i]) == str:
                    note[i] = float(-50)
                    np.float32

    for array in all_harmony_np:
        for note in array:
            for i in range(0, 2):
                if type(note[i]) == str:
                    note[i] = float(-50)

    return all_melody_np, all_harmony_np


def build_model():
    """Builds RNN-LSTM model

        :returns model: RNN-LSTM model
    """
    model = Sequential()

    # 2 LSTM layers
    model.add(LSTM(300, input_shape=(50, 2), return_sequences=True))
    model.add(Dropout(0.2))

    # Dense layers
    model.add(Dense(300, activation="tanh"))
    model.add(Dense(200, activation="tanh"))
    model.add(Dense(100, activation="tanh"))

    # Output Layer
    model.add(Dense(2))

    return model


if __name__ == "__main__":
    # load data
    all_melody_np, all_harmony_np = load_data()

    # prepare data
    x_train, x_test, y_train, y_test = train_test_split(all_melody_np, all_harmony_np, test_size=0.2)
    x_train = tf.convert_to_tensor(x_train, dtype=tf.float32)
    y_train = tf.convert_to_tensor(y_train, dtype=tf.float32)
    x_test = tf.convert_to_tensor(x_test, dtype=tf.float32)
    y_test = tf.convert_to_tensor(y_test, dtype=tf.float32)
    normalized_x_train = x_train / 50
    normalized_y_train = y_train / 50
    normalized_x_test = x_test / 50
    normalized_y_test = y_test / 50

    # build model
    model = build_model()

    # compile model
    optimizer = keras.optimizers.Adam(learning_rate=0.01)
    model.compile(optimizer=optimizer, metrics=['accuracy'], loss='mse')

    model.summary()

    # train model
    trained_model = model.fit(normalized_x_train, normalized_y_train, epochs=500,
                              validation_data=(normalized_x_test, normalized_y_test), batch_size=12)

    trained_model.summary()

    plt.plot(trained_model.history['acc'])
    plt.plot(trained_model.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()