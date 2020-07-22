import collections

#
from pitchr.music import *
from mido import Message, MidiFile, MidiTrack, bpm2tempo, tempo2bpm, tick2second, second2tick
#

# To download the needed libraries:
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')

# coding=utf-8

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class Predict():
    def __init__(self, measure):
        self._measure = measure

    def _get_base(self, m):
        base = []
        i = 0
        while (i < m._next_count):
            base.append(m[i].letter)
            i = i + m[i].duration

        return base

    def predict2(self):
        base = self._get_base(self._measure)
        words = [base[len(base)-2], base[len(base)-1]]
        bigrams = []
        suggestions = []

        print(base)
        print(words)

        for i in range(0, len(base)):
            if (i == len(base)-1):
                break
            else:
                if(base[i] == words[1] and base[i-1] == words[0]):
                    bigrams.append(base[i+1])

        counter = collections.Counter(bigrams)
        
        for i in range(0,len(counter.most_common())):
            if(i>=3):
                break
            else:
                suggestions.append(counter.most_common()[i][0])
        return suggestions

# key(Key.C_MAJOR)
# time(Time.COMMON_TIME)

# m = Measure()

# m[0] = Note('C5', 3/2)
# m[1.5] = Note('D5', 1/2)
# m[2] = Note('E5', 3/2)
# m[3.5] = Note('C5', 1/2)
# t = 1
# m[4] = Note('C5', t)
# m[5] = Note('D5', t)
# m[6] = Note('E5', t)
# m[7] = Note('C5', t)
# m[8] = Note('C5', t)
# m[9] = Note('D5', t)
# m[10] = Note('E5', t)
# m[11] = Note('C5', t)

# p = Predict(m)
# print(p.predict2())