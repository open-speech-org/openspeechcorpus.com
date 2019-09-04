import codecs

import os

from applications.isolated_words import models as isolated_words_models

def load_words(file_path):
    """
from isolated_words.load_isolated_words import load_words
load_words("isolated_words/source")
    :param file_path:
    :return:
    """

    categories = os.listdir(file_path)
    for category in categories:
        print("=========")
        print(category)
        print("=========")

        # category, created = isolated_words_models.Category.objects.get_or_create(
        #     name=category.split(".")[0].capitalize()
        # )
        words = codecs.open(os.path.join(file_path, category), encoding="latin1").readlines()
        for word in words:
            print(word.encode("utf8", "ignore").decode())