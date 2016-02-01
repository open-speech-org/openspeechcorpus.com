#! /usr/bin/python
# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isdir, join
import codecs
from openspeechcorpus.apps.tales import models as tales_models

def load_authors(file_path):
    a = listdir(file_path)
    for b in a:
        if isdir(join(file_path, b)):
            author_name = humanizate(b)
            author = tales_models.Author(name=author_name)
            author.save()
            c = listdir(join(file_path, b))
            for d in c:
                title = humanizate(d)
                tale = tales_models.Tale(title=title, author=author)
                tale.save()
                print title
                i = 1
                tale_content = codecs.open(join(file_path, b, d), 'r', 'utf-8')
                lines = tale_content.readlines()
                for line in lines:
                    tale_sentence = tales_models.TaleSentence(
                        tale=tale,
                        place=i,
                        text=line
                    )
                    tale_sentence.save()
                    i += 1



def humanizate(string):
    new_string = string.replace('.txt', '')
    new_string = new_string.replace('_', ' ')
    new_string = new_string[:1].upper()+new_string[1:]
    return new_string

# load_authors("../textos-procesados/")
load_authors("initial_tales/nuevos-textos-procesados")