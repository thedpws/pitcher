# Pitchr
A python library and framework for composing music.

## Installation
`pip install pitchr`.  Make sure pip points to pip3 not pip2. [Pitchr on PyPI](https://pypi.org/project/pitchr/)

## Documentation
Documentation is hosted on Github Pages [here](https://thedpws.github.io/pitcher/)


## Getting Started
```
from pitcher import *

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

# Contributing
### Setting up dependencies
* To create the virtual environment, `cd` into the project directory and `python3 -m venv env`
* To install dependencies to the virtual environment, `source env/bin/activate && pip3 install -r requirements.txt`
* Install these dependencies using your local package manager (ex. `sudo apt install python3-dev`):
  * `python3-dev`
  * `libasound2`
  * `lilypond`

### Working on the project
* Before working, activate the environment by `source env/bin/activate`
* Deactivate by `deactivate`
