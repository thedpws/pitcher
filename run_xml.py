from pitchr.music import *


from pitchr.data import get_tagged_data


dfs = get_tagged_data()

for df in dfs:
    print(df[df['Voice'] == '1'])
    print(df[df['Voice'] == '2'])
