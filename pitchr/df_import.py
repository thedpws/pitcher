
from pitchr.music import Score, Part, Measure, Note, time, Time

def measures_from_dataframe(pitches, durations, time_signature):
    """Transform a dataframe of Pitch Numbers into a list of measures

    :param pitches: Numpy.array of int32
    :param durations: a list of float detailing corresponding durations of each row in harmony_df
    :param time_signature: string. Example: '4/4'
    :returns measures: list of measures
    """

    time(Time(time_signature))

    pitches = list(map(int, pitches))


    notes = [Note(pitch, duration) for (pitch,duration) in zip(pitches, durations)]

    time(Time(time_signature))

    measures = [Measure()]

    while notes:
        try:
            measures[-1].append(notes[0])
            notes.pop(0)
        except Exception:
            measures.append(Measure())

    return measures

