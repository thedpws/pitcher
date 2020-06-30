


#from showing import *
from music import *

key(Key.C_MAJOR)
time(Time.COMMON_TIME)

m = Measure()


m[0] = Note('C5', 3/2)
m[1.5] = Note('D5', 1/2)
m[2] = Note('E5', 3/2)
m[3.5] = Note('C5', 1/2)



n = Measure()

n[0] = Chord([
    Note('G5', 1),
    Note('D5', 2),
    Note('G4', 2),
    Note('B5', 2),
])

n[1] = Note('F5', 1)

n[2] = Chord([
    Note('C4', 2),
    Note('E5', 2),
    Note('G4', 2),
])


#m.show()

s = Staff(measures=[m, n])
#s.show()



class N2(Note):
    def __init__(self, pitch):
        super(N2, self).__init__(pitch=pitch, duration=1/2)

sc = Score()

p = Part(tempo=100)
sc.add_part(p)


melody = Staff(clef=Clef.TREBLE)
harmony = Staff(clef=Clef.BASS)
bass = Staff(clef=Clef.BASS)
p.add_staff(melody)
p.add_staff(harmony)
p.add_staff(bass)


melody[0].extend([ Rest(2.0), Rest(1/2), Note('Eb', 1/2), Note('G', 1/2), Note('Ab4', 1/2) ])
melody[1].extend([ Note('Bb4', 3/2), Note('Bb4', 1/2), Note('Bb4', 1/2), Note('C4', 1/2), Note('Bb4', 1/2), Note('Ab4', 1/2) ])
melody[2].extend([ Note('G', 1), Note('F', 2.0), Note('F', 0.5), Note('E', 1/2) ])
melody[3].extend([ Note('F', 3/2), Note('G', 1/2), Note('Ab', 1/2), Note('F', 1/2), Note('Bb', 1/2), Note('Ab', 1/2) ])
melody[4].extend([ Note('G', 2.0), Note('G', 1/2) ])



harmony[0].extend([ Rest(2.0), Rest(1/2), Note('G3', 1/2), Note('Bb3', 1/2), N2('Ab3') ])
harmony[1].extend([ Note('G3', 2.0), Note('G3', 0.5), N2('Ab3'), N2('G3'), N2('C4') ])
harmony[2].extend([ Note('Bb3', 1), Note('Ab3', 2.0), Note('Ab3', 0.5), N2('G3') ])
harmony[3].extend([ Note('Ab3', 3/2), Note('G3', 1/2), N2('F3'), N2('Ab3'), N2('G3'), N2('C4') ])
harmony[4].extend([ Note('Bb3', 2.0), Note('Bb3', 0.5) ])

bass[0].append(Rest(4.0))
bass[1].append(Note('Eb3', 4))
bass[2].append(Note('Bb2', 2.0))
bass[2].append(Note('Bb2', 0.5))
bass[2].append(Rest(1.5))
bass[3].append(Note('Bb2', 4))
bass[4].append(Chord(notes=[Note('Eb3', 1/2), Note('F', 1), Note('G', 2)]))



p.show()


