from collections.abc import Collection
from enum import Enum

global _time_signature, _key_signature
_time_signature = None
_key_signature = None

def key(key_signature):
    global _key_signature
    _key_signature = key_signature

def time(time_signature):
    global _time_signature
    _time_signature = time_signature

class Key(Enum):
    C_MAJOR = A_MINOR = 0
    Db_MAJOR = 1

class Time(Enum):
    COMMON_TIME = 0

class Clef(Enum):
    TREBLE = 0

class Voice(Enum):
    PIANO = 0

class _Music:

    def listen(self, **kwargs):
        '''Plays music'''
        raise NotImplementedError

    def show(self, **kwargs):
        '''Shows a graphic of music'''
        raise NotImplementedError

    def save(self, filename, **kwargs):
        '''Saves music to a PDF'''
        raise NotImplementedError

class Score(_Music):
    '''Contains textual information and optional arguments for the first Part'''
    def __init__(self, title=None, subtitle=None, key_signature=None, time_signature=None):
        raise NotImplementedError


class Part(_Music):
    '''A collection of staffs. Add effects / stanza-chorus / key/time changes to parts. Should affect its children.'''

    @property
    def key_signature(self):
        return self._key_signature

    @key_signature.setter
    def key_signature(self, key_signature):
        self._key_signature = key_signature


    @property
    def time_signature(self):
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature):
        self._time_signature = time_signature


    def __init__(
            self,
            staffs=None,
            time_signature=Time.COMMON_TIME,
            key_signature=Key.C_MAJOR,
    ):
        self._staffs = staffs if staffs else [UnvoicedStaff()]
        self._time_signature = time_signature
        self._key_signature = key_signature

class _Staff(_Music):

    '''Collection of measuresinstrument/voice'''
    '''Measures must have correct rhythm to be successfully added to a staff in a part'''
    def __init__(self, clef=Clef.TREBLE, voice=Voice.PIANO, measures=None):
        self._clef = clef
        self._voice = voice
        self._measures = measures if measures else [Measure()]

    @property
    def clef(self):
        return self._clef

    @clef.setter
    def clef(self, clef):
        self._clef = clef

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, voice):
        self._voice = voice

    def __getitem__(self, i):
        return self._measures[i]


class VoicedStaff(_Staff):
    '''A staff with distinct voicing (SATB)'''
    '''Notes must be attached to a specific voice'''

    def __init__(self, clef=Clef.TREBLE, voice=Voice.PIANO, measures=None):
        self._voices = dict()
        super(VoicedStaff, self).__init__(clef, voice, measures)

    def __getitem__(self, voice):
        return self._voices[voice]


class UnvoicedStaff(_Staff):
    '''A staff without distinct voicing (Piano pieces)'''
    '''Notes are not attached to voices'''
    pass

# TODO: Bind measure length by global time signature
class Measure(_Music, Collection):
    '''Collection of notes'''

    def __init__(self, notes=None):
        self._notes = notes if notes else dict()

        global _time_signature
        if not _time_signature: raise Exception('Time signature undefined')
        self._time_signature = _time_signature

        global _key_signature
        if not _key_signature: raise Exception('Key signature undefined')
        self._key_signature = _key_signature

    @property
    def key_signature(self):
        return self._key_signature

    @key_signature.setter
    def key_signature(self, key_signature):
        self._key_signature = key_signature

    @property
    def time_signature(self):
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature):
        self._time_signature = time_signature

    def __setitem__(self, start, item):
        '''To add a quarter note at beat 2: m[2] = Note('C#', 1)'''
        self._notes[start] = item
        self._verify_duration()

    def _verify_duration(self):
        raise NotImplementedError('TODO. Verify recently-added note does not invalidate measure length wrt Time signature')



    def __getitem__(self, start):
        return self._notes[start]

    def __delitem__(self, start):
        del self.notes[start]

    def __iter__(self, start):
        raise NotImplementedError('TODO')
        return iter(self._notes)

    def __len__(self):
        '''Returns the total duration of the measure'''
        raise NotImplementedError('TODO')

    def __contains__(self, note):
        '''Returns True if note is in this measure'''
        return note in [note for chord in measure for note in chord]

    def append(self, note):
        raise NotImplementedError('TODO')

    def extend(self, notes):
        raise NotImplementedError('TODO.')

class Chord(_Music):
    def __init__(self, notes=None):
        self._notes = notes if notes else []
    def __iter__(self):
        return iter(self._notes)



# TODO: Add effects
class Note(_Music):
    '''Has pitch and duration. Also accidentals and note-effects (tremolo)'''
    def __init__(self, pitch, duration):
        self._pitch = pitch
        self._duration = duration

    @property
    def pitch(self):
        return self._pitch

    @property
    def duration(self):
        return self._duration

    def __eq__(self, other):
        return self.duration == other.duration and self.pitch == other.pitch

class Rest(Note):
    '''Has no pitch. Only duration.'''
    def __init__(self, duration):
        super(Rest, self).__init__(pitch=None, duration=duration)
