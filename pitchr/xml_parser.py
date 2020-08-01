from bs4 import BeautifulSoup
import os
import pandas as pd
from pitchr.pitch_tagger import tag_pitch
from pitchr.predict import tag_predictability
import numpy as np

circle_of_fifths = [
    'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#',
    'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'
]


def tag_df(df):
    """Adds column information about Pitch and Pitch predictability to a dataframe

    :param df: dataframe of notes
    """
    tag_pitch(df)
    tag_predictability(df)


def prepare_harmony(all_harmony_np):
    """Normalize harmony sizes to 50 notes

    :param all_harmony_np: list of harmony numpy arrays
    :returns all_harmony_np: list of harmony numpy array at size 50
    """
    for i in range(0, 210):
        difference = all_harmony_np[i].shape[0] - 50
        # harmony is too small
        if difference < 0:
            while difference != 0:
                all_harmony_np[i] = np.append(all_harmony_np[i], [[-50, 0]], axis=0)
                difference += 1
        # harmony is too large
        elif difference > 0:
            while difference != 0:
                all_harmony_np[i] = all_harmony_np[i][:-1]
                difference -= 1

    return all_harmony_np


def parse_xml(xml_contents):
    """Parses the contents of a musical XML file

    :param xml_contents: XML contents of file
    :returns melody_dfs: list of dataframes of bins of 50 melody notes
    :returns harmony_dfs: list of dataframes of bins of corresponding harmony notes
    """
    melody_notes = []
    harmony_notes = []
    temp_melody_notes = []
    temp_harmony_notes = []
    melody_dfs = []
    harmony_dfs = []
    measure_split_position = 0
    passed_measure = False
    soup = BeautifulSoup(xml_contents, 'xml')
    parts = soup.find_all('part')
    if soup.find("work-title"):
        title = soup.find("work-title").get_text().title()
    else:
        title = ""

    measure_split = []  # list of measure indexes of 50 melody notes

    for part in parts:
        measure_num = 0
        part_number = int(part.get('id')[-1])
        sign = part.find("sign").get_text()
        line = part.find("line").get_text()
        fifths = part.find("fifths").get_text()
        key = circle_of_fifths[int(fifths)]
        beats = part.find("beats").get_text()
        beat_type = part.find("beat-type").get_text()
        for measure in part.findChildren("measure"):
            measure_num += 1
            if measure.find("divisions"):
                divisions = measure.find("divisions").get_text()
            if measure.find("beats"):
                beats = measure.find("beats").get_text()
                beat_type = measure.find("beat-type").get_text()
            if measure.find("clef"):
                sign = measure.find("sign").get_text()
                line = measure.find("line").get_text()
            for note in measure.findChildren("note"):
                if not note.find("chord"):
                    if note.find("step"):
                        step = note.find("step").get_text()
                        octave = note.find("octave").get_text()
                    else:
                        step = "REST"
                        octave = "0"
                    if note.find("duration"):
                        duration = note.find("duration").get_text()
                    else:
                        duration = "0"
                    if note.find("accidental"):
                        accidental = note.find("accidental").get_text()
                    else:
                        accidental = None

                    duration = int(duration) / int(divisions)

                    # melody
                    if part_number == 1:
                        # only add the note if we have less than 50
                        # If we have more, the rest of the measure is obsolete
                        if len(temp_melody_notes) < 50:
                            temp_melody_notes.append((key, sign, step, octave, accidental, duration))
                        else:
                            melody_notes.append(temp_melody_notes)
                            temp_melody_df = pd.DataFrame(temp_melody_notes, columns=[
                                "Key", "Clef", "Letter", "Octave", "Accidental", "Duration"])
                            melody_dfs.append(temp_melody_df)
                            temp_melody_notes.clear()
                            if len(measure_split) == 0:
                                measure_split.append(measure_num)
                                break
                            else:
                                if measure_split[-1] != measure_num:
                                    measure_split.append(measure_num)
                                break

                    # harmony
                    elif part_number == 2:
                        # add all corresponding harmony until 50th melody note
                        if len(measure_split) != 0 and measure_num <= measure_split[-1]:
                            if (measure_split_position < len(measure_split) and measure_num <= measure_split[
                                measure_split_position]):
                                temp_harmony_notes.append((key, sign, step, octave, accidental, duration))
                            else:
                                harmony_notes.append(temp_harmony_notes)
                                temp_harmony_df = pd.DataFrame(temp_harmony_notes, columns=[
                                    "Key", "Clef", "Letter", "Octave", "Accidental", "Duration"])
                                harmony_dfs.append(temp_harmony_df)
                                temp_harmony_notes.clear()
                                temp_harmony_notes.append((key, sign, step, octave, accidental, duration))
                                measure_split_position += 1

                        # reached end of last interval of 50 melody notes
                        elif len(measure_split) != 0 and measure_num == measure_split[
                            -1] + 1 and passed_measure == False:
                            passed_measure = True
                            harmony_notes.append(temp_harmony_notes)
                            temp_harmony_df = pd.DataFrame(temp_harmony_notes, columns=[
                                "Key", "Clef", "Letter", "Octave", "Accidental", "Duration"])
                            harmony_dfs.append(temp_harmony_df)

            # For edge cases where last note in measure adds to 50
            if len(temp_melody_notes) == 50:
                melody_notes.append(temp_melody_notes)
                temp_melody_df = pd.DataFrame(temp_melody_notes, columns=[
                    "Key", "Clef", "Letter", "Octave", "Accidental", "Duration"])
                melody_dfs.append(temp_melody_df)
                if len(measure_split) != 0 and measure_split[-1] != measure_num:
                    measure_split.append(measure_num)
                temp_melody_notes.clear()

    return melody_dfs, harmony_dfs


def get_all_data():
    """Retrieves all data of songs to train from

    :returns all_melody_dfs: list of all melody dataframes
    :returns all_harmony_dfs: list of all harmony dataframes
    :returns all_melody_durations: list of all melody durations
    """
    all_melody_dfs = []
    all_harmony_dfs = []
    all_melody_durations = []
    path = "../dataset/_xml_scores"
    score_files = os.listdir(path)
    while ".DS_Store" in score_files:
        score_files.remove(".DS_Store")

    for score_name in score_files:
        file_name = "score.xml"
        target = (f"{path}/{score_name}/{file_name}")
        infile = open(target, 'r', encoding='utf-8')
        contents = infile.read()
        infile.close()

        melody_dfs, harmony_dfs = parse_xml(contents)
        difference = len(melody_dfs) - len(harmony_dfs)
        if difference < 0:
            while difference != 0:
                del harmony_dfs[-1]
                difference += 1
        elif difference > 0:
            while difference != 0:
                del melody_dfs[-1]
                difference -= 1

        for df in melody_dfs:
            tag_df(df)
            df['Score Name'] = score_name
            all_melody_dfs.append(df)

            for i, row in df.iterrows():
                if row['Letter'] == "REST":
                    df.at[i, 'Duration'] = -1

            all_melody_durations.append(df['Duration'])

        for df in harmony_dfs:
            tag_df(df)
            df['Score Name'] = score_name
            all_harmony_dfs.append(df)

    return all_melody_dfs, all_harmony_dfs, all_melody_durations
