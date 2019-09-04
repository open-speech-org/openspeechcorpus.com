
import os

from applications.isolated_words import models as isolated_words_models
from aphasia.load_initial_aphasia_words import humanize

def clear_word(word):
    cleaned_word = word.replace("ï»¿", "")
    cleaned_word = cleaned_word.replace("Â¿", "¿")
    cleaned_word = cleaned_word.replace("Ã¡", "á")
    cleaned_word = cleaned_word.replace("Ã©", "é")
    cleaned_word = cleaned_word.replace("Ã­", "í")
    cleaned_word = cleaned_word.replace("Ã³", "ó")
    cleaned_word = cleaned_word.replace("Ãº", "ú")
    cleaned_word = cleaned_word.replace("Ã±", "ñ")
    return cleaned_word

def load_words(file_path):
    """
# First transform all files to  UTF-8
from aphasia import transform_latin1_to_utf8
transform_latin1_to_utf8.transform_all_files("isolated_words/source", "isolated_words/source_utf-8")
from isolated_words.load_isolated_words import load_words
load_words("isolated_words/source_utf-8")
    :param file_path:
    :return:
    """

    categories = os.listdir(file_path)
    for category_file in categories:
        print("=========")
        category_name = humanize(category_file)
        print("=========")

        category, created = isolated_words_models.Category.objects.get_or_create(
            title=category_name
        )
        words = open(os.path.join(file_path, category_file)).readlines()
        for word in words:
            clean_word = clear_word(word).strip()
            print(clean_word)
            isolated_word, created = isolated_words_models.IsolatedWord.objects.get_or_create(
                category=category,
                text=clean_word
            )