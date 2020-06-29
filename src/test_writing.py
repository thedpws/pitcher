



from src.music import *


# Simple piano score
"""
In a GUI, I would...
    1. Create the score
    2. Declare the clefs
    3. Be given an empty staff
    4. Start placing notes and chords
"""

pc = Score(title='my piano piece', author='AZ Vasquez')

pt = Part(tempo=96, key_signature=Key.C_MAJOR, time_signature=Time.COMMON_TIME)

# Should default to empty key signature, empty tempo (60 bpm implicit), empty time signature
rh = Staff()

lh = Staff(clef=Clef.BASS)


lh[0][0.0] = Chord([
    Note('C3', 4.0),
    Note('G3', 4.0),
    Note('E4', 4.0),
    Note('C5', 4.0),
])
rh[0][0.0] = Note('C4', 0.5)


# No octave -> should default to 4
rh[0][0.5] = Note('D4', 0.5)
rh[0][1.0] = Note('E4', 0.5)
rh[0][1.5] = Note('F4', 0.5)
rh[0][2.0] = Note('G4', 0.5)
rh[0][2.5] = Note('F4', 0.5)
rh[0][3.0] = Note('E4', 0.5)
rh[0][3.5] = Note('D4', 0.5)

lh[1][0.0] = Chord([
    Note('C3', 1.5),
    Note('E3', 1.5),
    Note('G3', 1.5),
])
rh[1][0.0] = Note('C4', 4.0)


#my_scale = [Note(pitch, 1.0) for pitch in range(0, 7)]


lh[1][1.5] = Chord([
    Note('C3', 0.5),
    Note('E3', 0.5),
    Note('G3', 0.5),
])

lh[1][2.0] = Chord([
    Note('D3', 2.0),
    Note('F#3', 2.0),
    Note('A3', 2.0),
])








# Test Doing a piece with a simple 4 voice arrangement
# In a GUI, I would create the score, declare the clefs, be given an empty staff, and then start placing notes for voice1, voice2, voice3, and voice4

pc = Score(title='My simple 4 voice arrangement', author='AZ Vasquez')

pt = Part(tempo=96, key_signature=Key.C_MAJOR, time_signature=Time.COMMON_TIME)
pc.add_part(pt)

s = Staff(clef=Clef.TREBLE)
pt.add_staff(s)








rh[0].append(Note('D4', 0.5))
rh[0].append(Note('D4', 0.5))
rh[0].append(Rest(0.5))

d_chord = rh[0][1.0]
print(d_chord, d_chord.accidentals)
d_chord.transpose('+3')
print(d_chord, d_chord.accidentals)
d_chord.transpose('+99')
print(d_chord, d_chord.accidentals)
d_chord.transpose('-99')
print(d_chord, d_chord.accidentals)
"""
pc.show()
pc.listen()
pc.save('myfile.pdf')
"""


# getting notes



rh[0].append(Note('D4', 0.5))
rh[0].append(Note('D4', 0.5))
rh[0].append(Note('D4', 0.5))
rh[0].append(Note('D4', 0.5))
rh[0].append(Note('D4', 0.5))
rh[0].append(Note('D4', 0.5))

# 0th measure, 1st beat
rh[0][1.0] = Note('E4', 0.5)

rh[0][1.5] = Note('F4', 0.5)
rh[0][2.0] = Note('G4', 0.5)
rh[0][2.5] = Note('F4', 0.5)
rh[0][3.0] = Note('E4', 0.5)
rh[0][3.5] = Note('D4', 0.5)




#Key.C_MAJOR.scale() # should return list of notes

