#! /usr/bin/python
# -*- encoding: UTF-8 -*-

import codecs
import re
from itertools import chain

archivos = codecs.open("archivos.txt", 'r', 'utf-8')
lineasArchivos = archivos.readlines()
for archivo in lineasArchivos:
    print ("Procesando: "+archivo)
    # Ruta de salida a los textos procesados con la misma estructura de directorios
    salida = codecs.open('../textos-procesados/'+archivo.split('/')[-2]+'/'+archivo.split('/')[-1], 'w+', 'utf-8')
    archivoAbierto = codecs.open(archivo.replace('\n', ''), 'r', 'utf-8')
    lineasArchivo = archivoAbierto.readlines()
    tokens = []
    for lin in lineasArchivo:
        tokens = list(chain(tokens, (re.split(': |; |\. |\n', lin))))
    for token in tokens:
        if token:
            salida.write(token+"\n")
    salida.close()