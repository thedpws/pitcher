# must "pip install beautifulsoup4 bs4 lxml" before this will work. These were added to requirements.txt
# currently hard coded for a single file but in future will add functionality to traverse a directory
# currently output is just print to console but in future will send to numpy array or other structure for ML ingestion

from bs4 import BeautifulSoup
import os

path = "../docs/_xml_scores"
score_name = "twoset"   # this is the hardcoded piece that will have to be fixed.
file_name = "score.xml"
target = (f"{path}/{score_name}/{file_name}")
infile = open(target, 'r')
contents = infile.read()
soup = BeautifulSoup(contents, 'xml')
parts = soup.find_all('part')

print("Score Name: %s" % soup.find("work-title").get_text().title())
for part in soup.find_all("part"):
    print("Part: %s" % part.get("id"))
    sign = part.find("sign").get_text()
    line = part.find("line").get_text()
    beats = part.find("beats").get_text()
    beat_type = part.find("beat-type").get_text()
    for measure in part.findChildren("measure"):
        if measure.find("beats"):
            beats = measure.find("beats").get_text()
            beat_type = measure.find("beat-type").get_text()
        if measure.find("clef"):
            sign = measure.find("sign").get_text()
            line = measure.find("line").get_text()
        print(f"\tMeasure: %s \tClef: {sign}{line} \tTime: {beats}/{beat_type}" % measure.get("number"))

        i = 1
        for note in measure.findChildren("note"):
            if note.find("step"):
                step = note.find("step").get_text()
                octave = note.find("octave").get_text()
            else:
                step = "REST"
                octave = "0"
            duration = note.find("duration").get_text()

            print(f"\t\t\tNote: {i} \tStep: {step} \tOctave: {octave} \tDuration: {duration} ")
            i += 1


