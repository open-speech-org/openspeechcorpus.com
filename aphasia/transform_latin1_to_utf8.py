import codecs
from os import listdir, mkdir
from os.path import exists, isdir, abspath, join


def transform_file_to_utf_8_from(file_path, in_encoding="latin1", out_file_name=""):
    """
from transform_latin1_to_utf8 import transform_file_to_utf_8_from
transform_file_to_utf_8_from("lexicon/nivel_1.txt")
    Util function to transform a TXT file in encoding `in_encoding` to UTF-8
    :param file_path: 
    :param in_encoding:
    :param out_file_name:
    :return: 
    """
    in_file = codecs.open(file_path, encoding=in_encoding)
    in_lines = in_file.readlines()
    if not out_file_name:
        out_file_name = file_path.replace(".txt", ".utf8.txt")
    out_file = codecs.open(out_file_name, "w+")
    for line in in_lines:
        out_file.write(line)
    out_file.close()


def get_all_files_and_nested(file_path):
    """
from transform_latin1_to_utf8 import get_all_files_and_nested
get_all_files_and_nested("lexicon")
    :param file_path: 
    :return: 
    """
    stack_dirs = list()
    all_files = list()
    first_level_files = listdir(file_path)
    for f in first_level_files:
        full_f_path = join(file_path, f)
        if isdir(full_f_path):
            stack_dirs.append(full_f_path)
        else:
            all_files.append(full_f_path)
    for d in stack_dirs:
        all_files.extend(get_all_files_and_nested(d))
    return all_files


def transform_all_files(in_folder, out_folder):
    """
from transform_latin1_to_utf8 import transform_all_files
transform_all_files("lexicon", "lexicon_utf_8")
    :param in_folder: 
    :param out_folder: 
    :return: 
    """
    if not exists(out_folder):
        mkdir(out_folder)
    all_files = get_all_files_and_nested(in_folder)
    for in_file in all_files:
        out_file_name = in_file.replace(in_folder, out_folder)
        transform_file_to_utf_8_from(in_file, out_file_name=out_file_name)
