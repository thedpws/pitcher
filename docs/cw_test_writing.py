from src.music import *

# https://www.letsplaykidsmusic.com/happy-birthday-easy-piano-music/#:~:text=This%20version%20is%20in%20the,an%20F%20sharp%20(F%23)%20.

piece = Score(title="Happy Birthday", author="Caleb Wong")
part = Part(tempo=125, key_signature=Key.G_MAJOR, time_signature=Time('3/4'))

rh = Staff()
lh = Staff(clef=Clef.BASS)

# 1st measure
rh[0][1.5] = Note('D', 1)
rh[0][2.5] = Note('D', .5)

# 2nd measure
rh[1][0] = Note('E', 1)
lh[1][0] = Chord([Note('G', 3), Note('B', 3), Note('D', 3)])
rh[1][1] = Note('D', 1)
rh[1][2] = Note('G', 1)

# 3rd measure
rh[2][0] = Note('F', 2)
lh[2][0] = Chord([Note('C', 3), Note('D', 3)])
rh[2][2] = Note('D', .75)
rh[2][2.75] = Note('D', .25)

# 4th measure
rh[3][0] = Note('E', 1)
lh[3][0] = Chord([Note('C', 3), Note('D', 3)])
rh[3][1] = Note('D', 1)
rh[3][2] = Note('A', 1)

# 5th measure
rh[4][0] = Note('G', 2)
lh[4][0] = Chord([Note('G', 3), Note('B', 3), Note('D', 3)])
rh[4][2] = Note('D', .75)
rh[4][2.75] = Note('D', .25)

# 6th measure
rh[5][0] = Note('D', 1)
lh[5][0] = Chord([Note('G', 3), Note('B', 3), Note('D', 3)])
rh[5][1] = Note('B', 1)
rh[5][2] = Note('G', 1)

# 7th measure
rh[6][0] = Note('F', 1)
lh[6][0] = Chord([Note('C', 3), Note('E', 3)])
rh[6][1] = Note('E', 1)
rh[6][2] = Note('C5', .75)
rh[6][2.75] = Note('C5', .25)

# 8th measure
rh[7][0] = Note('B', 1)
lh[7][0] = Chord([Note('G', 2), Note('B', 2), Note('D', 2)])
rh[7][1] = Note('G', 1)
rh[7][2] = Note('A', 1)
lh[7][2] = Chord([Note('C', 1), Note('D', 1)])

# 9th measure
rh[8][0] = Note('G', 2)
lh[8][0] = Chord([Note('G', 2), Note('B', 2), Note('D', 2)])

#piece.show()
#piece.listen()