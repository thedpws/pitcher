from pitchr.music import Measure, Note, time, Time, Rest

def measures_from_ml_output(pitches, durations, time_signature):
    """Transform an array of Pitch Numbers into a list of measures

    :param pitches: Numpy.array of int32
    :param durations: a list of float detailing corresponding durations of each row in harmony_df
    :param time_signature: string. Example: '4/4'
    :returns measures: list of measures
    """

    time(Time(time_signature))

    pitches = map(int, pitches)

    notes = [Note(pitch_number, duration) if duration > 0 else  Rest(-1*duration) for (pitch_number,duration) in zip(pitches, durations)]

    time(Time(time_signature))

    measures = [Measure()]

    while notes:
        try:
            measures[-1].append(notes[0])
            notes.pop(0)
        except Exception:
            measures.append(Measure())

    return measures

