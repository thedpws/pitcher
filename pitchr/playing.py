
from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick
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
    events = []

    mid = MidiFile()

    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    events = []

    for part in score:
        tempo = 700 - part.tempo
        #print("tempo:", str(tempo))
        for i_staff, staff in enumerate(part):


            for i_measure, measure in enumerate(staff):

                measure_beat_offset = part.time_signature.beats_per_measure * i_measure

                for start, item in measure._notes.items():

                    try:
                        iter(item)
                        notes = item.notes
                    except Exception:
                        notes = [item]


                    for note in notes:
                        if note.pitch_number == None:
                            continue
                        midi_pitch = note.pitch_number + 60

                        beat_keyon = measure_beat_offset + start
                        beat_keyoff = beat_keyon + note.duration

                        #midi_seconds = 60000 / (1120 * tempo)
                        #midi_ticks = 5000*tempo/60000
                        #print("midi_seconds:", str(midi_seconds))
                        #print("midi_ticks:", str(midi_ticks))

                        time_keyon = beat_keyon * tempo
                        time_keyoff = beat_keyoff * tempo

                        #print("beat_keyon:", str(beat_keyon))
                        #print("beat_keyoff:", str(beat_keyoff))
                        #print("time_keyon:", str(time_keyon))
                        #print("time_keyoff:", str(time_keyoff))
                        events.extend([
                           Event(EventType.KEY_ON, midi_pitch, 127, time_keyon),
                           Event(EventType.KEY_OFF, midi_pitch, 127, time_keyoff),
                        ])

    curr_time = 0
    for e in sorted(events):
        delta_time = e.time - curr_time
        track.append(Message(e.event_type.value, channel=2, note=e.pitch_number, velocity=e.velocity, time=int(round(delta_time))))
        curr_time += delta_time


    with TemporaryDirectory() as tmpdirname:
        midi_filepath = tmpdirname + '/' + str(get_ident()) + '.mid'
        mid.save(midi_filepath)
        ps = Parser(midi_filepath)
        play_notes(*ps.parse(), np.sin)

    return True


    


"""
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
    print('AZ DONE')
"""
