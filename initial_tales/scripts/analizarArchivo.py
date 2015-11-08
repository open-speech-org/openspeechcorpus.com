#! /usr/bin/python3
import sys
sys.path.append('/home/vagrant/freeling-3.1/APIs/python')
import freeling
import codecs


print ("Definiendo Freeling Dir")
FREELINGDIR = "/usr/local"
print ("Definiendo freeling data")
DATA = FREELINGDIR+"/share/freeling/"
LANG="es"
print ("obteniendo el locale")
freeling.util_init_locale("default")
print ("Creando el analizador")
# create language analyzer
la=freeling.lang_ident(DATA+"common/lang_ident/ident-es.dat")
print ("Creando las operaciones")
# create options set for maco analyzer. Default values are Ok, except for data files.
op = freeling.maco_options("es")
op.set_active_modules(0, 1, 1, 1, 1, 1, 1, 1, 1, 1)
print ("Obteneiendo los diccionarios")
op.set_data_files("",DATA+LANG+"/locucions.dat", DATA+LANG+"/quantities.dat",
                  DATA+LANG+"/afixos.dat", DATA+LANG+"/probabilitats.dat",
                  DATA+LANG+"/dicc.src", DATA+LANG+"/np.dat",
                  DATA+"common/punct.dat")

print ("Creando los analizadores")
# create analyzers
tk = freeling.tokenizer(DATA+LANG+"/tokenizer.dat")
sp = freeling.splitter(DATA+LANG+"/splitter.dat")
mf = freeling.maco(op)

print ("Creando las HMM")
tg = freeling.hmm_tagger(DATA+LANG+"/tagger.dat", 1, 2)
sen = freeling.senses(DATA+LANG+"/senses.dat")

print ("Creando los parsers")
parser = freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat")
dep = freeling.dep_txala(DATA+LANG+"/dep/dependences.dat", parser.get_start_symbol())

# archivo con rutas a archivos con el texto
archivos = codecs.open("/shared/proyecto/scripts/archivos.txt", 'r', 'utf-8')
lineasArchivos = archivos.readlines()
for archivo in lineasArchivos:
    print ("Procesando: "+archivo)
    # Ruta de salida a los textos procesados con la misma estructura de directorios
    salida = codecs.open('../textos-procesados/'+archivo.split('/')[-2]+'/'+archivo.split('/')[-1], 'w+', 'utf-8')
    archivoAbierto = codecs.open(archivo.replace('\n', ''), 'r', 'utf-8')
    lineasArchivo = archivoAbierto.readlines()
    for lin in lineasArchivo:

        l = tk.tokenize(lin)
        ls = sp.split(l, " ")

        ls = mf.analyze(ls)
        ls = tg.analyze(ls)
        ls = sen.analyze(ls)
        ls = parser.analyze(ls)
        ls = dep.analyze(ls)

        ## output results
        for s in ls:
            ws = s.get_words()
            for w in ws :
                # print(w.get_form()+" "+w.get_lemma()+" "+w.get_tag())
                salida.write(w.get_form()+" "+w.get_lemma()+" "+w.get_tag()+"\n")

    salida.close()

