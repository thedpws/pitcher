


from midi2 import *
from music import *

key(Key.C_MAJOR)
time(Time.COMMON_TIME)


m = Measure()


m[0] = Note('C', 3/2)
m[1.5] = Note('D', 1/2)
m[2] = Note('E', 3/2)
m[3.5] = Note('C', 1/2)


midi_file = measure_to_midi(m)


midi_file.save('doremi.mid')

n = Measure()

n[0] = Chord([
    Note('F', 1),
    Note('D', 2),
    Note('G', 2),
    Note('B', 2),
])

n[1] = Note('E', 1)

n[2] = Chord([
    Note('C', 2),
    Note('E', 2),
    Note('G', 2),
])

midi_file = measure_to_midi(n)

midi_file.save('g7toc.mid')
