from abc import ABC
from collections.abc import Collection
import mingus.core.notes as notes
import mingus.core.chords as Chord
import mingus.core.scales as scales
from mingus.containers import Note
from mingus.containers import NoteContainer
from mingus.containers import Composition
from mingus.containers.instrument import Instrument, Piano, Guitar
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
    #def __init__(self):
    #    self._piano = Piano()
    #    self._guitar = Guitar()
    #    self._instrument = Instrument()
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
    def __init__(self, title=None, subtitle=None, key_signature=None, time_signature=None, author=None, author_email=None):
        self._composition = Composition()
        self._composition.set_author(author, author_email)
        self._composition.set_title(title)
        #raise NotImplementedError

    def get_author(self):
        return self._composition.author

    def get_title(self):
        return self._composition.title


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
        #self._notes = notes if notes else dict()
        self._notes = NoteContainer(notes)


        #global _time_signature
        #if not _time_signature: raise Exception('Time signature undefined')
        #self._time_signature = _time_signature

        #global _key_signature
        #if not _key_signature: raise Exception('Key signature undefined')
        #self._key_signature = _key_signature

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

    def add_note(self, note):
        self._notes += note

    def delete_note(self, note):
        self._notes.remove_note(note)

    def clear_measure(self):
        self._notes.empty()

    def determine(self):
        return self._notes.determine()
    
    def get_measure(self):
        return self._notes

class CChord(_Music):
    # note=pitch. Automatically creates the most likely chords the user might use for the note
    def __init__(self, note, key):
        self._natural_triad = Chord.triad(note, key)
        self._major_triad = Chord.major_triad(note)
        self._minor_triad = Chord.minor_triad(note)
        self._diminished_triad = Chord.diminished_triad(note)
        self._augmented_triad = Chord.augmented_triad(note)
        self._suspended_triad = Chord.suspended_triad(note)

    def __iter__(self):
        return iter(self._notes)

    # note is a string. This function returns the corresponding chord of notes
    # get_chord("C") returns ['C', 'E', 'G'] and get_chord("Cm") returns ['C', 'Eb', 'G']
    """ These are recognized abbreviations:
        Triads: ‘m’, ‘M’ or ‘’, ‘dim’.
        Sevenths: ‘m7’, ‘M7’, ‘7’, ‘m7b5’, ‘dim7’, ‘m/M7’ or ‘mM7’
        Augmented chords: ‘aug’ or ‘+’, ‘7#5’ or ‘M7+5’, ‘M7+’, ‘m7+’, ‘7+’
        Suspended chords: ‘sus4’, ‘sus2’, ‘sus47’, ‘sus’, ‘11’, ‘sus4b9’ or ‘susb9’
        Sixths: ‘6’, ‘m6’, ‘M6’, ‘6/7’ or ‘67’, 6/9 or 69
        Ninths: ‘9’, ‘M9’, ‘m9’, ‘7b9’, ‘7#9’
        Elevenths: ‘11’, ‘7#11’, ‘m11’
        Thirteenths: ‘13’, ‘M13’, ‘m13’
        Altered chords: ‘7b5’, ‘7b9’, ‘7#9’, ‘67’ or ‘6/7’
        Special: ‘5’, ‘NC’, ‘hendrix’
    """
    @staticmethod
    def get_chord(note):
        return Chord.from_shorthand(note)

    # Returns all triads in a given key. Key is a string
    @staticmethod
    def get_triads(key):
        return Chord.triads(key)




# TODO: Add effects
class NNote(_Music):
    '''Has pitch and duration. Also accidentals and note-effects (tremolo)'''
    def __init__(self, pitch, duration, accidental, dynamic, articulation):
        self._pitch = pitch
        self._duration = duration
        self._accidental = accidental  # sharp or flat
        self._dynamic = dynamic  # piano, forte, crescendo, etc
        self._articulation = articulation  # staccato, accent, fermata, etc
        self._note = Note(pitch, duration)

    @property
    def pitch(self):
        return self._pitch

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def accidental(self):
        return self._accidental

    @accidental.setter
    def accidental(self, accidental):
        self._accidental = accidental

    @property
    def dynamic(self):
        return self._dynamic

    @dynamic.setter
    def dynamic(self, dynamic):
        self._dynamic = dynamic

    @property
    def articulation(self):
        return self._articulation

    @articulation.setter
    def articulation(self, articulation):
        self._articulation = articulation

    """You can change everything about the note except the pitch itself"""

    def __eq__(self, other):
        return self.duration == other.duration and self.pitch == other.pitch

    # Mingus interface

    @staticmethod
    def is_valid_note(note):
        return notes.is_valid_note(note)

    def int_to_note(self, this_int):
        # C -> 0
        # C# -> 1
        # D -> 2
        # D# -> 3
        # E -> 4
        return notes.int_to_note(this_int)

    def augment_note(self):
        self._note = notes.augment(str(self._note))
        return True

    def diminish_note(self):
        self._note = notes.diminish(str(self._note))
        return True

    """ mingus documentation shows these are functions but are nowhere to be found in the actual code
    def to_minor(self):
        self._note = notes.to_minor(self._note)
        #self._note.to_minor()
        return True
    
    def to_major(self):
        #self._note = notes.to_major(self._note)
        self._note = notes.to_major(str(self._note))
        #self._note.to_major()
        return True
    """

    # Doesn't work right now for unknown reasons. Note can be transposed if created outside of the class but
    # self._note can't be transposed
    def transpose(self, transpose_t, up=True):
        self._note.transpose(transpose_t)

    def octave_up(self):
        self._note.octave_up()
        return True

    def octave_down(self):
        self._note.octave_down()
        return True

    # get hertz value of the note. May be useful for machine learning (associate frequencies with notes)
    def get_hertz(self):
        return self._note.to_hertz()

    """
    # gets major diatonic scale of self._note
    def get_diatonic(self):
        #scales.diatonic(self._note)
        scales.Major.ascending(str(self._note))
        return True

    # gets natural minor scale of self._note
    def get_natural_minor(self):
        scales.natural_minor(self._note)
        return True

    # gets harmonic minor scale of self._note
    def get_harmonic_minor(self):
        scales.harmonic_minor(self._note)
        return True

    # gets melodic minor scale of self._note
    def get_melodic_minor(self):
        scales.melodic_minor(self._note)
        return True

    # gets chromatic scale of scale._note
    def get_chromatic(self):
        scales.chromatic(self._note)
        return True
    """

class Rest(Note):
    '''Has no pitch. Only duration.'''
    def __init__(self, duration):
        super(Rest, self).__init__(pitch=None, duration=duration)
