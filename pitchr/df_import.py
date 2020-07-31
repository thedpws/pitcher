
from pitchr.music import Score, Part, Measure, Note, time, Time

def measures_from_dataframe(harmony_df, durations, time_signature):
    """Transform a dataframe of Pitch Numbers into a list of measures

    :param harmony_df: Dataframe with column 'Pitch Number'
    :param durations: a list of float detailing corresponding durations of each row in harmony_df
    :param time_signature: string. Example: '4/4'

    """

    time(Time(time_signature))

    harmony_df['Duration'] = durations

    notes = list(harmony_df.apply(lambda row: Note(int(row['Pitch Number']), float(row['Duration'])), axis=1))

    time(Time(time_signature))

    measures = []

    m = Measure()

    while notes:
        try:
            print(notes[0])
            m.append(notes[0])
            notes.pop(0)
        except Exception:
            measures.append(m)
            m = Measure()

    measures.append(m)


    return measures
