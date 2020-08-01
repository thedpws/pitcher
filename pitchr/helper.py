import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper
from ctypes import *
from pitchr.music import *
from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick
import sys

"""
Starter UI for learning Pitchr
"""

def window_border():
    window = curses.newwin(24, 80)
    window.border()
    window.refresh()
    return window


def show_menu(stdscr):
    menu = curses.newwin(11, 40, 2, 20)
    menu.refresh()
    menu.border()

    stdscr.addstr(3, 22, "[N] How to create a note?")
    stdscr.addstr(4, 22, "[M] How to create a measure?")
    stdscr.addstr(6, 22, "[S] How to create a staff?")
    stdscr.addstr(5, 22, "[P] How to create a part?")
    stdscr.addstr(7, 22, "[C] How to create a score?")
    stdscr.addstr(8, 22, "[Y] How to play a song?")
    stdscr.addstr(9, 22, "[W] Play a sample song!")
    stdscr.addstr(10, 22, "[E] Export sample song.")
    stdscr.addstr(11, 22, "[Q] Quit this helper.")
    return menu


def center_txt(msg, row, window):
    num_rows, num_cols = window.getmaxyx()
    middle_column = int(num_cols / 2)
    half_msg = int(len(msg) / 2)
    x_pos = middle_column - half_msg
    window.addstr(row, x_pos, msg)


def dialog1_box(prompt):
    dialog1 = curses.newwin(6, 78, 17, 1)
    dialog1.border()
    center_txt(prompt, 1, dialog1)
    return dialog1


def explanation(title, text1, text2, stdscr):
    curses.flash()
    textkey = curses.newwin(10, 76, 13, 2)
    textkey.border()
    textkey.refresh()
    stdscr.addstr(14, 4, title)
    stdscr.addstr(16, 4, text1)
    stdscr.addstr(18, 4, text2)


def export_sample_song(stdscr):
    f = open("example.py", "w+")
    f.write("from pitchr.music import *")
    f.write("\n")
    f.write("from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick")
    f.write("\n")
    f.write("\n")

    f.write("key(Key.C_MAJOR)")
    f.write("\n")
    f.write("time(Time.COMMON_TIME)")
    f.write("\n")
    f.write("\n")

    f.write("m = Measure()")
    f.write("\n")
    f.write("m[0] = Note('C5', 3/2)")
    f.write("\n")
    f.write("m[1.5] = Note('D5', 1/2)")
    f.write("\n")
    f.write("m[2] = Note('E5', 3/2)")
    f.write("\n")
    f.write("m[3.5] = Note('C5', 1/2)")
    f.write("\n")
    f.write("\n")

    f.write("n = Measure()")
    f.write("\n")
    f.write("n[0] = Chord([Note('G5', 1), Note('D5', 2), Note('G4', 2), Note('B4', 2)])")
    f.write("\n")
    f.write("n[1] = Note('F5', 1)")
    f.write("\n")
    f.write("n[2] = Chord([Note('C4', 2), Note('E5', 2), Note('G4', 2)])")
    f.write("\n")
    f.write("\n")

    f.write("s = Staff(measures=[m, n])")
    f.write("\n")
    f.write("\n")

    f.write("s.play()")
    explanation("This song have been exported to Python code to the current folder.",
                "It contains the exact data structures from this song.",
                "To play, run from the terminal: python3 example.py", stdscr)


def run_gui(stdscr):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)

    window = window_border()
    window.addstr(1, 25, "Welcome to the Pitchr Framework!")
    window.refresh()
    menu = show_menu(stdscr)
    menu.refresh()

    stdscr.refresh()

    while True:
        ch = stdscr.getch()
        if (chr(ch) == 'n' or chr(ch) == 'N'):
            explanation("To create a note:", "note = Note(pitch='C4', duration=1.0).",
                        "You can also add dynamics, such as Note('C4', 1.0, 'forte')", stdscr)
        elif (chr(ch) == 'm' or chr(ch) == 'M'):
            explanation("To create a measure:", "m1 = Measure(Note('C4', 1/2))",
                        "To add a second note, you cal also do: m1[0.5] = Note('E5', 3/2)", stdscr)
        elif (chr(ch) == 's' or chr(ch) == 'S'):
            explanation("To create a staff:", "m1 = Measure(Note('C4', 1/2))",
                        "Staff(m1, Clef.TREBLE, Voice.PIANO)", stdscr)
        elif (chr(ch) == 'p' or chr(ch) == 'P'):
            explanation("To create a part:", "A part is a collection of Staff()",
                        "part = Part(Staff(), tempo, time_signature, key_signature)", stdscr)
        elif (chr(ch) == 'c' or chr(ch) == 'C'):
            explanation("To create a score:", "A score has only informational value.",
                        "s = Score('My Song', 'Wonderful Subtitle', 'Author Me', 'me@email.com')", stdscr)
        elif (chr(ch) == 'y' or chr(ch) == 'Y'):
            explanation("First initialize: time(Time.COMMON_TIME)", "Play an entire staff: Staff([measures]).play()",
                        "To play a single note: Note('C4', 1.0).play()", stdscr)
        elif (chr(ch) == 'e' or chr(ch) == 'E'):
            export_sample_song(stdscr)
        elif (chr(ch) == 'w' or chr(ch) == 'W'):
            explanation("Playing song...", "", "", stdscr)
            stdscr.refresh()
            key(Key.C_MAJOR)
            time(Time.COMMON_TIME)
            m = Measure()
            m[0] = Note('C5', 3 / 2)
            m[1.5] = Note('D5', 1 / 2)
            m[2] = Note('E5', 3 / 2)
            m[3.5] = Note('C5', 1 / 2)

            n = Measure()

            n[0] = Chord([
                Note('G5', 1),
                Note('D5', 2),
                Note('G4', 2),
                Note('B4', 2),
            ])

            n[1] = Note('F5', 1)

            n[2] = Chord([
                Note('C4', 2),
                Note('E5', 2),
                Note('G4', 2),
            ])

            s = Staff(measures=[m, n])
            save_stdout = sys.stdout
            sys.stdout = open('.trash', 'w')

            s.play()
            sys.stdout = save_stdout

        elif (chr(ch) == 'q' or chr(ch) == 'Q'):
            curses.beep()
            break


def main():
    wrapper(run_gui)


if __name__ == "__main__":
    main()
