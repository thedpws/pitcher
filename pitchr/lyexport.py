
from mingus.extra.lilypond import to_png, to_pdf
from tempfile import TemporaryDirectory
from threading import get_ident
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import numpy as np




def to_ly(score):

    ly_staffs = []
    ly_parts = []
    for part in score:

        time_sig = part.time_signature
        key_sig = part.key_signature
        tempo = part.tempo

        durations = {
            1/64 : '64',

            1/32 : '32',
            3/64 : '32.',

            1/16 : '16',
            3/32 : '16.',
            9/64 : '16..',

            1/8 : '8',
            3/16 : '8.',
            9/32 : '8..',


            1/4 : '4',
            3/8 : '4.',
            9/16 : '4..',

            1/2 : '2',
            3/4 : '2.',
            9/8 : '2..',

            1/1  : '1',
            3/2  : '1.',
            9/4  : '1..',
        }

        base = part.time_signature.beat_definition
        durations = {k*base : v for (k,v) in durations.items()}

        def ly_from_note(note):

            MIDDLE = 3
            try:
                letter = note.letter.lower()

                if note.octave > MIDDLE:
                    octave_suffix = '\'' * (note.octave - MIDDLE)
                elif note.octave < MIDDLE:
                    octave_suffix = ',' * (MIDDLE - note.octave)
                else:
                    octave_suffix = ''
            except Exception:
                letter = 'r'
                octave_suffix = ''

            try:
                duration_suffix = durations[note.duration]
            except KeyError:
                # TODO: make PitcherException
                raise Exception(f'Duration not representable by a note: {note.duration}')

            return letter + octave_suffix + duration_suffix

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
                        return  's' + durations[item.duration]

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
''' % (part.time_signature, part.key_signature, ['treble', 'bass'][staff.clef.value], '%s')


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

%s
''' % (score.title or '', score.author or '', '%s')


    ly = ly_book_format % ly_score


    return ly


def write_to_pdf(score, output_file):

    lilypond_string = to_ly(score)
    to_pdf(lilypond_string, output_file)

def write_to_png(score, output_file):

    lilypond_string = to_ly(score)
    to_png(lilypond_string, output_file)


def show_score_png(score):

    with TemporaryDirectory() as tmpdirname:
        png_filepath = tmpdirname + '/' + str(get_ident()) + '.png'

        lilypond_string = to_ly(score)
        to_png(lilypond_string, png_filepath)

        #im = Image.open(png_filepath)
        im = mpimg.imread(png_filepath)

        height, width, _ = im.shape

        # account for lilypond default text at bottom
        height -= 40



        # Crop
        text_start_row = None
        text_end_row = None
        text_start_col = None
        text_end_col = None

        found_text = False

        padding = 10

        # This could be a lot more performant. However, The best possible algorithm will have runtime O(n), n is number of pixels
        for row in range(height):
            found_text = False
            for col in range(width):
                p = im[row][col]
                if [p[0], p[1], p[2]] != [1., 1., 1.]:
                    text_start_row = max(row - padding, 0)
                    found_text = True
                    break
            if found_text:
                break

        for row in reversed(range(height)):
            found_text = False
            for col in reversed(range(width)):
                p = im[row][col]
                if [p[0], p[1], p[2]] != [1., 1., 1.]:
                    text_end_row = min(row + padding, height-1)
                    found_text = True
                    break
            if found_text:
                break

        for col in range(width):
            found_text = False
            for row in range(height):
                p = im[row][col]
                if [p[0], p[1], p[2]] != [1., 1., 1.]:
                    text_start_col = max(col - padding, 0)
                    found_text = True
                    break
            if found_text:
                break

        for col in reversed(range(width)):
            found_text = False
            for row in reversed(range(height)):
                p = im[row][col]
                if [p[0], p[1], p[2]] != [1., 1., 1.]:
                    text_end_col = min(col+padding, width)
                    found_text = True
                    break
            if found_text:
                break

        im = im[text_start_row:text_end_row, text_start_col:text_end_col]


        plt.axis('off')
        plt.imshow(im)
        plt.show()



