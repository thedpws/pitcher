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
    soup = BeautifulSoup(xml_contents, 'xml')
    parts = soup.find_all('part')
    if soup.find("work-title"):
        title = soup.find("work-title").get_text().title()
    else:
        title = ""
    for part in parts:
        part_number = int(part.get('id')[-1])
        sign = part.find("sign").get_text()
        line = part.find("line").get_text()
        fifths = part.find("fifths").get_text()
        key = circle_of_fifths[int(fifths)]
        beats = part.find("beats").get_text()
        beat_type = part.find("beat-type").get_text()
        for measure in part.findChildren("measure"):

            measure_index = measure["number"]

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

                    # melody part
                    if part_number == 1:
                        melody_notes.append((key, sign, measure_index, step, octave, accidental, duration))

                    # harmony part
                    elif part_number == 2:
                        harmony_notes.append((key, sign, measure_index, step, octave, accidental, duration))

    melody_df = pd.DataFrame(melody_notes, columns=[
        "Key", "Clef", "Measure", "Letter", "Octave", "Accidental", "Duration"
    ])
    harmony_df = pd.DataFrame(harmony_notes, columns=[
        "Key", "Clef", "Measure", "Letter", "Octave", "Accidental", "Duration"
    ])

    return melody_df, harmony_df
