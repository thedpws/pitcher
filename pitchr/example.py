from pitchr.music import *
from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick

key(Key.C_MAJOR)
time(Time.COMMON_TIME)

m = Measure()
m[0] = Note('C5', 3/2)
m[1.5] = Note('D5', 1/2)
m[2] = Note('E5', 3/2)
m[3.5] = Note('C5', 1/2)

n = Measure()
n[0] = Chord([Note('G5', 1), Note('D5', 2), Note('G4', 2), Note('B4', 2)])
n[1] = Note('F5', 1)
n[2] = Chord([Note('C4', 2), Note('E5', 2), Note('G4', 2)])

s = Staff(measures=[m, n])

s.play()