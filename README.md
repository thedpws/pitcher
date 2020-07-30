# Pitchr
A python library and framework for composing music.

## Features

1. Enables creation of music by composition of music objects (notes, chords, measures, and staffs)
2. Unified interface for playing any music object (`note.play()`, `staff.play()`)
3. Unified interface for showing any music object (`note.show()`, `staff.show()`)
  * Spawns an image of the music object
4. Unified interface for exporting any music object (`note.save('note.pdf')`, `staff.save('staff.pdf')`)
5. Flexible manipulation of music
  * easily access notes by indexing a measure by beat: `note0 = measure[0]`
  * edit note attributes' pitch via methods `transpose`, `octave_up`, `augment`
6. Finalizes your composition as beautiful standard sheet music
7. Enables interactive development in Jupyter Notebook

## Installation
`pip install pitchr`.  Make sure pip points to pip3 not pip2. [Pitchr on PyPI](https://pypi.org/project/pitchr/)
`lilypond` is required for listening.

## Documentation
Documentation is hosted on Github Pages [here](https://thedpws.github.io/pitcher/)


## Getting Started
```python
from pitchr import *

# Instantiate notes
n = Note(pitch='C4', duration=1.0)

# Play them
n.play()

# Write music

m = Measure([
    Note('C', 1.0),
    Note('D', 1.0),
    Note('E', 1.0),
    Note('F', 1.0),
    Note('G', 1.0),
    Note('F', 1.0),
    Note('E', 1.0),
    Note('D', 1.0),
    Note('C', 4.0),
])

# See what you've written
m.show()

# Export to PDF
m.save('MySong.pdf')
```

## More Detailed Notes

![flow](https://raw.githubusercontent.com/thedpws/pitcher/master/demo/flow.png)


## Note() class

**Init**:
- `pitch` (`"C#6"`)
- `duration` in beats
- `dynamic` (piano, forte, crescendo)
- `articulation` (staccato, accent, fermata)

### Note()
    from pitchr import *
    note1 = Note("C4", 1, "forte")
    note1.mingus_note # 'C-4'
    note1.duration # 1
    note1.dynamic # "forte"
    note1.augment() or note1.diminish()

### Chords
    note2. = Note("E4", 1)
    chord1 = Chord([note1, note2])
    chord1.determine() # "Major third"

### Measure is a collection of Notes
    measure1 = Measure([note1, note2])
    measure1.contains(note1) # True
    measure1.append(note3)

### Staff is a collection of Measures

**Init**:
- `measures`
- `clef`
- `voice`https://thedpws.github.io/pitcher/

`staff1 = music.Staff(measure1, Clef.TREBLE, Voice.PIANO)`


### Part is a collection of Staffs

    part1 = Part(staff1, tempo, time_signature, key_signature)
    part1.add_staff(staff2)
    part1.time_signature = 3/4

### Score is a collection of Parts

    score1 = Score("My Song", "Wonderful Subtitle", "Author Me", "me@email.com")
    score1.get_author() # "Author Me"
    score1.get_title() # "My Song"
    score1.add_part(part1)

## Running all Pitchr tests
```bash
./run_pitchr_tests.sh
```

# Contributing
### Setting up dependencies
* python3.8 is required for pitchr and python3 should link to python3.8 to run the tests
* `ln -s /usr/bin/python3.8 /usr/bin/python3`
* To create the virtual environment, `cd` into the project directory and `python3 -m venv env`
* To install dependencies to the virtual environment, `source env/bin/activate && pip3 install -r requirements.txt`
* Install these dependencies using your local package manager (ex. `sudo apt install python3-dev python3-venv libasound2 libasound2-dev lilypond`):
  * `python3-dev`
  * `python3-venv`
  * `libasound2`
  * `libasound2-dev`
  * `lilypond`

### Working on the project
* Before working, activate the environment by `source env/bin/activate`
* Deactivate by `deactivate`
