


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



sc = Score()

p = Part()
sc.append_part(p)


melody = Staff(clef=Clef.Treble)
harmony = Staff(clef=Clef.Bass)
p.add_staff(melody)
p.add_staff(harmony)





