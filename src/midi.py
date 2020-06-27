
from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick
from music import Note, Chord
from timidity import Parser, play_notes
from tempfile import TemporaryDirectory
from threading import get_ident
import numpy as np


from enum import Enum
class EventType(Enum):
    KEY_ON = 'note_on'
    KEY_OFF = 'note_off'


class Event:
    def __init__(self, event_type, pitch_number, velocity, time):
        self._type = event_type
        self._pitch_number = pitch_number
        self._velocity = velocity
        self._time = time

    @property
    def event_type(self):
        return self._type

    @property
    def pitch_number(self):
        return self._pitch_number

    @property
    def velocity(self):
        return self._velocity

    @property
    def time(self):
        return self._time

    def __lt__(self, other):
        return self._time < other._time



def play_score(score):
    raise NotImplemented('TODO: score_to_midi')

def measure_to_midi(measure):

    tempo = 600


    mid = MidiFile()

    track = MidiTrack()

    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))


    note_pitches = ['C4', 'D4', 'E4', 'F4', 'G4', 'A5', 'B5']
    note_pitch_nums = [60, 62, 64, 65, 67, 70, 72]


    pitch_dict = dict(zip(note_pitches, note_pitch_nums))


    events = []

    for start, item in sorted(measure._notes.items()):

        if isinstance(item, Note):
            notes = [item]
        elif isinstance(item, Chord):
            notes = item.notes

        for note in notes:

            pitch_number = pitch_dict[note.pitch]

            on_beat, off_beat = (start), (start + note.duration)

            on_time, off_time = (on_beat * tempo), (off_beat * tempo)
            
            events.extend([
               Event(EventType.KEY_ON, pitch_number, 127, on_time),
               Event(EventType.KEY_OFF, pitch_number, 127, off_time),
            ])

    curr_time = 0
    for e in sorted(events):
        delta_time = e.time - curr_time
        track.append(Message(e.event_type.value, channel=2, note=e.pitch_number, velocity=e.velocity, time=int(round(delta_time))))
        curr_time += delta_time


    return mid




def play(midi_file):
    with TemporaryDirectory() as tmpdirname:
        midi_filepath = tmpdirname + '/' + str(get_ident()) + '.mid'
        midi_file.save(midi_filepath)
        ps = Parser(midi_filepath)
        play_notes(*ps.parse(), np.sin)
    print('AZ DONE')
