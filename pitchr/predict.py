import collections

# Local testing
from pitchr.music import *


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

    def find_in_tuples(self, note_tuple, tuples):
        for t in tuples:
            if (t == note_tuple):
                return True
        
        return False

    def qtd_in_tuples(self, note_tuple, tuples):
        found_pair = 0
        found_single = 0
        for t in tuples:
            if (t == note_tuple):
                found_pair = found_pair + 1

        for t in tuples:
            if (t[0] == note_tuple[0]):
                found_single = found_single + 1

        return (found_single, found_pair)


    def novel(self):
        base = self._get_base(self._measure)
        tuples = []
        novelty = []
        i = 0

        while(i < (len(base)-1)):
            this_tuple = tuple((base[i], base[i+1]))
            if (len(tuples) == 0): 
                novelty.append(0.0)
            else:
                if not self.find_in_tuples(this_tuple, tuples): 
                    novelty.append(0.0)
                else:
                    (found_single, found_pair) = self.qtd_in_tuples(this_tuple, tuples)
                    novelty.append(float('%.2f' % (found_pair/found_single)))

            tuples.append(this_tuple)
            i = i+1
        return novelty

key(Key.C_MAJOR)
time(Time.COMMON_TIME)

melody = [
    Note('C', 1.0), # Predictability: 0.0 
    Note('D', 1.0), # 0.0
    Note('E', 1.0), # 0.0

    Note('C', 1.0), # 0.0
    Note('D', 1.0), # 1.0
    Note('E', 1.0), # 1.0

    Note('C', 1.0), # 1.0
    Note('D', 1.0), # 1.0
    Note('G', 1.0), # 0.0
    Note('F', 1.0), # 0.0
    Note('E', 1.0), # 0.0

    Note('C', 1.0), # 1.0
    Note('D', 1.0), # 1.0
    Note('E', 1.0), # 0.67
    Note('C', 1.0), # 1.0
    Note('D', 1.0), # 1.0
    Note('G', 1.0), # 0.33
    Note('C5', 1.0) # 0.0
]

q = 0
m = Measure()
while (q < len(melody)):
    m[q] = melody[q]
    q = q+1

p = Predict(m)
novelty = p.novel()
print(novelty)

# def predict(notes_df):
#     notes_df['Pitch Predictability'] = notes_df.apply(lambda _: 0.0, axis=1)
