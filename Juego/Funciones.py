import csv
import json
import random

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

def seleccionar_palabra(tematicas_palabras):
    tematica = random.choice(list(tematicas_palabras.keys()))
    palabra = random.choice(tematicas_palabras[tematica])
    return tematica, palabra

def cargar_json(path: str):
    try:
        with open(path, 'r', encoding= "utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
    return data

def guardar_json(path: str, data):
    with open(path, 'w', encoding= "utf-8") as file:
        json.dump(data, file)

def actualizar_puntuacion(puntos, path: str =r'Recursos\Archivos\Letras_incorrectas.json'):
    puntuacion = cargar_json(path)
    puntuacion['score'] = puntuacion.get('score', 0) + puntos
    guardar_json(path, puntuacion)

def registrar_letra_incorrecta(letra, path: str =r'Recursos\Archivos\Puntuacion.json'):
    letras_incorrectas = cargar_json(path)
    letras_incorrectas['letras'] = letras_incorrectas.get('letras', []) + [letra]
    guardar_json(path, letras_incorrectas)

#comodin
def descubrir_letra(palabra, letras_adivinadas):
    letras_disponibles = [letra for letra in palabra if letra not in letras_adivinadas]
    if letras_disponibles:
        letra = random.choice(letras_disponibles)
        return letra
    return None