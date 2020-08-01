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
        Chord(notes=
          [Note('C', 1),
           Note('E', 1),
           Note('G', 1)]),
        Chord(notes=
          [Note('D', 1),
           Note('F#', 1),
           Note('A', 1)]),
        Chord(notes=
          [Note('E', 1),
           Note('G#', 1),
           Note('B', 1)]),
        Chord(notes=
          [Note('F', 1),
           Note('A', 1),
           Note('C', 1)]),
    ]),

    Measure([
        Chord(notes=
          [Note('G', 1),
           Note('B', 1),
           Note('D', 1)]),
        Chord(notes=
          [Note('A', 1),
           Note('C#', 1),
           Note('E', 1)]),
        Note('G', 0.5),
        Note('F', 0.5),
        Note('E', 0.5),
        Note('D', 0.5),
    ]),

    Measure([
        Note('C', 0.5),
        Note('D', 0.5),
        Note('E', 0.5),
        Note('D', 0.5),
        Chord(notes=
          [Note('C', 1),
           Note('E', 1),
           Note('G', 1)]),
    ]),

    Measure([
        Note('C', 0.5),
        Note('G', 0.5),
        Note('D', 0.5),
        Note('A', 0.5),
        Note('E', 0.5),
        Note('B', 0.5),
        Note('F', 0.5),
        Note('C', 0.5),
    ]),

])


from pitchr import harmony_maker

harmony = harmony_maker.build_harmony(melody)

p = Part(staffs=[melody, harmony])
p.play()
p.show()



