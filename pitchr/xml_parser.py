# this script will traverse all files in dataset/_xml_scores

from bs4 import BeautifulSoup
import os
import pandas as pd
from pitchr.pitch_tagger import tag_pitch

circle_of_fifths = [
    'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#',
    'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'
]


def parse_xml(xml_contents):
    """Parses the contents of an XML file

        :input xml_contents: XML contents of the file we want to parse
        :return melody_df: Dataframe of the melody notes
        :return harmony_df: Dataframe of the harmony notes
    """
    melody_notes = []
    harmony_notes = []
    temp_melody_notes = []
    temp_harmony_notes = []
    measure_split_position = 0
    passed_measure = False
    soup = BeautifulSoup(xml_contents, 'xml')
    parts = soup.find_all('part')
    if soup.find("work-title"):
        title = soup.find("work-title").get_text().title()
    else:
        title = ""

    # list of measure indexes of 50 notes of harmony
    measure_split = []
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

                    # melody part
                    if part_number == 1:
                        # only add the melody note if we have less than 50 notes.
                        # If we have more, the rest of the measure is obsolete
                        if len(temp_melody_notes) < 50:
                            temp_melody_notes.append((key, sign, step, octave, accidental, duration))
                        else:
                            melody_notes.append(temp_melody_notes)
                            print("temp_melody_notes.length:", len(temp_melody_notes))
                            print("last thing in melody_notes", len(melody_notes[-1]))
                            temp_melody_notes.clear()
                            if len(measure_split) == 0:
                                measure_split.append(measure_num)
                                break
                            else:
                                if measure_split[-1] != measure_num:
                                    measure_split.append(measure_num)
                                break


                    # harmony part
                    elif part_number == 2:
                        if measure_num <= measure_split[-1]:
                            if (measure_split_position < len(measure_split) and measure_num <= measure_split[
                                measure_split_position]):
                                temp_harmony_notes.append((key, sign, step, octave, accidental, duration))
                            else:
                                harmony_notes.append(temp_harmony_notes)
                                print("temp_harmony_notes.length:", len(temp_harmony_notes))
                                temp_harmony_notes.clear()
                                temp_harmony_notes.append((key, sign, step, octave, accidental, duration))
                                measure_split_position += 1
                        elif measure_num == measure_split[-1] + 1 and passed_measure == False:
                            passed_measure = True
                            harmony_notes.append(temp_harmony_notes)


            if len(temp_melody_notes) == 50:
                # double-checks for adding the same measure
                melody_notes.append(temp_melody_notes)
                if measure_split[-1] != measure_num:
                    measure_split.append(measure_num)
                temp_melody_notes.clear()



    print("measure_split:", measure_split)
    print(type(melody_notes), len(melody_notes))
    print(type(harmony_notes), len(harmony_notes))
    for thing in melody_notes:
        print(len(thing))
    for thing in harmony_notes:
        print(len(thing))
    #melody_notes = np.reshape(melody_notes, (-1, 6))
    #harmony_notes = np.reshape(harmony_notes, (-1, 6))


    """
    melody_df = pd.DataFrame(melody_notes, columns=[
        "Key", "Clef", "Letter", "Octave", "Accidental", "Duration"
    ])
    harmony_df = pd.DataFrame(harmony_notes, columns=[
        "Key", "Clef", "Letter", "Octave", "Accidental", "Duration"
    ])
    
    return melody_df, harmony_df
    """
