


from playing import *
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


print('Playing measure')
m.play()

print('Playing staff')
s = Staff(measures=[m, n])
s.play()



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


melody[0].extend([ Rest(2.5), Note('Eb', 1/2), Note('G', 1/2), Note('Ab5', 1/2) ])
melody[1].extend([ Note('Bb5', 3/2), Note('Bb5', 1/2), Note('Bb5', 1/2), Note('C5', 1/2), Note('Bb5', 1/2), Note('Ab5', 1/2) ])
melody[2].extend([ Note('G', 1), Note('F', 5/2), Note('E', 1/2) ])
melody[3].extend([ Note('F', 3/2), Note('G', 1/2), Note('Ab5', 1/2), Note('F', 1/2), Note('Bb5', 1/2), Note('Ab5', 1/2) ])
melody[4].extend([ Note('G', 2.5) ])



harmony[0].extend([ Rest(2.5), Note('G3', 1/2), Note('Bb4', 1/2), N2('Ab4') ])
harmony[1].extend([ Note('G3', 5/2), N2('Ab4'), N2('G3'), N2('C4') ])
harmony[2].extend([ Note('Bb4', 1), Note('Ab4', 5/2), N2('G3') ])
harmony[3].extend([ Note('Ab4', 3/2), Note('G3', 1/2), N2('F3'), N2('Ab4'), N2('G3'), N2('C4') ])
harmony[4].extend([ Note('Bb4', 5/2) ])


bass[1].append(Note('Eb3', 4))
bass[2].append(Note('Bb3', 3.5))
bass[3].append(Note('Bb3', 4))
bass[4].append(Note('Eb3', 2.5))



print('Playing part')
p.play()


