
from enum import Enum

class Key(Enum):
    C_MAJOR = 0


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
        raise NotImplementedError

    @key_signature.setter
    def key_signature(self, key_signature):
        raise NotImplementedError


    @property
    def time_signature(self):
        raise NotImplementedError

    @time_signature.setter
    def time_signature(self, time_signature):
        raise NotImplementedError


    def __init__(
            self,
            staffs=None,
            time_signature=Time.COMMON_TIME,
            key_signature=Key.C_MAJOR,
    ):
        raise NotImplementedError

class _Staff(_Music):

    '''Collection of measuresinstrument/voice'''
    '''Measures must have correct rhythm to be successfully added to a staff in a part'''
    def __init__(self, clef=Clef.TREBLE, voice=Voice.PIANO, measures=None):
        if not measures:
            measures = [Measure()]
        self._measures = []

class VoicedStaff(_Staff):
    '''A staff with distinct voicing (SATB)'''
    '''Notes must be attached to a specific voice'''

    def __init__(self, clef=Clef.TREBLE, voice=Voice.PIANO):
        self._voices = dict()

    def __getitem__(self, voice):
        return self._voices[voice]

class UnvoicedStaff(_Staff):
    '''A staff without distinct voicing (Piano pieces)'''
    '''Notes are not attached to voices'''
    def __init__(self, clef=Clef.TREBLE, voice=Voice.PIANO):
        raise NotImplementedError

# TODO: Bind measure length by global time signature
class Measure(_Music):
    '''Collection of notes'''

    def __init__(self, notes=None):
        if not notes:
            notes = []
        self._notes = notes

# TODO: Add effects
class Note(_Music):
    '''Has pitch and duration. Also accidentals and note-effects (tremolo)'''
    def __init__(self, pitch, duration):
        self._pitch = pitch
        self._duration = duration

class Rest(Note):
    '''Has no pitch. Only duration.'''
    def __init__(self, duration):
        super(Rest, self).__init__(pitch=None, duration=duration)
