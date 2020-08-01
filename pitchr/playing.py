from enum import Enum
from tempfile import TemporaryDirectory
from threading import get_ident

import numpy as np
from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick
from timidity import Parser, play_notes

from pitchr.utils import _suppress_stdout_stderr

class EventType(Enum):
    """Enumeration of Event types"""
    KEY_ON = 'note_on'
    KEY_OFF = 'note_off'


class Event:
    """Represents a MIDI keyon/keyoff event.

    :param event_type: a MIDI message type of "note_on" or "note_off"
    :param pitch_number: int representing the pitch of the key"
    :param velocity: int representing the velocity of keypress
    :param time: number of ticks after the previous event
    """
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
    """Plays a score.
    :param score: instance of Pitchr.Score
    :returns: True"""
    mid = MidiFile()

    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    events = []

    for part in score:
        bpm = part.tempo
        ticks = lambda beats: int(beats * bpm2tempo(bpm)) / 1000

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

                        # test for note tie, create space between notes if not tied.
                        duration = note.duration
                        if duration > 0:
                            if not note.tie:
                                duration = duration - 0.05

                        beat_keyon = measure_beat_offset + start
                        beat_keyoff = beat_keyon + duration

                        time_keyon = ticks(beat_keyon)
                        time_keyoff = ticks(beat_keyoff)

                        time_delay = ticks(part.time_signature.beat_definition) // (2 ** 5)

                        time_keyoff = time_keyoff - time_delay

                        events.extend([
                            Event(EventType.KEY_ON, midi_pitch, 127, time_keyon),
                            Event(EventType.KEY_OFF, midi_pitch, 127, time_keyoff),
                        ])

    curr_time = 0
    for e in sorted(events):
        delta_time = e.time - curr_time
        track.append(Message(e.event_type.value, channel=2, note=e.pitch_number, velocity=e.velocity,
                             time=int(round(delta_time))))
        curr_time += delta_time

    with TemporaryDirectory() as tmpdirname:
        midi_filepath = tmpdirname + '/' + str(get_ident()) + '.mid'
        mid.save(midi_filepath)
        with _suppress_stdout_stderr():
            ps = Parser(midi_filepath)
            play_notes(*ps.parse(), np.sin)

    return True
