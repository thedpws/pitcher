# from playing import *
#from pitchr.music import *
from pitchr.music import *

key(Key.C_MAJOR)
time(Time.COMMON_TIME)

measures = [Measure()]

measures.append(Measure([
    Note('C5', 1.0),
    Note('D5', 1.0),
    Note('E5', 1.0),
    Note('F5', 1.0),
]))

measures.append(Measure([
    Note('G5', 1.0),
    Note('F5', 1.0),
    Note('E5', 1.0),
    Note('D5', 1.0),
]))

measures.append(Measure([
    Note('C5', 0.5),
    Note('D5', 0.5),
    Note('E5', 0.5),
    Note('F5', 0.5),
    Note('G5', 0.5),
    Note('F5', 0.5),
    Note('E5', 0.5),
    Note('D5', 0.5),
]))

measures.append(Measure([
    Note('C5', 1.0)
]))


Part(staffs=[Staff(measures)], tempo=60).play()

Part(staffs=[Staff(measures)], tempo=120).play()
