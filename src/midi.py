
from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick
from music import Note, Chord



def measure_to_midi(measure):

    tempo = 600


    mid = MidiFile()

    track = MidiTrack()

    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))


    note_pitches = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    note_pitch_nums = [60, 62, 64, 65, 67, 70, 72]


    notedict = dict(zip(note_pitches, note_pitch_nums))
            

    time = 0
    for _, item in sorted(measure._notes.items()):


        if isinstance(item, Note):
            notes = [item]
        elif isinstance(item, Chord):
            notes = item.notes
        else:
            break

        mspb = int(round(tempo * time))

        for note in notes[:1]:
            track.append(Message('note_on', note=notedict[note.pitch], velocity=64, time=mspb))
            track.append(Message('note_off', note=notedict[note.pitch], velocity=64, time=0))
        for note in notes[1:]:
            track.append(Message('note_on', note=notedict[note.pitch], velocity=64, time=0))
            track.append(Message('note_off', note=notedict[note.pitch], velocity=64, time=0))

        time = min(map(lambda n: n.duration, notes))


    return mid




