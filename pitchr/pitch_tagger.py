from pitchr.music import *


def tag_accidentals(notes_df):
    """Tag accidentals to a dataframe of notes

    :param notes_df: dataframe of notes
    """
    # get the corresponding key object
    key = getattr(Key, notes_df.iloc[0]['Key'] + '_MAJOR')

    key_accidentals = {pitch[0]: pitch[1:] or None for pitch in key.major_scale}
    key_accidentals.update({'REST': None})

    # The accidentals gotten from the music xml are relative to the key signature

    # Calculate accidentals wrt key
    notes_df['Accidental'] = notes_df.apply(lambda row: row['Accidental'] or key_accidentals[row['Letter']], axis=1)

    return


def tag_pitch_interval(notes_df):
    """Tag pitch intervals to a dataframe of notes

    :param notes_df: dataframe of notes
    """
    curr_pitch = 0

    def pitch_interval_fn(row):
        nonlocal curr_pitch

        interval = int(row['Pitch Number'] or '0') - curr_pitch
        curr_pitch += interval
        return interval

    notes_df['Pitch Interval'] = notes_df.apply(pitch_interval_fn, axis=1)


def tag_pitch(notes_df):
    """Tags pitch information to a dataframe of notes from XML file

    :param notes_df: dataframe of notes
    """
    tag_accidentals(notes_df)

    def pitch_fn(row):
        if row['Letter'] == 'REST':
            return ''

        return (row['Letter'] or '') + (row['Accidental'] or '') + (row['Octave'] or '')

    notes_df['Pitch'] = notes_df.apply(pitch_fn, axis=1)

    def pitch_number(row):
        if not row['Pitch']:
            return ''
        return Note(row['Pitch'], float()).pitch_number

    notes_df['Pitch Number'] = notes_df.apply(pitch_number, axis=1)

    curr_pitch = 0

    def pitch_interval_fn(row):
        nonlocal curr_pitch

        interval = int(row['Pitch Number'] or '0') - curr_pitch
        curr_pitch += interval
        return interval

    notes_df['Pitch Interval'] = notes_df.apply(pitch_interval_fn, axis=1)
