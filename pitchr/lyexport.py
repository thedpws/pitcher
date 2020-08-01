import os
import re
import subprocess
from tempfile import TemporaryDirectory
from threading import get_ident

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from pitchr.utils import _suppress_stdout_stderr
from pitchr.utils import _verify_lilypond_in_path


def save_string_and_execute_LilyPond_silent(ly_string, filename, command):
    """A helper function for to_png and to_pdf. Should not be used directly.
    :param ly_string:
    :param filename:
    :param command:
    :return: true if export was successful, false if failed
    :rtype: bool
    """
    ly_string = '\\version "2.10.33"\n' + ly_string
    if filename[-4:] in [".pdf", ".png"]:
        filename = filename[:-4]
    try:
        f = open(filename + ".ly", "w")
        f.write(ly_string)
        f.close()
    except:
        return False
    command = 'lilypond %s -o "%s" "%s.ly" 2>/dev/null 1>&2' % (command, filename, filename)
    # print("Executing: %s" % command)
    p = subprocess.Popen(command, shell=True).wait()
    os.remove(filename + ".ly")
    return True


def to_png(ly_string, filename):
    """ write lilypond string to PNG using lilypond executable
    :param ly_string:
    :param filename:
    :return: whether export was successful
    :rtype: bool
    """
    return save_string_and_execute_LilyPond_silent(ly_string, filename, "-fpng")


def to_pdf(ly_string, filename):
    """ write lilypond string to PDF using lilypond executable
    :param ly_string:
    :param filename:
    :return: whether export was successful
    :rtype: bool
    """
    return save_string_and_execute_LilyPond_silent(ly_string, filename, "-fpdf")


def to_ly(score):
    """ convert score to lilypond string
    :param score:
    :return: lilypond string
    :rtype: string
    """
    ly_staffs = []
    ly_parts = []
    for part in score:

        time_sig = part.time_signature
        tempo = part.tempo

        durations = {
            1 / 64: '64',

            1 / 32: '32',
            3 / 64: '32.',

            1 / 16: '16',
            3 / 32: '16.',
            9 / 64: '16..',

            1 / 8: '8',
            3 / 16: '8.',
            9 / 32: '8..',

            1 / 4: '4',
            3 / 8: '4.',
            9 / 16: '4..',

            1 / 2: '2',
            3 / 4: '2.',
            9 / 8: '2..',

            1 / 1: '1',
            3 / 2: '1.',
            9 / 4: '1..',
        }

        base = part.time_signature.beat_definition
        durations = {k * base: v for (k, v) in durations.items()}

        def ly_from_note(note):

            MIDDLE = 3
            try:
                letter = note.letter.lower()

                accidentals = note.accidentals
                accidentals = re.sub('#', 'is', accidentals)
                accidentals = re.sub('b', 'es', accidentals)
                accidentals_suffix = accidentals

                if note.octave > MIDDLE:
                    octave_suffix = '\'' * (note.octave - MIDDLE)
                elif note.octave < MIDDLE:
                    octave_suffix = ',' * (MIDDLE - note.octave)
                else:
                    octave_suffix = ''
            except Exception:
                letter = 'r'
                accidentals_suffix = ''
                octave_suffix = ''
                accidentals_suffix = ''

            try:
                duration_suffix = durations[note.duration]
            except KeyError:
                # TODO: make PitcherException
                raise Exception(f'Duration not representable by a note: {note.duration}')

            return letter + accidentals_suffix + octave_suffix + duration_suffix

        ly_staffs = []

        for staff in part:

            voice_i = 0
            ly_voices = []

            some_notes_are_unwritten = True
            while some_notes_are_unwritten:
                some_notes_are_unwritten = False

                def ly_from_item(item):
                    try:
                        iter(item)

                        # Is a chord
                        notes = [n for n in item.notes]
                        note = notes[voice_i]

                        # No index error -> some notes are unwritten
                        nonlocal some_notes_are_unwritten
                        some_notes_are_unwritten = True

                        return ly_from_note(note)

                    except IndexError:
                        # Chord's notes are all written. write hidden rest.
                        return 's' + durations[item.duration]

                    except TypeError:
                        # Is a Note

                        # If note already written
                        if voice_i != 0:
                            # fill with hidden rest
                            return 's' + durations[item.duration]

                        note = item
                        return ly_from_note(note)

                ly_voice_format = '\\new Voice {%s}'

                ly_voice = ly_voice_format % ' '.join([ly_from_item(item) for measure in staff for item in measure])

                if not (ly_voice == (ly_voice_format % '')):
                    ly_voices.append(ly_voice)
                voice_i += 1

            ly_staff_format = '''
\\new Staff <<
    \\numericTimeSignature
    \\time %s
    \\key %s
    \\clef %s
    %s
>>
''' % (part.time_signature, part.key_signature.ly, ['treble', 'bass'][staff.clef.value], '%s')

            if not ly_voices:
                continue
            ly_staff = ly_staff_format % '\n\n'.join(ly_voices)

            ly_staffs.append(ly_staff)

        ly_part_format = '<<\n%s\n>>'

        ly_part = ly_part_format % '\n'.join(ly_staffs)

        ly_parts.append(ly_part)

    ly_staffs = ly_staffs or []
    ly_score = '''
\\score {
    <<
    %s
    >>
}
''' % '\n\n'.join(ly_staffs)

    ly_book_format = '''
\\header {
    title = "%s"
    composer = "%s"
}

#(set-global-staff-size 30)

%s
''' % (score.title or '', score.author or '', '%s')

    ly = ly_book_format % ly_score

    return ly


def write_to_pdf(score, output_file):
    """
    write score to PDF
    :param score:
    :param output_file:
    """
    _verify_lilypond_in_path()

    lilypond_string = to_ly(score)
    to_pdf(lilypond_string, output_file)


def write_to_png(score, output_file):
    """
    write score to PNG
    :param score:
    :param output_file:
    """
    _verify_lilypond_in_path()

    lilypond_string = to_ly(score)
    to_png(lilypond_string, output_file)


def show_score_png(score):
    """Reveals the score in an image form.
    Image will block the current process until it is closed in non-interactive scripts.

    :param score:
    """
    _verify_lilypond_in_path()

    with TemporaryDirectory() as tmpdirname:
        png_filepath = tmpdirname + '/' + str(get_ident()) + '.png'

        lilypond_string = to_ly(score)
        to_png(lilypond_string, png_filepath)

        # im = Image.open(png_filepath)
        im = mpimg.imread(png_filepath)

        # plt.imshow(im, cmap=plt.cm.binary)
        # plt.show()

        height, width, _ = im.shape

        # account for lilypond default text at bottom
        height -= 60

        # Crop
        text_start_row = None
        text_end_row = None
        text_start_col = None
        text_end_col = None

        padding = 10

        for i, p in [(i, p) for i, row in enumerate(im) for p in row]:
            if not p[0]:
                text_start_row = max(i - padding, 0)
                break

        for i, p in [(i, p) for i, row in enumerate(im[-60::-1, :]) for p in row]:
            if not p[0]:
                i = height - 1 - i
                text_end_row = min(i + padding, height - 1)
                break

        for i, p in [(i, p) for i, col in enumerate(im.transpose(1, 0, 2)) for p in col]:
            if not p[0]:
                text_start_col = max(i - padding, 0)
                break

        for i, p in [(i, p) for i, col in enumerate(im.transpose(1, 0, 2)[::-1, :-60]) for p in col]:
            if not p[0]:
                i = width - 1 - i
                text_end_col = min(i + padding, width - 1)
                break

        im_cropped = im[text_start_row:text_end_row, text_start_col:text_end_col]

        with _suppress_stdout_stderr():
            plt.axis('off')
            plt.imshow(im_cropped, cmap=plt.cm.binary)
            plt.show()
