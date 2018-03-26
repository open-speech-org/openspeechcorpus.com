#! /usr/bin/python
# -*- coding: UTF-8 -*-
"""
Based on `initial_tales/load_initial_tales.py`
"""
from os import listdir
from os.path import isdir, join
import codecs
from applications.aphasia import models as aphasia_models


def load_levels(file_path):
    """
from aphasia.load_initial_aphasia_words import load_levels
load_levels("aphasia/lexicon_utf_8")
    :param file_path: 
    :return: 
    """
    a = listdir(file_path)
    for b in a:
        if isdir(join(file_path, b)):
            level_name = humanizate(b)
            print(level_name)
            level = aphasia_models.Level(title=level_name)
            level.save()
            c = listdir(join(file_path, b))
            for d in c:
                title = humanizate(d)
                print("-{}".format(title))
                level_category = aphasia_models.LevelCategory(
                    title=title,
                    level=level
                )
                level_category.save()
            #     print(title)
                level_content = codecs.open(join(file_path, b, d), 'r', 'utf-8')
                lines = level_content.readlines()
                for line in lines:
                    print("--{}".format(line))
                    level_sentence = aphasia_models.LevelSentence(
                        level_category=level_category,
                        text=line
                    )

                    level_sentence.save()


def humanizate(string):
    new_string = string.replace('.txt', '')
    new_string = new_string.replace('_', ' ')
    new_string = new_string[:1].upper()+new_string[1:]
    return new_string

# load_authors("../textos-procesados/")
# load_authors("initial_tales/nuevos-textos-procesados")
