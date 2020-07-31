
from pitchr.music import Score, Part, Measure, Note, time, Time

def measures_from_dataframe(harmony_df, durations, time_signature):

    time(Time(time_signature))

    # Zip df with durations

    harmony_df['Duration'] = durations

    notes = list(harmony_df.apply(lambda row: Note(int(row['Pitch Number']), float(row['Duration'])), axis=1))

    beat_count, beat_type = map(int, time_signature.partition('/')[::2])

    time(Time(time_signature))

    measures = []

    for i in range(len(notes) // beat_count):
        start = i * beat_count
        end = min((i + 1) * beat_count, len(notes))
        measure_notes = notes[start:end]
        measures.append(Measure(measure_notes))





    return measures
