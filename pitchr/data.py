# this script will traverse all files in dataset/_xml_scores

from bs4 import BeautifulSoup
import os
from pitchr.pitch_tagger import tag_pitch
from pitchr.predict import tag_predictability
from pitchr.xml_parser import parse_xml


def tag_df(df):
    tag_pitch(df)
    tag_predictability(df)


def get_tagged_data():
    """Cycles through all data and tags Dataframes with predictability and other values

        :return melody_dfs: list of melody dataframes
        :return harmony_dfs: list of harmony dataframes
    """
    melody_dfs = []
    harmony_dfs = []
    path = "../dataset/_xml_scores"
    score_files = os.listdir(path)

    while ".DS_Store" in score_files:
        score_files.remove(".DS_Store")

    for score_name in score_files:
        file_name = "score.xml"
        target = (f"{path}/{score_name}/{file_name}")
        infile = open(target, 'r', encoding='utf-8')
        contents = infile.read()
        infile.close()
        melody_df, harmony_df = parse_xml(contents)
        tag_df(melody_df)
        tag_df(harmony_df)
        melody_df['Score Name'] = score_name
        harmony_df['Score Name'] = score_name
        melody_dfs.append(melody_df)
        harmony_dfs.append(harmony_df)

    return melody_dfs, harmony_dfs
