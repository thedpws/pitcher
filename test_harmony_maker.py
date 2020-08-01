from pitchr.music import *


melody = Staff([

    Measure([
        Note('C', 1.0),
        Note('D', 1.0),
        Note('E', 1.0),
        Rest(1.0),
    ]),

    Measure([
        Note('G', 1.0),
        Note('F', 1.0),
        Note('E', 1.0),
        Note('D', 1.0),
    ]),

    Measure([
        Note('C', 4.0),
    ])


])


from pitchr import harmony_maker


harmony = harmony_maker.build_harmony(melody)
harmony.show()
harmony.play()
for n in [n for measure in harmony for n in measure]:
    print(n.pitch_number)
