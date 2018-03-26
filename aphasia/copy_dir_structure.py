# -*- coding: UTF-8 -*-
"""
Based on `initial_tales/crearEstructuraDirectorias.py`
"""

from os import listdir, makedirs
from os.path import exists, isdir, abspath, join


def copy_dir_structure_from_to(from_dir, to_dir):
    """
from copy_dir_structure import copy_dir_structure_from_to
copy_dir_structure_from_to("lexicon", "lexicon_utf_8")
    :param from_dir: 
    :param to_dir: 
    :return: 
    """

    # First we create the root
    if not exists(to_dir):
        makedirs(to_dir)

    # We copy first level schema
    # TODO: Make recursive in all levels
    a = listdir(from_dir)
    for b in a:
        if isdir(join(from_dir, b)):
            makedirs("{}/{}".format(to_dir, b.replace(" ", "_")))
