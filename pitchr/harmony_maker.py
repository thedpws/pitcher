# tensorflow requires 64-bit python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Flatten
import numpy as np
from sklearn.model_selection import train_test_split

# steps to NN model: 1) build model, 2) compile model, 3) train model, 4) evaluate model, 5) make predictions

# loads the data: data_path is path to file which has 2 lines:
# 1st line is a list of 32 arrays of melody info
# 2nd line is a list of 32 arrays of harmony info
def load_data(data_path):
    with open(data_path) as data:
        melody = data.readline()
        harmony = data.readline()
        melody.reshape(32, 4)
        harmony.reshape(32, 4)

    return melody, harmony



# build model
def make_model(melody):
# Uses Recurrent Neural Networks (RNN). Suitable bc it takes into account order. use LSTM cell
# This model processes 64 notes at a time, and will break up the score into chunks of 64 notes. If not enough, adds
# rest notes to the end
# 32 x 4 (number of notes x number of features)
    model = Sequential()    # data moves from left to right
    model.add(LSTM(128, input_shape=(melody_train.shape[1:]), activation='relu', return_sequences=True))
    model.add(Dense(32, input_shape=(32,4)))  # produces 32 outputs
    model.add(Dense(64))
    model.add(Dense(64))
    model.add(LSTM(128, activation='relu'))
    

if __name__ == "__main__":
    # load data
    melody, harmony = load_data("data_path")

    # split data
    melody_train, melody_test, harmony_train, harmony_test = train_test_split(melody, harmony, test_size=0.2)

    # build model
    model = Sequential()
    model.add(Flatten(input_shape=(32, 4)))   # input layer
    model.add(Dense(512, activation="relu"))    # 1st hidden layer. relu increases efficiency and is good for the model overall
    model.add(Dense(256, activation="relu"))    # 2nd hidden layer
    model.add(Dense(128, activation="relu"))    # 3rd hidden layer
    model.add(Dense(64, activation="relu"))    # 4th hidden layer
    model.add(Dense(32, activation="softmax"))    # output layer

    # compile model
    optimizer = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    model.summary() # summarizes model. Good for debugging

    # train model
    model.fit(melody_train, harmony_train, validation_data=(melody_test, harmony_test),
              epochs=50,
              batch_size=32) # 32 is the default. Might play around with some of the parameters