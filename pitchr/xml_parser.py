# this script will traverse all files in dataset/_xml_scores

from bs4 import BeautifulSoup
import os
import pandas as pd
from pitchr.pitch_tagger import tag_pitch

circle_of_fifths = [
        'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#',
        'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'
]


def parse_mxl(mxl):
    notes = []
    soup = BeautifulSoup(mxl, 'xml')
    parts = soup.find_all('part')
    if soup.find("work-title"):
        title = soup.find("work-title").get_text().title()
    else:
        title = ""
    for part in soup.find_all("part"):
        sign = part.find("sign").get_text()
        line = part.find("line").get_text()
        fifths = part.find("fifths").get_text()
        key = circle_of_fifths[int(fifths)]
        beats = part.find("beats").get_text()
        beat_type = part.find("beat-type").get_text()
        for measure in part.findChildren("measure"):
            if measure.find("beats"):
                beats = measure.find("beats").get_text()
                beat_type = measure.find("beat-type").get_text()
            if measure.find("clef"):
                sign = measure.find("sign").get_text()
                line = measure.find("line").get_text()

            i = 1
            for note in measure.findChildren("note"):
                if note.find("step"):
                    step = note.find("step").get_text()
                    octave = note.find("octave").get_text()
                else:
                    step = "REST"
                    octave = "0"
                if note.find("duration"):
                    duration = note.find("duration").get_text()
                else:
                    duration = "missing"
                if note.find("accidental"):
                    accidental = note.find("accidental").get_text()
                else:
                    accidental = None
                if note.find("voice"):
                    voice = note.find("voice").get_text()
                else:
                    voice = None
                notes.append((key, sign, voice, step, octave, accidental, duration))
                i += 1

    df = pd.DataFrame(notes, columns=[
        "Key", "Clef", "Voice", "Letter", "Octave", "Accidental", "Duration"
    ])

    return df
