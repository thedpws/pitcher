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
import playing
import lyexport as showing


class PitcherException(Exception):
    pass

global _time_signature, _key_signature
_time_signature = '4/4'
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
    def __str__(self):
        return 'c \\major'


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

    def __str__(self):
        return self._time

    @property
    def beats_per_measure(self):
        return int(self._time.partition('/')[0])

    @property
    def beat_definition(self):
        return int(self._time.partition('/')[2])

Time.COMMON_TIME = Time('4/4')
Time.CUT_TIME = Time('2/4')



class Clef(Enum):
    TREBLE = 0
    BASS = 1

class Voice(Enum):
    PIANO = 0

class _Music:

    def play(self, **kwargs):
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
    def __init__(self, parts=None, title=None, subtitle=None, author=None, author_email=None):
        self._composition = MingusComposition()
        self._composition.set_author(author, author_email)
        self._composition.set_title(title)

        self._parts = parts or []

    @property
    def composer(self):
        return self._composition.author

    @property
    def author(self):
        return self._composition.author

    @property
    def title(self):
        return self._composition.title

    # A little more explicit than "append" or "extend". This is for readability since these are not conventional terms.
    def add_part(self, part):
        self._parts.append(part)

    def play(self):
        playing.play_score(self)

    def show(self):
        showing.show_score_png(self)

    def __iter__(self):
        return iter(self._parts)


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
            tempo=40,
            time_signature=None,
            key_signature=None,
    ):
        self._staffs = staffs or [Staff()]
        if not time_signature:
            global _time_signature
            time_signature = _time_signature

        if not key_signature:
            global _key_signature
            key_signature = _key_signature

        self._time_signature = time_signature
        self._key_signature = key_signature
        self.tempo = tempo

    def add_staff(self, staff):
        self._staffs.append(staff)

    def play(self):
        return Score(parts=[self]).play()

    def show(self):
        return Score(parts=[self]).show()

    def __iter__(self):
        return iter(self._staffs)

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

    def play(self):
        return Part(staffs=[self]).play()

    def show(self):
        return Part(staffs=[self]).show()

    def __iter__(self):
        return iter(self._measures)


# TODO: Bind measure length by global time signature
class Measure(_Music, Collection):
    '''Collection of notes'''

    def __init__(self, notes=None):
        self._notes = dict()
        self._next_count = 0.0

        if notes:
            self.extend(notes)

    def __setitem__(self, start, item):
        self._notes[start] = item
        self._next_count = max(self._next_count, start + item.duration)

    def append(self, item):
        # TODO: FIX
        if False and self._next_count + item.duration > _time_signature:
            print("Item exceeds measure's time signature")
        else:
            self._notes[self._next_count] = item
            self._next_count += item.duration

    def extend(self, items):
        for item in items:
            self.append(item)

    def __getitem__(self, start):
        return self._notes[start]

    def __delitem__(self, start):
        del self._notes[start]

    def __iter__(self):
        return iter(self._notes.values())

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

    def play(self):
        return Staff(measures=[self]).play()

    def show(self):
        return Staff(measures=[self]).show()



class Chord(_Music):
    def __init__(self, notes=None):
        self._notes = notes or []
        self._mingus_notes = MingusNoteContainer()

    def __str__(self):
        return f'{[str(n) for n in self.notes]}'

    @staticmethod
    def mingusChord_to_chord(mingus_chord, note):
        my_triad = []
        for n in mingus_chord:
            temp = Note.mingusNote_to_note(n, note)
            my_triad.append(temp)
        return Chord(my_triad)

    @staticmethod
    def major_triad(note):
        mingus_chord = MingusChord.major_triad(note.pitch)
        return Chord.mingusChord_to_chord(mingus_chord, note)
      
    @staticmethod
    def minor_triad(note):
        mingus_chord = MingusChord.minor_triad(note.pitch)
        return Chord.mingusChord_to_chord(mingus_chord, note)

    @staticmethod
    def diminished_triad(note):
        mingus_chord = MingusChord.diminished_triad(note.pitch)
        return Chord.mingusChord_to_chord(mingus_chord, note)

    @staticmethod
    def augmented_triad(note):
        mingus_chord = MingusChord.augmented_triad(note.pitch)
        return Chord.mingusChord_to_chord(mingus_chord, note)

    @staticmethod
    def suspended_triad(note):
        mingus_chord = MingusChord.suspended_triad(note.pitch)
        return Chord.mingusChord_to_chord(mingus_chord, note)
   
    @property
    def duration(self):
        return max(map(lambda n: n.duration, self._notes))

    def __iter__(self):
        return iter(self._notes)

    @property
    def notes(self):
        return self._notes

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

    def play(self):
        return Measure(notes=[self]).play()

    def show(self):
        return Measure(notes=[self]).show()

class Note(_Music):

    def __str__(self):
        return f'{self.letter} {self.duration}'

    #converts mingus_note to note
    @staticmethod
    def mingusNote_to_note(mingus_note, note):
        result = Note(mingus_note + note.accidentals + str(note.octave), note.duration, note.dynamic, note.articulation)
        return result

    '''Has pitch and duration. Also accidentals and note-effects (tremolo)'''
    # pitch has 3 characters max: note,#/b,octave
    def __init__(self, pitch, duration, dynamic=None, articulation=None):

        self._pitch = _Pitch.from_string(pitch)
        self._duration = duration
        self._dynamic = dynamic  # piano, forte, crescendo, etc
        self._articulation = articulation  # staccato, accent, fermata, etc

        if self.pitch_number != None:
            self._mingus_note = MingusNote(self.pitch_number)

    @property
    def letter(self):
        return self._pitch.letter

    @property
    def accidentals(self):
        return self._pitch.accidentals

    @property
    def pitch(self):
        """Returns a string of letter-note, accidentals, and octave"""
        return str(self._pitch)

    @pitch.setter
    def pitch(self, pitch):
        self._pitch = _Pitch.from_string(pitch)

    @property
    def octave(self):
        return self._pitch.octave

    @octave.setter
    def octave(self, octave):
        self._pitch.octave = octave

    @property
    def pitch_number(self):
        return int(self._pitch)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def accidentals(self):
        return self._pitch.accidentals

    @accidentals.setter
    def accidentals(self, accidentals):
        self._pitch.accidentals = accidentals

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
        self._pitch.accidentals += 1
        return True

    def diminish(self):
        """Lowers the note by a half step"""
        self._mingus_note = mingus_notes.diminish(str(self.mingus()))
        self._pitch.accidentals -= 1
        return True

    # half_steps is a 2 character string of +/- and a number of half-steps
    def transpose(self, half_steps):
        """Raises/Lowers the note"""
        num_half_steps = int(half_steps[1:])
        if half_steps[0] == '+':
            for num in range(num_half_steps):
                self._pitch.accidentals += '#'
        elif half_steps[0] == '-':
            for num in range(num_half_steps):
                self._pitch.accidentals += 'b'

    def note(self):
        return self._mingus_note

    def octave_up(self):
        """Raises the pitch an octave"""
        self._mingus_note.octave_up()
        self._pitch.octave += 1
        return True

    def octave_down(self):
        """Lowers the pitch an octave"""
        self._mingus_note.octave_down()
        self._pitch.octave -= 1
        return True
    
    def play(self):
        return Measure(notes=[self]).play()

    def show(self):
        return Measure(notes=[self]).show()


class Rest(Note):
    '''Has no pitch. Only duration.'''
    def __init__(self, duration):
        super(Rest, self).__init__(pitch=None, duration=duration)

    def __str__(self):
        return f'Rest {self.duration}'

    def _throw_exception(self):
        raise PitcherException('Rests cannot be assigned a pitch')

    @property
    def letter(self):
        self._throw_exception()

    @property
    def pitch(self):
        return None

    @pitch.setter
    def pitch(self, pitch):
        self._throw_exception()

    @property
    def pitch_number(self):
        return None

    @property
    def octave(self):
        return None

    @octave.setter
    def octave(self, octave):
        self._throw_exception()

    @property
    def accidentals(self):
        return None

    @accidentals.setter
    def accidentals(self, accidentals):
        self._throw_exception()

    def augment(self):
        self._throw_exception()

    def diminish(self):
        self._throw_exception()

    def transpose(self, half_steps):
        self._throw_exception()

    def octave_up(self, _):
        self._throw_exception()

    def octave_down(self, _):
        self._throw_exception()

        
class _Pitch:
    def __init__(self, letter, accidentals=None, octave=4):
        self._letter = letter
        self._accidental_offset = sum([offset*(sum(map(lambda c: c == accidental, accidentals))) for accidental, offset in {'b':-1, '#':+1, 'X':+2}.items()])
        self._octave = octave

    @staticmethod
    def from_string(pitch):
        if pitch == None: return None

        def get_accidentals(pitch_string):
            accidentals = ""
            if len(pitch_string) == 1:
                return accidentals
            else:
                for temp in pitch_string:
                    if temp == "#" or temp == "b":
                        accidentals += temp
                return accidentals

        def get_octave(pitch_string):
            octave = 4
            try:
                float(pitch_string[-1])
            except ValueError:
                return 4
            else:
                octave = int(pitch_string[-1])
            return octave

        letter = pitch[0]
        octave = get_octave(pitch)
        accidentals = get_accidentals(pitch)

        return _Pitch(letter, accidentals, octave)

    @property
    def letter(self):
        return self._letter

    @property
    def accidentals(self):
        if self._accidental_offset == 0:
            return ''
        elif self._accidental_offset < 0:
            return 'b' * abs(self._accidental_offset)
        else:
            return 'X' * (self._accidental_offset // 2) + '#' * (self._accidental_offset % 2)

    @accidentals.setter
    def accidentals(self, accidentals):
        self._accidental_offset = sum([offset*(sum(map(lambda c: c == accidental, accidentals))) for accidental, offset in {'b':-1, '#':+1, 'X':+2}.items()])
        if self._accidental_offset == 0:
            return ''
        elif self._accidental_offset < 0:
            return 'b' * abs(self._accidental_offset)
        else:
            return 'X' * (self._accidental_offset // 2) + '#' * (self._accidental_offset % 2)

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, octave):
        self._octave = octave
        return True


    def __int__(self):
        letter_offset = {
            'C': 0,
            'D': 2,
            'E': 4,
            'F': 5,
            'G': 7,
            'A': 9,
            'B': 11,
        }[self._letter]


        accidental_offset = self._accidental_offset

        octave_offset = self.octave * 12

        middle_c_offset = -12*4

        return sum([middle_c_offset, letter_offset, accidental_offset, octave_offset])

    def __str__(self):
        return ''.join(map(str, [self.letter, self.accidentals, self.octave]))

    def __eq__(self, other):
        return self.pitch_number == other.pitch_number


    @classmethod
    def int_to_pitch(cls, pitch_number):
        if pitch_number == None: return None
        raise NotImplementedError('TODO')


    def transpose(self, half_steps):
        raise PitcherException('Rests cannot be assigned a pitch')

# class Song(Note, Score, _Music, Chord, Part):
#     def __init__(self, title, subtitle, author, author_email):
#         self._chord = []
#         self._part = []
#         self._measure = []
#         self._notes = []
#         self._score = Score(title, subtitle, author, author_email)

#     @score.setter
#     def add_score(self, score): self._score = score

#     @chord.setter
#     def add_chord(self, chord): self._chord.append(chord)

#     @part.setter
#     def add_part(self, part): self._part.append(part)

#     @measure.setter
#     def add_measure(self, measure): self._measure.append(measure)

#     @note.setter
#     def add_note(self, note): self._notes.append(note)

#     @property
#     def score(self): return self._score

#     @property
#     def measure(self): return self._measure

#     @property
#     def part(self): return self._part

#     @property
#     def chord(self): return self._chord

#     @property
#     def notes(self): return self._notes
