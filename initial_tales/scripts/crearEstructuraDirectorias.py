#! /usr/bin/python
# -*- coding: UTF-8 -*-
# Copia la estructura de directorios en pathTextos a newPath
from os import listdir, makedirs
from os.path import exists, isdir, abspath, join

# Raiz al sistema de rutas que queremos copiar
pathTextos = abspath("../nuevos-textos")
newPath = "../nuevos-textos-procesados/"

# Creamos la nueva raiz
if not exists(newPath):
    makedirs(newPath)

# Copiamos el sistema de directorios (solo funciona con 1 nivel)
a = listdir(pathTextos)
for b in a:
    if isdir(join(pathTextos, b)):
        makedirs(newPath+b)
