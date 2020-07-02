import mingus.core.notes as _mingus_notes
from mingus.containers import Note as _MingusNote
import mingus.core.chords as _MingusChord
from mingus.containers import NoteContainer as _MingusNoteContainer
from mingus.containers import Composition as _MingusComposition
from mingus.containers.instrument import Instrument as _MingusInstrument, Piano as _MingusPiano, Guitar as _MingusGuitar
from enum import Enum as _Enum
import re as _re
import pitchr.playing as _playing
import pitchr.lyexport as _showing

"""
.. module:: Pitcher
  :synopsis: A python library and framework for composing music.
.. moduleauthor:: Quarantine Quintet
"""


class PitcherException(Exception):
    pass

class Time:
    """Class representing the Time signature the Score is played in

    :param time: String representing the time signature
    """

    def __init__(self, time):
        if not _re.match(r'\d/\d', time):
            raise PitcherException(f'{time} is an invalid time signature')
        self._time = time

    def __str__(self):
        return self._time

    @property
    def beats_per_measure(self):
        """Get the beats per measure of the Score

        :returns: beats per measure
        """
        return int(self._time.partition('/')[0])

    @property
    def beat_definition(self):
        """Get the beat defition of the Score

        :returns: beat defition
        """
        return int(self._time.partition('/')[2])

    def __eq__(self, other):
        return self._time == other._time

Time.COMMON_TIME = Time('4/4')
Time.CUT_TIME = Time('2/4')

global _time_signature, _key_signature
_time_signature = Time('4/4')
_key_signature = None


def key(key_signature):
    global _key_signature
    _key_signature = key_signature


def time(time_signature):
    global _time_signature
    _time_signature = time_signature


class Key:
    """
        Class representing the Key the Score is played in

        if (flats and sharps) or sharps < 0 or flats < 0 or flats > 7 or sharps > 7:
        :param flats: number of flats in the Key
        :param sharps: number of sharps in the Key
    """

    def __init__(self, flats=0, sharps=0):
        if (flats and sharps) or sharps < 0 or flats < 0 or flats > 7 or sharps > 7:
            raise PitcherException(f'Key signature with {flats} flats and {sharps} sharps is invalid')

        self._flats = flats
        self._sharps = sharps

    def __str__(self):

        return {
            (0, 0): 'c',
            (0, 1): 'g',
            (0, 2): 'd',
            (0, 3): 'a',
            (0, 4): 'e',
            (0, 5): 'b',
            (0, 6): 'f-sharp',
            (0, 7): 'c-sharp',
            (1, 0): 'f',
            (2, 0): 'b-flat',
            (3, 0): 'e-flat',
            (4, 0): 'a-flat',
            (5, 0): 'd-flat',
            (6, 0): 'g-flat',
            (7, 0): 'c-flat', 
        }[(self._flats, self._sharps)] + ' \\major'

    def __eq__(self, other):
        return self._sharps == other._sharps and self._flats == other._flats


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

class Clef(_Enum):
    TREBLE = 0
    BASS = 1


class Voice(_Enum):
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
    """Class representing a collection of parts

       :param parts: [Part]
       :param title: str
       :param subtitle: str
       :param author: str
       :param author_email: str
    """

    def __init__(self, parts=None, title=None, subtitle=None, author=None, author_email=None):
        self._composition = _MingusComposition()
        self._composition.set_author(author, author_email)
        self._composition.set_title(title)

        self._parts = parts or []

    @property
    def composer(self):
        return self._composition.author

    @property
    def author(self):
        """Get the author of the current Score.

        :returns: Author
        """
        return self._composition.author

    @property
    def title(self):
        """Get the title of the current Score.

        :returns: title
        """
        return self._composition.title

    # A little more explicit than "append" or "extend". This is for readability since these are not conventional terms.
    def add_part(self, part):
        """Adds a new Part to the current Score

        :param part: Part
        """
        self._parts.append(part)

    def play(self):
        _playing.play_score(self)

    def show(self):
        _showing.show_score_png(self)

    def save(self, filename):
        _showing.write_to_pdf(self, filename)

    def __iter__(self):
        return iter(self._parts)

    def __getitem__(self, i):
        return self._parts[i]


class Part(_Music):
    """Class representing a collection of staffs. Add effects / stanza-chorus / key/time changes to parts. Should affect its children.

       :param staffs: from Staff()
       :param tempo: int
       :param time_signature: e.g. 3/4
       :param key_signature: int
    """

    @property
    def key_signature(self):
        """Get the key signature of the current Part

        :returns: key signature
        """
        return self._key_signature

    @key_signature.setter
    def key_signature(self, key_signature):
        """Set the key signature of the current Part
        :param key_signature: Key
        """
        self._key_signature = key_signature
    @property
    def time_signature(self):
        """Get the time signature of the current Part

        :returns: time signature
        """
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature):
        """Set the time signature of the current Part
        :param time_signature: Time
        """
        self._time_signature = time_signature

    @property
    def tempo(self):
        return self._tempo

    @tempo.setter
    def tempo(self, tempo):
        self._tempo = tempo

    def __init__(
            self,
            staffs=None,
            tempo=60,
            time_signature=None,
            key_signature=None,
    ):
        self._staffs = staffs or []
        if not time_signature:
            global _time_signature
            time_signature = _time_signature

        if not key_signature:
            global _key_signature
            key_signature = _key_signature

        self._time_signature = time_signature
        self._key_signature = key_signature
        self._tempo = tempo

    def add_staff(self, staff):
        """Adds a staff to the current Part

        :param staff: Staff
        """
        self._staffs.append(staff)

    def play(self):
        return Score(parts=[self]).play()

    def show(self):
        return Score(parts=[self]).show()

    def save(self, filename):
        return Score(parts=[self]).save(filename)

    def __iter__(self):
        return iter(self._staffs)

    def __getitem__(self, i):
        return self._staffs[i]


class Staff(_Music):
    """Class representing a collection of measures.

       :param clef: from Clef()
       :param voice: from Voice()
       :param measures: Measure()
    """


    '''_Collection of measures'''
    def __init__(self, measures=None, clef=Clef.TREBLE, voice=Voice.PIANO):
        self._clef = clef
        self._voice = voice
        self._measures = measures if measures else []

    @property
    def clef(self):
        """Get clef of the Staff

        :returns: clef
        """
        return self._clef

    @clef.setter
    def clef(self, clef):
        """Set clef of the Staff

        :param clef: Clef
        """
        self._clef = clef

    @property
    def voice(self):
        """Get voice of the Staff

        :returns: voice
        """
        return self._voice

    @voice.setter
    def voice(self, voice):
        """Set voice of the Staff

        :param voice: Voice
        """
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

    def save(self, filename):
        return Part(staffs=[self]).save(filename)

    def __iter__(self):
        return iter(self._measures)


# TODO: Bind measure length by global time signature
class Measure(_Music):
    """Class representing a collection of notes.

       :param notes: []
    """

    def __init__(self, notes=None):
        self._notes = dict()
        self._next_count = 0.0

        if notes:
            self.extend(notes)

    def __setitem__(self, start, item):
        self._notes[start] = item
        self._next_count = max(self._next_count, start + item.duration)

    def append(self, item):
        """Adds new note to current measure

        :param item: Note
        """
        # TODO: FIX
        if False and self._next_count + item.duration > _time_signature:
            print("Item exceeds measure's time signature")
        else:
            self._notes[self._next_count] = item
            self._next_count += item.duration

    def extend(self, items):
        """Adds multiple items (chord/notes) to current measure

        :param items: [Note] or [Chord]
        """
        for item in items:
            self.append(item)

    def __getitem__(self, start):
        return self._notes[start]

    def __delitem__(self, start):
        del self._notes[start]

    def __iter__(self):
        return iter(self._notes.values())

    @property
    def duration(self):
        '''Returns the total duration of notes in this measure'''
        return self._next_count

    def __contains__(self, note):
        '''Returns True if note is in this measure'''
        for item in self._notes.values():
            if item == note:
                return True
        else:
            return False

    def extend(self, notes):
        for note in notes:
            self.append(note)

    def play(self):
        return Staff(measures=[self]).play()

    def show(self):
        return Staff(measures=[self]).show()

    def save(self, filename):
        return Staff(measures=[self]).save(filename)


class Chord(_Music):
    """Class representing an organized group of notes.

       :param notes: [Note]
    """

    def __init__(self, notes=None):
        self._notes = notes or []
        #self.__mingus_notes = __MingusNoteContainer()

    def __str__(self):
        return f'{[str(n) for n in self._notes]}'

    def __eq__(self, other):
        val = list(sorted(self.notes)) == list(sorted(other.notes))
        return val

    @staticmethod
    def mingusChord_to_chord(mingus_chord, root):
        my_triad = [root]
        for n in mingus_chord[1:]:
            
            octave = 0
            while Note(str(n) + str(octave), root.duration) < root:
                octave += 1
            my_triad.append(Note(str(n) + str(octave), root.duration))

            #temp = Note.mingusNote_to_note(n, note)
            #my_triad.append(temp)
            
        c = Chord(my_triad)
        return c

    @staticmethod
    def major_triad(note):
        """Get the major triad of a Note

        :param note: Note
        :returns: Chord
        """
        mingus_chord = _MingusChord.major_triad(note.letter)
        return Chord.mingusChord_to_chord(mingus_chord, note)

    @staticmethod
    def minor_triad(note):
        """Get the minor triad of a Note

        :param note: Note
        :returns: Chord
        """
        mingus_chord = _MingusChord.minor_triad(note.letter)
        return Chord.mingusChord_to_chord(mingus_chord, note)

    @staticmethod
    def diminished_triad(note):
        """Get the diminished triad of a Note

        :param note: Note
        :returns: Chord
        """
        mingus_chord = _MingusChord.diminished_triad(note.letter)
        return Chord.mingusChord_to_chord(mingus_chord, note)

    @staticmethod
    def augmented_triad(note):
        """Get the augmented triad of a Note

        :param note: Note
        :returns: Chord
        """
        mingus_chord = _MingusChord.augmented_triad(note.letter)
        return Chord.mingusChord_to_chord(mingus_chord, note)

    @staticmethod
    def suspended_triad(note):
        """Get the suspended triad of a Note

        :param note: Note
        :returns: Chord
        """
        mingus_chord = _MingusChord.suspended_triad(note.letter)
        return Chord.mingusChord_to_chord(mingus_chord, note)

    @property
    def duration(self):
        """Get the duration of a Chord

        :returns: duration
        """
        return max(map(lambda n: n.duration, self._notes)) if self._notes else 0.0

    def __iter__(self):
        return iter(self._notes)

    @property
    def notes(self):
        """Get the notes of a Chord

        :returns: [Note]
        """
        return self._notes

    def append(self, note):
        """Append a note to a Chord

        :param note: Note
        """
        self._notes.append(note)

    def remove(self, note):
        """Remove a note from a Chord

        :param note: Note
        """
        self._notes = [n for n in self._notes if n != note]
        #self.__mingus_notes.remove_note(note.mingus())

    def clear(self):
        """Clears all notes from a Chord"""
        #self.__mingus_notes.empty()
        self._notes.clear()

    def determine(self):
        mingus_chord = _MingusNoteContainer([n.letter for n in sorted(self.notes)])
        return mingus_chord.determine()
      
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

    def save(self, filename):
        return Measure(notes=[self]).save(filename)

class Note(_Music):
    """Class representing the smallest unit for the Pitcher.

       :param pitch: string with letter name, accidentals, and octave, such as 'A#4'
       :param duration: note duration
       :param dynamic: dynamic, such as piano, forte, crescendo, etc
       :param articulation: articulation, such as staccato, accent, fermata, etc
    """

    def __str__(self):
        return f'Note({self.letter}{self.octave}, {self.duration})'

    def __eq__(self, other):
        return self.pitch_number == other.pitch_number and self.duration == other.duration

    def __lt__(self, other):
        return (self.pitch_number, self.duration) < (other.pitch_number, other.duration)

    def __str__(self):
        return f'{self.letter} {self.duration}'

    @staticmethod
    def mingusNote_to_note(mingus_note, note):
        result = Note(mingus_note + note.accidentals + str(note.octave), note.duration, note.dynamic, note.articulation)
        return result

    def __init__(self, pitch, duration, dynamic=None, articulation=None):
        self._pitch = _Pitch.from_string(pitch)
        self._duration = duration
        self._dynamic = dynamic  # piano, forte, crescendo, etc
        self._articulation = articulation  # staccato, accent, fermata, etc

        if self.pitch_number != None:
            self._mingus_note = _MingusNote(self.letter, self.octave)

    @property
    def letter(self):
        """Get the letter of a Note

        :returns: letter
        """
        return self._pitch.letter

    @property
    def accidentals(self):
        """Get the accidentals of a Note

        :returns: accidentals (string)
        """
        return self._pitch.accidentals

    @property
    def pitch(self):
        """Get the pitch of a Note

        :returns: String of letter-note, accidentals, and octave
        """
        return str(self._pitch)

    @pitch.setter
    def pitch(self, pitch):
        """Set the pitch of a Note

        :param pitch: String of letter-note, accidentals, and octave
        """
        self._pitch = _Pitch.from_string(pitch)

    @property
    def octave(self):
        """Get the octave of a Note

        :returns: octave
        """
        return self._pitch.octave

    @octave.setter
    def octave(self, octave):
        """Set the octave of a Note

        :param octave: int
        """
        self._pitch.octave = octave

    @property
    def pitch_number(self):
        return int(self._pitch)

    @property
    def duration(self):
        """Get the duration of a Note

        :returns: duration
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Set the duration of a Note

        :param duration: float
        """
        self._duration = duration

    @accidentals.setter
    def accidentals(self, accidentals):
        """Set the accidentals of a Note

         :param accidentals: accidentals
         """
        self._pitch.accidentals = accidentals

    @property
    def dynamic(self):
        """Get the dynamic of a Note

        :returns: dynamic
        """
        return self._dynamic

    @dynamic.setter
    def dynamic(self, dynamic):
        """Set the dynamic of a Note

        :param dynamic: string
        """
        self._dynamic = dynamic

    @property
    def articulation(self):
        """Get the articulation of a Note

        :returns: duration
        """
        return self._articulation

    @articulation.setter
    def articulation(self, articulation):
        """Set the articulation of a Note

        :param articulation: string
        """
        self._articulation = articulation

    def __eq__(self, other):
        return self.duration == other.duration and self.pitch == other.pitch

    # _Mingus interface

    def augment(self):
        """Raises the note by a half step"""
        self._mingus_note = _mingus_notes.augment(str(self._mingus_note))
        self._pitch.accidentals += '#'
        return True

    def diminish(self):
        """Lowers the note by a half step"""
        self._mingus_note = _mingus_notes.diminish(str(self._mingus_note))
        self._pitch.accidentals += 'b'
        return True

    def transpose(self, half_steps):
        """Transpose the Note by half_steps

        :param half_steps: string of +/- and number of half-steps, ex: '+11' or '-4'
        """
        num_half_steps = int(half_steps[1:])
        if half_steps[0] == '+':
            for num in range(num_half_steps):
                self._pitch.accidentals += '#'
        elif half_steps[0] == '-':
            for num in range(num_half_steps):
                self._pitch.accidentals += 'b'

    @property
    def mingus_note(self):
        """Returns mingus note"""
        return self._mingus_note

    def octave_up(self):
        """Raises the Note an octave"""
        self._mingus_note.octave_up()
        self._pitch.octave += 1
        return True

    def octave_down(self):
        """Lowers the Note an octave"""
        self._mingus_note.octave_down()
        self._pitch.octave -= 1
        return True

    def play(self):
        return Measure(notes=[self]).play()

    def show(self):
        return Measure(notes=[self]).show()

    def save(self, filename):
        return Measure(notes=[self]).save(filename)


class Rest(Note):
    """Class representing a Rest Note. Has no pitch. Only duration.

    :param duration: float
    """

    def __init__(self, duration):
        super(Rest, self).__init__(pitch=None, duration=duration)

    def __str__(self):
        return f'Rest {self.duration}'

    def _throw_exception(self):
        raise PitcherException('Rests cannot be assigned a pitch')

    @property
    def letter(self):
        return None

    @letter.setter
    def letter(self, _):
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

    def octave_up(self):
        self._throw_exception()

    def octave_down(self):
        self._throw_exception()


class _Pitch:
    def __init__(self, letter, accidentals=None, octave=4):
        self._letter = letter
        self._accidental_offset = sum([offset*(sum(map(lambda c: c == accidental, accidentals))) for accidental, offset in {'b':-1, '#':+1, 'x':+2}.items()])
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
                    if temp == "#" or temp == "b" or temp == 'x':
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
            return 'x' * (self._accidental_offset // 2) + '#' * (self._accidental_offset % 2)

    @accidentals.setter
    def accidentals(self, accidentals):
        self._accidental_offset = sum([offset*(sum(map(lambda c: c == accidental, accidentals))) for accidental, offset in {'b':-1, '#':+1, 'x':+2}.items()])
  
        if self._accidental_offset == 0:
            return ''
        elif self._accidental_offset < 0:
            return 'b' * abs(self._accidental_offset)
        else:
            return 'x' * (self._accidental_offset // 2) + '#' * (self._accidental_offset % 2)

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

        middle_c_offset = -12 * 4

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
