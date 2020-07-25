# this script will traverse all files in dataset/_xml_scores

from bs4 import BeautifulSoup
import os
import pandas as pd
from pitchr.pitch_tagger import tag_pitch
from pitchr.predict import tag_predictability
from pitchr.xml_parser import parse_xml


def tag_df(df):
    tag_pitch(df)
    tag_predictability(df)


def get_tagged_data():
    dfs = []

    path = "../dataset/_xml_scores"
    score_files = os.listdir(path)

    if os.path.exists(".DS_Store"):
        score_files.remove(".DS_Store")

    for score_name in score_files:
        notes = []
        file_name = "score.xml"
        target = (f"{path}/{score_name}/{file_name}")
        infile = open(target, 'r', encoding='utf-8')
        contents = infile.read()
        infile.close()

        df = parse_xml(contents)
        tag_df(df)
        dfs.append(df)
    return dfs
