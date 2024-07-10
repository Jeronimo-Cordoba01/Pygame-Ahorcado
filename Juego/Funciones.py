import json, random
#from Datos_iniciales import * 

def leer_palabras(path: str = r"Recursos\\Archivos\tematicas_palabras.csv"):
    """
    Lee las palabras desde un archivo CSV y las organiza por temáticas.
    Parámetros:
    - path (str): La ruta al archivo CSV. Por defecto, se asume que está en "Recursos\\Archivos\tematicas_palabras.csv".
    Retorna:
    - dict: Un diccionario donde las claves son las temáticas y los valores son listas de palabras asociadas a cada temática.
    """
    tematicas_palabras = {}
    with open(path, newline='', encoding="utf-8") as csvfile:
        contenido = csvfile.read().splitlines() 
        headers = contenido[0].split(',')
        datos = contenido[1:]
        for row in datos:
            columnas = row.split(',')
            for i, palabra in enumerate(columnas):
                tematica = headers[i]
                palabra = palabra.lower()
                if tematica not in tematicas_palabras:
                    tematicas_palabras[tematica] = []
                tematicas_palabras[tematica].append(palabra)
                
    return tematicas_palabras

def seleccionar_palabra(tematicas_palabras):
    """
    Selecciona una palabra aleatoria de una temática aleatoria.
    Parámetros:
    - tematicas_palabras (dict): Un diccionario con temáticas y sus palabras correspondientes.
    Retorna:
    - tuple: Una tupla con la temática y la palabra seleccionada.
    """
    tematica = random.choice(list(tematicas_palabras.keys()))
    palabra = random.choice(tematicas_palabras[tematica])
    return tematica, palabra

def cargar_json(path: str):
    """
    Carga datos desde un archivo JSON.
    Parámetros:
    - path (str): La ruta al archivo JSON.
    Retorna:
    - dict: Un diccionario con los datos cargados. Si el archivo no existe o hay un error de decodificación, retorna un diccionario vacío.
    """
    try:
        with open(path, 'r', encoding= "utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
    return data

def guardar_json(path: str, data):
    """
    Guarda datos en un archivo JSON.
    Parámetros:
    - path (str): La ruta al archivo JSON.
    - data (dict): El diccionario con los datos a guardar.
    """
    with open(path, 'w', encoding= "utf-8") as file:
        json.dump(data, file)

def registrar_letra_incorrecta(letra, nombre, path: str =r"Recursos\\Archivos\Data_jugador.json"):
    """
    Registra una letra incorrecta para un jugador en un archivo JSON.
    Parámetros:
    - letra (str): La letra incorrecta a registrar.
    - nombre (str): El nombre del jugador.
    - path (str): La ruta al archivo JSON del jugador. ".
    """
    data_jugador = cargar_json(path)
    if data_jugador.get('nombre') == nombre:
        data_jugador['letras_incorrectas'] = data_jugador.get('letras_incorrectas', []) + [letra]
        guardar_json(path, data_jugador)
    
def limpiar_letras_incorrectas(path: str = r'Recursos\\Archivos\Data_jugador.json'):
    """
    Limpia las letras incorrectas registradas para un jugador en un archivo JSON.
    Parámetros:
    - path (str): La ruta al archivo JSON del jugador. .
    """
    data_jugador = cargar_json(path)
    data_jugador['letras_incorrectas'] = []
    guardar_json(path, data_jugador)