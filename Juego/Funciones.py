import csv, json, random

"""
Lee las palabras desde un archivo CSV y las organiza por temáticas.
Parámetros:
- path (str): La ruta al archivo CSV. Por defecto, se asume que está en "Recursos\Archivos\tematicas_palabras.csv".
Retorna:
- dict: Un diccionario donde las claves son las temáticas y los valores son listas de palabras asociadas a cada temática.
"""
def leer_palabras(path: str = r"Recursos\Archivos\tematicas_palabras.csv"):
    tematicas_palabras = {}
    with open(path, newline='', encoding= "utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Leer la primera fila como encabezados
        for row in reader:
            for i, palabra in enumerate(row):
                tematica = headers[i]
                palabra = palabra.lower()
                if tematica not in tematicas_palabras:
                    tematicas_palabras[tematica] = []
                tematicas_palabras[tematica].append(palabra)
    return tematicas_palabras

"""
Selecciona una palabra aleatoria de una temática aleatoria.
Parámetros:
- tematicas_palabras (dict): Un diccionario con temáticas y sus palabras correspondientes.
Retorna:
- tuple: Una tupla con la temática y la palabra seleccionada.
"""
def seleccionar_palabra(tematicas_palabras):
    tematica = random.choice(list(tematicas_palabras.keys()))
    palabra = random.choice(tematicas_palabras[tematica])
    return tematica, palabra

"""
Carga datos desde un archivo JSON.
Parámetros:
- path (str): La ruta al archivo JSON.
Retorna:
- dict: Un diccionario con los datos cargados. Si el archivo no existe o hay un error de decodificación, retorna un diccionario vacío.
"""
def cargar_json(path: str):
    try:
        with open(path, 'r', encoding= "utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
    return data

"""
Guarda datos en un archivo JSON.
Parámetros:
- path (str): La ruta al archivo JSON.
- data (dict): El diccionario con los datos a guardar.
"""
def guardar_json(path: str, data):
    with open(path, 'w', encoding= "utf-8") as file:
        json.dump(data, file)

"""
Actualiza la puntuación de un jugador en un archivo JSON.
Parámetros:
- puntos (int): La cantidad de puntos a añadir.
- nombre (str): El nombre del jugador.
- path (str): La ruta al archivo JSON del jugador. Por defecto, "Recursos\Archivos\Data_jugador.json".
"""
def actualizar_puntuacion(puntos, nombre, path: str =r'Recursos\Archivos\Data_jugador.json'):
    data_jugador = cargar_json(path)
    if data_jugador.get('nombre') == nombre:
        data_jugador['puntuacion'] = data_jugador.get('puntuacion', 0) + puntos
        guardar_json(path, data_jugador)

"""
Registra una letra incorrecta para un jugador en un archivo JSON.
Parámetros:
- letra (str): La letra incorrecta a registrar.
- nombre (str): El nombre del jugador.
- path (str): La ruta al archivo JSON del jugador. Por defecto, "Recursos\Archivos\Data_jugador.json".
"""
def registrar_letra_incorrecta(letra, nombre, path: str =r"Recursos\Archivos\Data_jugador.json"):
    data_jugador = cargar_json(path)
    if data_jugador.get('nombre') == nombre:
        data_jugador['letras_incorrectas'] = data_jugador.get('letras_incorrectas', []) + [letra]
        guardar_json(path, data_jugador)
    

"""
Limpia las letras incorrectas registradas para un jugador en un archivo JSON.
Parámetros:
- path (str): La ruta al archivo JSON del jugador. Por defecto, "Recursos\Archivos\Data_jugador.json".
"""
def limpiar_letras_incorrectas(path: str = r'Recursos\Archivos\Data_jugador.json'):
    data_jugador = cargar_json(path)
    data_jugador['letras_incorrectas'] = []
    guardar_json(path, data_jugador)