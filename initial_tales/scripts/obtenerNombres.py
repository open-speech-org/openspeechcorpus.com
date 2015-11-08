#! /usr/bin/python
# -*- coding: UTF-8 -*-
# Extrae todos los nombres de archivos en la ruta pathTextos y los escribe en el archivo nombreArchivo
from os import listdir
from os.path import join, isdir, abspath
files = []
nombreArchivo = "archivos.txt"
# Ruta donde estan los textos en su respectivo sistema de carpetas
pathTextos = abspath("../textos")
a = listdir(pathTextos)
for b in a:
    if isdir(join(pathTextos, b)):
        # Si el archivo es un directorio, accederemos a el
        c = listdir(join(pathTextos, b))
        textosAutor = []
        for d in c:
            # Agregamos los archivos a nuestro texto final
            textosAutor.append(join(pathTextos, b, d))
        files.append(textosAutor)

# Archivo de salida
salida = open(nombreArchivo, 'w+')
for b in files:
    for c in b:
        salida.write(c+"\n")

salida.close()