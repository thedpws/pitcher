from tensorflow import keras
from pitchr import df_import
import tensorflow as tf
from tensorflow import keras


def prepare_np(melody_np):
    """Converts and normalizes numpy array for prediction in model

        :param melody_np: (50x2) numpy array of melody notes
        :returns melody_tf: tensorflow object of melody notes
    """
    melody_np = melody_np.reshape(1, 50, 2)
    melody_tf = tf.convert_to_tensor(melody_np, dtype=tf.float32)
    melody_tf = melody_tf/50

    return melody_tf


def build_harmony(measures):
    """Builds Harmony

        :param measures: list of melody measures
        :returns harmony_np: (50, 2) numpy array of harmony notes
    """
    model = keras.models.load_model('saved_model/my_model')
    input = prepare_np(melody_np)
    output = model.predict(input, verbose=0)
    output = output*50
    output = output.reshape(50, 2)
    df_import.measures_from_dataframe()


