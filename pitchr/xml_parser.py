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
    temp_harmony_notes = []
    temp_melody_notes = []
    another_temp_melody_notes = []
    soup = BeautifulSoup(xml_contents, 'xml')
    parts = soup.find_all('part')
    if soup.find("work-title"):
        title = soup.find("work-title").get_text().title()
    else:
        title = ""

    # list of measure indexes of 50 notes of harmony
    measure_split = []
    for part in reversed(parts):
        measure_num = -1
        part_number = int(part.get('id')[-1])
        print("Part_number:", part_number)
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
                        for ms in measure_split:
                            if measure_num <= ms:
                                temp_melody_notes.append((key, sign, step, octave, accidental, duration))
                            else:
                                
                                for note in temp_melody_notes:
                                    print(note[2]+str(note[4]), end=",")
                                print()

                                melody_notes.append(temp_melody_notes)
                                temp_melody_notes.clear()

                    # harmony part
                    elif part_number == 2:
                        # only add the harmony note if we have less than 50 notes.
                        # If we have more, the rest of the measure is obsolete
                        if len(temp_harmony_notes) < 50:
                            temp_harmony_notes.append((key, sign, step, octave, accidental, duration))
                        else:
                            harmony_notes.append(temp_harmony_notes)
                            if len(measure_split) == 0:
                                measure_split.append(measure_num)
                            else:
                                if measure_split[-1] != measure_num:
                                    measure_split.append(measure_num)
            if len(temp_harmony_notes) == 50:
                for note in temp_harmony_notes:
                    print(note[2]+str(note[4]), end=",")
                print()

                # double-checks for adding the same measure
                if measure_split[-1] != measure_num:
                    measure_split.append(measure_num)
                temp_harmony_notes.clear()

        print("measure_split:", measure_split)
        

    


    """
    melody_df = pd.DataFrame(melody_notes, columns=[
        "Key", "Clef", "Letter", "Octave", "Accidental", "Duration"
    ])
    harmony_df = pd.DataFrame(harmony_notes, columns=[
        "Key", "Clef", "Letter", "Octave", "Accidental", "Duration"
    ])
    
    return melody_df, harmony_df
    """