
from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick
from timidity import Parser, play_notes
from tempfile import TemporaryDirectory
from threading import get_ident
import numpy as np


def play_score(score):
    raise NotImplementedError('TODO: score_to_midi')
