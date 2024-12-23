import random
from Datos_iniciales import *

# Comodín descubrir letra
def descubrir_letra(palabra, letras_adivinadas):
    """
    Comodín descubrir letra
    Esta función elige aleatoriamente una letra de la palabra que aún no ha sido adivinada.
    Parámetros:
    - palabra (str): La palabra que se está tratando de adivinar.
    - letras_adivinadas (list): Lista de letras que ya han sido adivinadas.
    Retorna:
    - str: Una letra de la palabra que aún no ha sido adivinada.
    - None: Si todas las letras han sido adivinadas.
    """
    letras_disponibles = list(filter(lambda letra: letra not in letras_adivinadas, palabra))
    if letras_disponibles:
        letra = random.choice(letras_disponibles)
        return letra
    return None

# Comodín tiempo extra
def tiempo_extra(tiempo_restante, tiempo_extra=30):
    """
    Comodín tiempo extra
    Esta función añade tiempo extra al tiempo restante.
    Parámetros:
    - tiempo_restante (int): Tiempo restante en segundos.
    - tiempo_extra (int, opcional): Cantidad de tiempo extra a añadir. Valor por defecto es 30 segundos.
    Retorna:
    - int: Tiempo total después de añadir el tiempo extra.
    """
    return tiempo_restante + tiempo_extra

# Comodín multiplicar tiempo
def multi_puntuacion(tiempo_transcurrido, tiempo_restante):
    """
    Comodín multiplicar ountuacion
    Esta función multiplica el tiempo restante si el tiempo transcurrido es menor o igual a 10 segundos.
    Parámetros:
    - tiempo_restante (int): Tiempo restante en segundos.
    - tiempo_transcurrido (int): Tiempo que ha pasado desde el inicio en segundos.
    Retorna:
    - int: Tiempo restante multiplicado por 2 si el tiempo transcurrido es menor o igual a 10 segundos, 
    de lo contrario, retorna el tiempo restante sin cambios.
    """
    if tiempo_transcurrido <= 10:
        return tiempo_restante * 2 
    else:
        return tiempo_restante
    
def manejar_comodines(estado_juego, tipo_comodin, pos, tiempo_restante, tiempo_transcurrido):
    """
    Maneja los comdines del juego

    Parámetros:
    estado_juego: Diccionario con el estado actual del juego.
    tipo_comodin: El tipo de comodín a usar ("letra", "tiempo", "multiplicar_tiempo").
    pos: La posición del clic del ratón.
    tiempo_restante: El tiempo restante del juego.
    tiempo_transcurrido: El tiempo transcurrido del juego.

    Retorna:
    El tiempo restante actualizado después de usar el comodín.
    """
    if tipo_comodin == "letra":
        if estado_juego["comodin_letra_pos"].collidepoint(pos) and not estado_juego["comodin_letra_usado"]:
            letra_descubierta = descubrir_letra(estado_juego["palabra"], estado_juego["letras_adivinadas"])
            if letra_descubierta:
                estado_juego["letras_adivinadas"].append(letra_descubierta)
            estado_juego["comodin_letra_usado"] = True
    elif tipo_comodin == "tiempo":
        if estado_juego["comodin_tiempo_pos"].collidepoint(pos) and not estado_juego["comodin_tiempo_extra_usado"]:
            tiempo_restante = tiempo_extra(tiempo_restante)
            estado_juego["comodin_tiempo_extra_usado"] = True
    elif tipo_comodin == "multiplicar_tiempo":
        if estado_juego["comodin_multiplicar_pos"].collidepoint(pos) and not estado_juego["comodin_multiplicar_tiempo_usado"]:
            # if tiempo_transcurrido <= 10:
            tiempo_restante =  multi_puntuacion(tiempo_transcurrido, tiempo_restante)
            estado_juego["comodin_multiplicar_tiempo_usado"] = True
    
    return tiempo_restante

def actualizar_puntuacion(puntos, nombre, comodin_multiplicar_tiempo_usado, path: str =r'Recursos\\Archivos\Data_jugador.json'):
    """
    Actualiza la puntuación de un jugador en un archivo JSON.
    Parámetros:
    - puntos (int): La cantidad de puntos a añadir.
    - nombre (str): El nombre del jugador.
    - comodin_multiplicar_tiempo_usado(bool): True o False
    - path (str): La ruta al archivo JSON del jugador.

    retorna la puntuacion actualizada del jugador
    """
    data_jugador = cargar_json(path)
    if data_jugador.get('nombre') == nombre:
        if comodin_multiplicar_tiempo_usado:
            puntos *= 2 
        
        data_jugador['puntuacion'] = data_jugador.get('puntuacion', 0) + puntos
        guardar_json(path, data_jugador)
    
    return data_jugador['puntuacion']