import os

import mingus.extra.lilypond as LilyPond
from music import *


class Export:

    def convert_to_lilypond_note(self, note):
        pitch = note.pitch_number
        accidental = note.accidentals.replace("#", "is") \
            .replace("b", "es")

        octave = note.octave
        octave_str = ""

        if octave >= 4:
            num_octaves = octave - 4
            octave_str += "'" * num_octaves
        elif octave <= 2:
            num_octaves = 3 - octave
            octave_str += "'" * num_octaves

        lily_note = f"{pitch}{accidental}{octave_str}"
        return lily_note

    def build_lilypond_str(self, score):
        lilypond_str = ""
        for part in score:
            for staff in part:
                if staff.clef == Clef.TREBLE:
                    lilypond_str += r"\new Staff { "
                    for measure in staff:
                        for note in measure:
                            lilypond_str += self.convert_to_lilypond_note(note)
                    lilypond_str += " }"
                else:
                    lilypond_str += r"\new Staff { \clef "
                    for measure in staff:
                        for note in measure:
                            lilypond_str += self.convert_to_lilypond_note(note)
                    lilypond_str += " }"
        return lilypond_str

    def which(self, program):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

    def toPNG(self, score, output_file):
        lilypond_str = self.build_lilypond_str(score)

        print(f"\n_____________'lilypond_str' = '{lilypond_str}'_____________\n")
        if not self.which("lilypond"):
            raise PitcherException("lilypond does not exist in path!")
        LilyPond.to_png(lilypond_str, output_file)

    def toPDF(self, score, output_file):
        lilypond_str = self.build_lilypond_str(score)

        print(f"\n_____________'lilypond_str' = '{lilypond_str}'_____________\n")

        if not self.which("lilypond"):
            raise PitcherException("lilypond does not exist in path!")
        LilyPond.to_pdf(lilypond_str, output_file)
