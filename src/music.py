from abc import ABC
from collections.abc import Collection
import mingus.core.notes as mingus_notes
from mingus.containers import Note as MingusNote
import mingus.core.chords as MingusChord
from mingus.containers import NoteContainer as MingusNoteContainer
from mingus.containers import Composition as MingusComposition
from mingus.containers.instrument import Instrument as MingusInstrument, Piano as MingusPiano, Guitar as MingusGuitar
from enum import Enum
import re


class PitcherException(Exception):
    pass

global _time_signature, _key_signature
_time_signature = None
_key_signature = None

def key(key_signature):
    global _key_signature
    _key_signature = key_signature

def time(time_signature):
    global _time_signature
    _time_signature = time_signature

class Key:
    def __init__(self, flats=0, sharps=0):

        if flats and sharps:
            raise PitcherException(f'Key signature with {flats} flats and {sharps} sharps is invalid')

        self._flats = flats
        self._sharps = sharps


Key.Cb_MAJOR = Key(flats=7)
Key.Gb_MAJOR = Key.Eb_MINOR = Key(flats=6)
Key.Db_MAJOR = Key.Bb_MINOR = Key(flats=5)
Key.Ab_MAJOR = Key.F_MINOR = Key(flats=4)
Key.Eb_MAJOR = Key.C_MINOR = Key(flats=3)
Key.Bb_MAJOR = Key.G_MINOR = Key(flats=2)
Key.F_MAJOR = Key.D_MINOR = Key(flats=1)

Key.C_MAJOR = Key.A_MINOR = Key()

Key.G_MAJOR = Key.E_MINOR = Key(sharps=1)
Key.D_MAJOR = Key.B_MINOR = Key(sharps=2)
Key.A_MAJOR = Key.F_SHARP_MINOR = Key(sharps=3)
Key.E_MAJOR = Key.C_SHARP_MINOR = Key(sharps=4)
Key.B_MAJOR = Key.G_SHARP_MINOR = Key(sharps=5)
Key.F_SHARP_MAJOR = Key(sharps=6)
Key.C_SHARP_MAJOR = Key(sharps=7)


class Time:
    def __init__(self, time):
        if not re.match(r'\d/\d', time):
            raise PitcherException(f'{time} is an invalid time signature')
        self._time = time

Time.COMMON_TIME = Time('4/4')
Time.CUT_TIME = Time('2/4')



class Clef(Enum):
    TREBLE = 0
    BASS = 1

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
    def __init__(self, title=None, subtitle=None, author=None, author_email=None):
        self._title = title or ''


        self._composition = MingusComposition()
        self._composition.set_author(author, author_email)
        self._composition.set_title(title)

        self._parts = []

    def get_author(self):
        return self._composition.author

    def get_title(self):
        return self._composition.title

    # A little more explicit than "append" or "extend". This is for readability since these are not conventional terms.
    def add_part(self, part):
        self._parts.append(part)


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
            tempo=None,
            time_signature=None,
            key_signature=None,
    ):
        self._staffs = staffs or [Staff()]
        self._time_signature = time_signature
        self._key_signature = key_signature
        self.tempo = tempo

    def add_staff(self, staff):
        self._staffs.append(staff)

class Staff(_Music):

    '''Collection of measures'''
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

        enough_measures = len(self._measures) > i

        while not enough_measures:
            self._measures.append(Measure())
            enough_measures = len(self._measures) > i


        return self._measures[i]


# TODO: Bind measure length by global time signature
class Measure(_Music, Collection):
    '''Collection of notes'''

    def __init__(self, notes=None):
        self._notes = notes or dict()
        self._next_count = 0.0

    def __setitem__(self, start, item):
        self._notes[start] = item
        self._next_count = max(self._next_count, start + item.duration)

    def append(self, item):
        self._notes[self._next_count] = item

        self._next_count += item.duration

    def __getitem__(self, start):
        return self._notes[start]

    def __delitem__(self, start):
        del self._notes[start]

    def __iter__(self, start):
        return iter(self._notes)

    def __len__(self):
        '''Returns the total duration of the measure'''
        return self._next_count

    def __contains__(self, note):
        '''Returns True if note is in this measure'''
        all_notes = []
        for item in self._notes:
            if type(item) == Chord:
                all_notes.extend(item.notes)
            elif type(item) == Note:
                all_notes.append(item)

        return note in all_notes


    def extend(self, notes):
        for note in notes:
            self.append(note)


class Chord(_Music):
    def __init__(self, notes=None):
        self._notes = notes or []
        self._mingus_notes = MingusNoteContainer()

    # need to find a way to get the octave of the note so we can accurately make the chords
    # right now, we have the right pitch but not necessarily the right octave
    # only use these methods if notes is exactly 1 Note.
    @staticmethod
    def major_triad(note):
        mingus_triad = MingusChord.major_triad(note._pitch)
        my_triad = []
        for n in mingus_triad:
            temp = Note(n, note.duration, note.accidentals, note.dynamic, note.articulation)
            my_triad.append(temp)
        result = Chord(my_triad)
        return result
      
    @staticmethod
    def minor_triad(note):
        mingus_triad = MingusChord.minor_triad(note._pitch)
        my_triad = []
        for n in mingus_triad:
            temp = Note(n, note.duration, note.accidentals, note.dynamic, note.articulation)
            my_triad.append(temp)
        result = Chord(my_triad)
        return result

    @staticmethod
    def diminished_triad(note):
        mingus_triad = MingusChord.diminished_triad(note._pitch)
        my_triad = []
        for n in mingus_triad:
            temp = Note(n, note.duration, note.accidentals, note.dynamic, note.articulation)
            my_triad.append(temp)
        result = Chord(my_triad)
        return result

    @staticmethod
    def augmented_triad(note):
        mingus_triad = MingusChord.augmented_triad(note._pitch)
        my_triad = []
        for n in mingus_triad:
            temp = Note(n, note.duration, note.accidentals, note.dynamic, note.articulation)
            my_triad.append(temp)
        result = Chord(my_triad)
        return result

    @staticmethod
    def suspended_triad(note):
        mingus_triad = MingusChord.suspended_triad(note._pitch)
        my_triad = []
        for n in mingus_triad:
            temp = Note(n, note.duration, note.accidentals, note.dynamic, note.articulation)
            my_triad.append(temp)
        result = Chord(my_triad)
        return result
   
    @property
    def duration(self):
        return max(map(lambda n: n.duration, self._notes))

    def __iter__(self):
        return iter(self._notes)

    def append(self, note):
        self._notes += note
        self._mingus_notes += note.mingus()

    def remove(self, note):
        self._notes = [n for n in self._notes if n != note]
        self._mingus_notes.remove_note(note.mingus())

    def clear(self):
        self._mingus_notes.empty()
        self._notes.clear()

    def determine(self):
        return self._mingus_notes.determine()
      
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
    """
    @staticmethod
    def get_chord(note):
        return Chord.from_shorthand(note)

    # Returns all triads in a given key. Key is a string
    @staticmethod
    def get_triads(key):
        return Chord.triads(key)
    """

class Note(_Music):

    @classmethod
    def pitch_to_int(cls, pitch_string):
        if pitch_string == None: return None
        letter = re.findall('[A-G]', pitch_string)[0]
        accidentals = re.findall('[#Xb]+', pitch_string)
        accidentals = accidentals[0] if accidentals else ''
        octave = re.findall('\\d', pitch_string)[0]         #this line was throwing list index out of bounds
        octave = int(octave[0]) if octave else 4

        MIDDLE_C_OFFSET = 12*4

        pitch_number = (ord(letter) - ord('C')) + 12*octave - MIDDLE_C_OFFSET + 1*len(list(map(lambda c: c == '#', accidentals))) + 2*len(list(map(lambda c: c == 'X', accidentals))) - 1*len(list(map(lambda c: c == 'b', accidentals)))
        return pitch_number

    @classmethod
    def int_to_pitch(cls, pitch_number):
        if pitch_number == None: return None
        raise NotImplementedError('TODO')

    '''Has pitch and duration. Also accidentals and note-effects (tremolo)'''
    def __init__(self, pitch, duration, accidentals=None, dynamic=None, articulation=None):
        self._pitch = pitch
        self._pitch_number = Note.pitch_to_int(pitch)
        self._duration = duration
        self._accidentals = accidentals or ''  # sharp or flat
        self._dynamic = dynamic  # piano, forte, crescendo, etc
        self._articulation = articulation  # staccato, accent, fermata, etc
        if self._pitch_number != None:
            print(self._pitch_number)
            self._mingus_note = MingusNote(self._pitch_number)

    @property
    def pitch(self):
        pitch = self.int_to_pitch(self._pitch_number)
        return pitch + self._accidentals

    @property
    def pitch_number(self):
        self._pitch_number + 1*len(list(map(lambda c: c == '#', self._accidentals))) + 2*len(list(map(lambda c: c == 'X', self._accidentals))) - 1*len(list(map(lambda c: c == 'b', self._accidentals)))
        return pitch + self._accidentals

    @pitch.setter
    def pitch(self, pitch):
        self._pitch_number = Note.pitch_to_int(pitch)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def accidentals(self):
        return self._accidentals

    @accidentals.setter
    def accidentals(self, accidentals):
        self._accidentals = accidentals

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

    def __eq__(self, other):
        return self.duration == other.duration and self.pitch == other.pitch

    # Mingus interface

    def augment(self):
        """Raises the note by a half step"""
        self._mingus_note = mingus_notes.augment(str(self._mingus_note))
        
        if 'b' in self._accidentals:
            self._accidentals.remove('b')
        elif '#' in self._accidentals:
            self._accidentals.replace('#', 'X')
        else:
            self._accidentals += '#'
        return True

    def diminish(self):
        """Lowers the note by a half step"""
        self._mingus_note = mingus_notes.diminish(str(self._mingus_note))
        if 'X' in self._accidentals:
            self._accidentals.replace('X', '#')
        elif '#' in self._accidentals:
            self._accidentals.remove('#')
        else:
            self._accidentals += 'b'
        return True

    def transpose(self, half_steps):
        """Raises/Lowers the note"""
        if half_steps < 0:
            for _ in range(abs(half_steps)):
                self.diminish()
        elif half_steps > 0:
            for _ in range(abs(half_steps)):
                self.augment()

    def note(self):
        return self._mingus_note

    def octave_up(self):
        self._mingus_note.octave_up()
        self._pitch_number += 12
        return True

    def octave_down(self):
        self._mingus_note.octave_down()
        self._pitch_number -= 12
        return True


class Rest(Note):
    '''Has no pitch. Only duration.'''
    def __init__(self, duration):
        super(Rest, self).__init__(pitch=None, duration=duration)

    @property
    def pitch(self):
        return None

    @pitch.setter
    def pitch(self, pitch):
        raise PitcherException('Rests cannot be assigned a pitch')

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def accidentals(self):
        return None

    @accidentals.setter
    def accidentals(self, accidentals):
        raise PitcherException('Rests cannot be assigned a pitch')

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

    def augment(self):
        raise PitcherException('Rests cannot be assigned a pitch')

    def diminish(self):
        raise PitcherException('Rests cannot be assigned a pitch')

    def transpose(self, half_steps):
        raise PitcherException('Rests cannot be assigned a pitch')
    