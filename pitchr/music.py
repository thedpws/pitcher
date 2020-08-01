import re as _re
from enum import Enum as _Enum

import mingus.core.chords as _MingusChord
import mingus.core.notes as _mingus_notes
from mingus.containers import Composition as _MingusComposition
from mingus.containers import Note as _MingusNote
from mingus.containers import NoteContainer as _MingusNoteContainer

from mingus.containers import Composition as _MingusComposition
from enum import Enum as _Enum
import re as _re
import pitchr.playing as _playing

import pitchr.lyexport as _showing
import pitchr.playing as _playing

"""
.. module:: Pitcher
  :synopsis: A python library and framework for composing music.
.. moduleauthor:: Quarantine Quintet
"""


class PitcherException(Exception):
    """Exceptions related to Pitcher issues
    """

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
        """Get the beat definition of the Score

        :returns: beat definition
        """
        return int(self._time.partition('/')[2])

    def __eq__(self, other):
        return self._time == other._time


Time.COMMON_TIME = Time('4/4')
Time.CUT_TIME = Time('2/4')

global _time_signature, _key_signature
_time_signature = Time('4/4')


def key(key_signature):
    """Sets the global key signature

    :param key_signature: Key Signature object
    """
    global _key_signature
    _key_signature = key_signature


def time(time_signature):
    """Sets the global time signature

    :param key_signature: Time Signature object
    """
    global _time_signature
    _time_signature = time_signature


class Keyboard:
    """Simulates a piano keyboard. Useful for calculating scales.
    """

    @staticmethod
    def key(i, sharps=True):
        """Given a number, returns the letter of an associated key on the keyboard.
        Middle C is defined to be 0.

        :param i: index of key on keyboard
        :param sharps: if True, gives accidentals in sharp form rather than flat form.

        :returns: letter note of associated key
        """
        return {
            0: ['C', 'C'],
            1: ['Db', 'C#'],
            2: ['D', 'D'],
            3: ['Eb', 'D#'],
            4: ['E', 'E'],
            5: ['F', 'F'],
            6: ['Gb', 'F#'],
            7: ['G', 'G'],
            8: ['Ab', 'G#'],
            9: ['A', 'A'],
            10: ['Bb', 'A#'],
            11: ['B', 'B'],
        }[i % 12][sharps]


class Interval:
    """Stores Pitch Intervals."""
    pass


for halfsteps, attr in enumerate(['m2', 'M2', 'm3', 'M3', 'M4', 'm5', 'M5', 'm6', 'M6', 'm7', 'M7', 'M8']):
    setattr(Interval, attr, halfsteps + 1)


class Key:
    """Class representing the Key the Score is played in

    :param flats: number of flats in the Key
    :param sharps: number of sharps in the Key
    """

    def __init__(self, flats=0, sharps=0):
        if (flats and sharps) or sharps < 0 or flats < 0 or flats > 7 or sharps > 7:
            raise PitcherException(f'Key signature with {flats} flats and {sharps} sharps is invalid')

        self._flats = flats
        self._sharps = sharps

    def __str__(self):
        return self.major_tonic + ' major'

    @property
    def fifths(self):
        """Returns number of fifths that defines this key signature.

        :returns: number of fifths that defines this key signature.
        """
        return self._sharps - self._flats

    @property
    def major_tonic(self):
        """Returns the tonic/root of this key signature, assuming a major key.

        :returns: returns the letter of the key signature's tonic
        """
        return Keyboard.key(self.major_tonic_offset, sharps=self.sharp)

    @property
    def major_tonic_offset(self):
        """Returns the index of the tonic of this key signature.

        :returns: the related offset (in half steps) of this tonic from middle C"""
        return (Interval.M5 * self.fifths) % 12

    @property
    def major_scale(self):
        """Returns the index of the tonic of this key signature.

        :returns: list of strings of the 8 letters representing the major scale associated with this major key"""
        intvs = [0, 2, 2, 1, 2, 2, 2, 1]
        return [Keyboard.key(intv + sum(intvs[:i]) + self.major_tonic_offset, self.sharp) for i, intv in
                enumerate(intvs)]

    @property
    def ly(self):
        """Returns a lilypond string representation of this key signature.
        Consists of the tonic in lowercase with "-is" or "-es" if sharp or flat respectively, and then "\\major".
        :returns: lilypond string representation of this key signature
        """
        tonic = self.major_tonic

        tonic = _re.sub('#', 'is', tonic)
        tonic = _re.sub('b', 'es', tonic)
        tonic = tonic.lower()

        return tonic + ' \\major'

    @property
    def sharp(self):
        """Returns True if this key signature contains sharps
        :returns: this key signature contains sharps
        """
        return self._sharps > 0

    @property
    def flat(self):
        """Returns True if this key signature contains flats
        :returns: this key signature contains flats
        """
        return self._flats > 0

    def __eq__(self, other):
        """Returns True if key signatures share the same definition"""
        return self._sharps == other._sharps and self._flats == other._flats

    def __contains__(self, pitch):
        """Returns True if this key signature has this pitch or Note in its notes

        :param pitch: Note or pitch
        :returns: returns True if this key signature contains this note or pitch
        """

        if isinstance(pitch, Note):
            pitch = pitch.pitch

        pitch = _re.sub('\\d', '', pitch)

        return pitch in self.major_scale


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

_key_signature = Key.C_MAJOR


class Clef(_Enum):
    TREBLE = 0
    BASS = 1


class Voice(_Enum):
    PIANO = 0


class _Music:

    def play(self, **kwargs):
        """Plays music"""
        raise NotImplementedError

    def show(self, **kwargs):
        """Shows a graphic of music"""
        raise NotImplementedError

    def save(self, filename, **kwargs):
        """Saves music to a PDF"""
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
        """Alias for author of the score"""
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
    :param time_signature: instance of Time
    :param key_signature: instance of Key
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

    """_Collection of measures"""

    def __init__(self, measures=None, clef=Clef.TREBLE, voice=Voice.PIANO, time_signature=None):

        if not time_signature:
            global _time_signature
            time_signature = _time_signature
        self._clef = clef
        self._voice = voice
        self._measures = measures if measures else []
        for measure in self._measures:
            measure.time_signature = time_signature
        self._time_signature = time_signature

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

    @property
    def time_signature(self):
        """Get time signature of the Staff

        :returns: time signature
        """
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature):
        """Set time signature of the Staff

        :param time_signature: Time signature
        """
        self._time_signature = time_signature

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

    def __init__(self, notes=None, time_signature=None):
        self._notes = dict()
        self._next_count = 0.0
        if not time_signature:
            global _time_signature
            time_signature = _time_signature
        self._time_signature = time_signature

        if notes:
            self.extend(notes)

    def __setitem__(self, start, item):
        self._notes[start] = item
        self._next_count = max(self._next_count, start + item.duration)

    @property
    def time_signature(self):
        """Get time signature of the Measure

        :returns: time signature
        """
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature):
        """Set time signature of the Measure

        :param time_signature: Time signature
        """
        self._time_signature = time_signature

    def append(self, item):
        """Adds new note to current measure

        :param item: Note
        """
        beats_per_measure = self._time_signature.beats_per_measure  # numerator
        beat_definition = self._time_signature.beat_definition  # denominator
        max_length = 4 * (beats_per_measure * (1 / beat_definition))
        if self._next_count + item.duration > max_length:
            raise PitcherException("Item exceeds measure's time signature")
        else:
            self._notes[self._next_count] = item
            self._next_count += item.duration

    def extend(self, items):
        """Adds multiple items (chord/notes) to current measure

        :param items: [Note] or [Chord]
        """
        beats_per_measure = self._time_signature.beats_per_measure  # numerator
        beat_definition = self._time_signature.beat_definition  # denominator
        max_length = 4 * (beats_per_measure * (1 / beat_definition))
        items_duration = 0
        for item in items:
            items_duration += item.duration
        if self._next_count + items_duration > max_length:
            print("Items exceed measure's time signature")
        else:
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
        """Returns the total duration of notes in this measure"""
        return self._next_count

    def __contains__(self, note):
        """Returns True if note is in this measure"""
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
    def pitch(self):
        """Get the pitch of a Chord

        :returns: String of letter-note, accidentals, and octave
        """
        return str(self._notes[0])

    @property
    def letter(self):
        """Get the letter of a Chord

        :returns: letter
        """
        return self._notes[0].letter

    @property
    def octave(self):
        """Get the octave of a Chord

        :returns: octave
        """
        return self._notes[0].octave

    @property
    def accidentals(self):
        """Get the accidentals of a Chord

        :returns: accidentals (string)
        """
        return self._notes[0].accidentals

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
        # self.__mingus_notes.remove_note(note.mingus())

    def clear(self):
        """Clears all notes from a Chord"""
        self._notes.clear()

    def determine(self):
        """Used to determine the type of chord"""
        mingus_chord = _MingusNoteContainer([n.letter for n in sorted(self.notes)])
        return mingus_chord.determine()

    @staticmethod
    def get_chord(note):
        return Chord.from_shorthand(note)

    @staticmethod
    def get_triads(key):
        """Returns all triads in a given key

        :param key: String
        """
        return Chord.triads(key)


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
    :param tie: when true will play this note continuously into the next note
    """

    def __str__(self):
        return f'Note({self.pitch}, {self.duration})'

    def __repr__(self):
        return f'Note({self.pitch}, {self.duration})'

    def __eq__(self, other):
        return self.pitch_number == other.pitch_number and self.duration == other.duration

    def __lt__(self, other):
        return (self.pitch_number, self.duration) < (other.pitch_number, other.duration)

    @staticmethod
    def mingusNote_to_note(mingus_note, note):
        result = Note(mingus_note + note.accidentals + str(note.octave), note.duration, note.dynamic, note.articulation)
        return result

    def __init__(self, pitch, duration, dynamic=None, articulation=None, tie=False):
        if type(pitch) == str:
            self._pitch = _Pitch.from_string(pitch)
        elif type(pitch) in [int, float]:
            self._pitch = _Pitch.from_int(int(pitch))
        elif pitch is None:
            self._pitch = None
        else:
            raise PitcherException(f'Bad pitch type: {pitch} of type {type(pitch)}')

        self._duration = duration
        self._dynamic = dynamic  # piano, forte, crescendo, etc
        self._articulation = articulation  # staccato, accent, fermata, etc
        self._tie = tie  # if True, no audible break between this note into next note

        if self.pitch_number != None:
            self._mingus_note = _MingusNote(self.letter, self.octave)

    @property
    def letter(self):
        """Get the letter of a Note

        :returns: letter
        """
        return self._pitch.letter

    def get_accidentals_wrt_key(self, key):
        if self.pitch not in key:
            return self._pitch.accidentals
        else:
            return ''

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
        return int(self._pitch) if hasattr(self, '_pitch') else None

    @pitch_number.setter
    def pitch_number(self, pitch):
        self._pitch = _Pitch.from_int(pitch)

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

    @property
    def tie(self):
        """Get the tie status of a Note

        :returns: tie
        """
        return self._tie

    @tie.setter
    def tie(self, tie):
        """Set the tie status of a Note

        :param tie: boolean
        """
        self._tie = tie

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
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
        num_half_steps = int(half_steps)
        if half_steps[0] == '-':
            for num in range(num_half_steps):
                self._pitch.accidentals += 'b'
        else:
            for num in range(num_half_steps):
                self._pitch.accidentals += '#'
        return self

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
    """Represents a pitch. Contains utilities for transforming pitch.

    :param letter: letter of pitch
    :param accidentals: default None, string representation of accidentals
    :param octave: default 4, octave number
    """
    FLAT = 'b'
    SHARP = '#'
    DOUBLE_SHARP = 'x'

    def __init__(self, letter, accidentals=None, octave=4):
        self._letter = letter
        self._accidental_offset = sum(
            [offset * (sum(map(lambda c: c == accidental, accidentals))) for accidental, offset in
             {'b': -1, '#': +1, 'x': +2}.items()])
        self._octave = octave

    @staticmethod
    def from_int(pitch):
        """Returns a _Pitch calculated from an integer representation.
        :returns: instance of _Pitch
        """
        octave = pitch // 12 + 4
        return _Pitch.from_string(''.join([Keyboard.key(pitch), str(octave)]))

    @staticmethod
    def from_string(pitch):
        """Returns a _Pitch calculated from a string representation
        :returns: instance of _Pitch
        """
        if pitch == None: return None

        def get_accidentals(pitch_string):
            accidentals = ""
            if len(pitch_string) == 1:
                return accidentals
            else:
                for temp in pitch_string:
                    if temp == _Pitch.SHARP or temp == _Pitch.FLAT or temp == _Pitch.DOUBLE_SHARP:
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
        """?Returns the letter of this pitch.
        :returns: letter
        """
        return self._letter

    @property
    def accidentals(self):
        """Returns the accidentals of this pitch

        :returns: string of "x", "#", and "b" characters
        """
        if self._accidental_offset == 0:
            return ''
        elif self._accidental_offset < 0:
            return _Pitch.FLAT * abs(self._accidental_offset)
        else:
            return _Pitch.DOUBLE_SHARP * (self._accidental_offset // 2) + _Pitch.SHARP * (self._accidental_offset % 2)

    @accidentals.setter
    def accidentals(self, accidentals):
        """Sets the accidentals of this pitch

        :param accidentals: string of "x", "#", and "b" characters
        """
        self._accidental_offset = sum(
            [offset * (sum(map(lambda c: c == accidental, accidentals))) for accidental, offset in
             {_Pitch.FLAT: -1, _Pitch.SHARP: +1, _Pitch.DOUBLE_SHARP: +2}.items()])

        if self._accidental_offset == 0:
            return ''
        elif self._accidental_offset < 0:
            return _Pitch.FLAT * abs(self._accidental_offset)
        else:
            return _Pitch.DOUBLE_SHARP * (self._accidental_offset // 2) + _Pitch.SHARP * (self._accidental_offset % 2)

    @property
    def octave(self):
        """Returns the octave of this pitch
        :returns: pitch octave
        """
        return self._octave

    @octave.setter
    def octave(self, octave):
        """Sets the octave of this pitch
        :param octave: int
        """
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
