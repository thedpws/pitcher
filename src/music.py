
'''



Design decisions:


Piece > Parts 
Part > Staves

Part > tempo, time/key signature, staves, brace/bracket 

N-voice staff > measures, clef, instrument/voice

Measure > Notes/Rests, N lines, technique (forte, legato, etc)

Note > pitch, duration

pitch > octave (c3, c4, c5), accidental

1. Parts - Parts are necessary because it is not uncommon to switch tempo, key signatures, vocal arrangements, etc.


2. Indexing - 
    * You should not be able to append a single note to a DS expecting multiple notes (1-voice staff vs 2-voice staff).

    * Indexing a structure accesses its substructures. (In contrast to accessing notes)

    * Notes cannot be indexed using integers since they may appear at half counts.

2. A System is not a DS. It is simply a side effect of how the program decides to format the sheet music. But users should be able to define how many measures are in each system.


4. Reserved keywords
    * Section (Brass section)
    * 

'''

class _Music:

    def listen(self, **kwargs):
        '''Should play music'''
        raise NotImplementedError

    def show(self, **kwargs):
        '''Should show a graphic of music'''
        raise NotImplementedError

    def save(self, filename, **kwargs):
        '''Should save music to a PDF'''
        raise NotImplementedError

class Score(_Music):
    '''Contains textual information and optionally arguments for the first Part'''

    def __init__(self, title=None, subtitle=None):
        self.parts = [Part()]


# Will handle things like repeats, lyrics, 
# How to group into sections (bracket)?
class Part(_Music):
    '''A collection of staffs'''

    @key_signature.setter
    def (self, key_signature):
        pass

    @property
    def key_signature(self):
        pass

    @time_signature.setter
    def (self, time_signature):
        pass

    @property
    def time_signature(self):
        pass


    def __init__(
            self,
            staffs=None,
            time_signature=Time.COMMON_TIME,
            key_signature=Key.C_MAJOR,
    ):
        pass

class _Staff(_Music):

    '''Collection of measuresinstrument/voice'''
    '''Measures must have correct rhythm to be successfully added to a staff in a part'''
    def __init__(self, clef=Clef.TREBLE, voice=Voice.PIANO, measures=None):
        if not measures:
            measures = [Measure()]
        self._measures = []

class VoicedStaff(_Staff):
    '''A staff with distinct voicing'''
    '''Notes must be attached to a specific voice'''

    def __init__(self, clef=Clef.TREBLE, voice=Voice.PIANO):
        self._voices = dict()

    def __getitem__(self, voice):
        return self._voices[voice]

class UnvoicedStaff(_Staff):
    '''A staff without distinct voicing'''
    '''Notes are not attached to voices'''
    pass


# : How to keep all durations rational wrt the time signature?
# TODO: Tremolo

class Note(_Music):
    '''Has pitch and duration. Also accidentals.'''
    def __init__(self, pitch, duration):
        self._pitch = pitch
        self._duration = duration

class Rest(Note):
    '''Has no pitch. Only duration.'''
    def __init__(self, duration):
        super(Rest, self).__init__(pitch=None, duration=duration)



        Piece line issue
        
pitcher.CMajor()

Measure()

# TODO: Look for music dataset
# TODO: Performance angle w/ python lib?
# TODO: Global time signatures
# TODO: Look at Mingus
