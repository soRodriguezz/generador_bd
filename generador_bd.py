import os
import sys
import random
from random import randint
import datetime
from itertools import cycle

# DEFINICION DE ARRAYS
paises_array = []
companies_array = []
languages_array = []
last_names_array = []
men_names_array = []
women_names_array = []

# LEER .TXT 
paises_file = open("data/country.txt", "r", )
companies_file = open("data/companies.txt", "r")
languages_file = open("data/languages.txt", "r")
last_names_file = open("data/last_names.txt", "r")
men_names_file = open("data/men_names.txt", "r")
women_names_file = open("data/women_names.txt", "r")

# CALCULAR FECHA ALEATORIA
def fecha_aleatoria():
    mes_fecha = random.randint(1, 12)
    ano_fecha = random.randint(1950, 2020)

    if mes_fecha == 2:
        dia_fecha = random.randint(1, 28)
    elif mes_fecha == 4 or mes_fecha == 6 or mes_fecha == 9 or mes_fecha == 11:
        dia_fecha = random.randint(1,30)
    else:
        dia_fecha = random.randint(1, 31)
    
    fecha_random = (str(ano_fecha)+ "-" + str(mes_fecha).zfill(2) + "-" + str(dia_fecha).zfill(2))
    return fecha_random

# GENERO ALEATORIO
def genero_aleatorio():
    genero = random.randint(1,1000)
    genero_random = genero % 2

    if genero_random == 1:
        genero_text = "Masculino"
    else:
        genero_text = "Femenino"
    return genero_text

# RECORRIDO DE LISTA
def listado_random(lista):
    return lista[random.randint(0, len(lista) - 1)]

# CARGAR DE ARCHIVOS
def cargar_data_files(data_file, data_array):
    for x in data_file:
        data_array.append(str(x).strip())

# CALCULAR DIGITO VERIFICADOR
def digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return (-s) % 11

# PREPARACION DE CARGA DE DATOS
def preparar_data_en_memoria():
    cargar_data_files(paises_file, paises_array)
    cargar_data_files(companies_file, companies_array)
    cargar_data_files(languages_file, languages_array)
    cargar_data_files(last_names_file, last_names_array)
    cargar_data_files(men_names_file, men_names_array)
    cargar_data_files(women_names_file, women_names_array)

# GENERAR CADENAS Y PASAR FUNCIONES A VARIABLES
def generar_registro_persona():
    empleador = listado_random(companies_array)
    pais = listado_random(paises_array)
    apellido_1 = listado_random(last_names_array)
    apellido_2 = listado_random(last_names_array)
    idioma = listado_random(languages_array)
    fecha_nacimiento = fecha_aleatoria()
    run_num = str(randint(1000000, 30000000))

    run_dv = str(digito_verificador(run_num))
    genero_persona = genero_aleatorio()
    nombre_persona = ''

    if (genero_persona == 'Femenino'):
        nombre_persona = listado_random(women_names_array)
    else:
        nombre_persona = listado_random(men_names_array)

    #return "INSERT INTO "+ name_table +" VALUES("+ run_num.zfill(8)+"-"+run_dv+","+nombre_persona+","+apellido_1+","+apellido_2+","+fecha_nacimiento+","+genero_persona+","+idioma+","+pais+","+empleador+");"
    return "INSERT INTO %s VALUES ('%s-%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (name_table, run_num.zfill(8), run_dv, nombre_persona, apellido_1, apellido_2, fecha_nacimiento, genero_persona,idioma,pais,empleador)

# GENERADOR DE SQL
if __name__ == "__main__":
    try:
        preparar_data_en_memoria()
        name_db = sys.argv[1]
        name_table = sys.argv[2]
        cantidad_registros_soliticados = int(sys.argv[3])
        fecha_proceso = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        nombre_archivo_salida = "sql/" + fecha_proceso + "_bd.sql"
        data_out_registros = open(nombre_archivo_salida, "w")
        data_out_registros.write("CREATE DATABASE "+ name_db +";\n")
        data_out_registros.write("CREATE TABLE "+ name_table +"(rut VARCHAR(11), nombre VARCHAR(20), apellido1 VARCHAR(25), apellido2 VARCHAR(25), fecha_nacimiento VARCHAR(20), genero VARCHAR(15), idioma VARCHAR(20), pais VARCHAR(30), empleador VARCHAR(30));\n")
        for x in range(cantidad_registros_soliticados):
            data_out_registros.write(generar_registro_persona()+"\n")
        print("SQL generado")
    except IndexError as e:
        print("Programa recibe un parametro numerico, cantidad de registros solicitados")
        print("EJEMPLO: python Generar_Personas.py name_db name_table 100")
    except IOError as e:
        print("directorio de salida no existe, entonces se crea, debes volver a ejecutar la instruccion!!!")
        os.mkdir("sql")
