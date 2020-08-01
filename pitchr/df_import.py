
from pitchr.music import Score, Part, Measure, Note, time, Time

def measures_from_ml_output(pitches, durations, time_signature):
    """Transform an array of Pitch Numbers into a list of measures

    :param pitches: Numpy.array of int32
    :param durations: a list of float detailing corresponding durations of each row in harmony_df
    :param time_signature: string. Example: '4/4'
    :returns measures: list of measures
    """

    time(Time(time_signature))

    pitches = list(map(int, pitches))

    notes = [Note(pitch, duration) for (pitch,duration) in zip(pitches, durations)]
    print(len(notes))
    print(type(notes))
    print(notes)
    count = 0
    time(Time(time_signature))

    measures = [Measure()]

    while notes:
        try:
            measures[-1].append(notes[0])
            notes.pop(0)
        except Exception:
            measures.append(Measure())
            count += 1

    print("made", count, "measures")
    return measures

