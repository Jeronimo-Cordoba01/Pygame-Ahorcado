import random

# Comodín descubrir letra
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
def descubrir_letra(palabra, letras_adivinadas):
    letras_disponibles = list(filter(lambda letra: letra not in letras_adivinadas, palabra))
    if letras_disponibles:
        letra = random.choice(letras_disponibles)
        return letra
    return None

# Comodín tiempo extra
"""
Comodín tiempo extra
Esta función añade tiempo extra al tiempo restante.
Parámetros:
- tiempo_restante (int): Tiempo restante en segundos.
- tiempo_extra (int, opcional): Cantidad de tiempo extra a añadir. Valor por defecto es 30 segundos.
Retorna:
- int: Tiempo total después de añadir el tiempo extra.
"""
def tiempo_extra(tiempo_restante, tiempo_extra=30):
    return tiempo_restante + tiempo_extra

# Comodín multiplicar tiempo
"""
Comodín multiplicar tiempo
Esta función multiplica el tiempo restante si el tiempo transcurrido es menor o igual a 10 segundos.
Parámetros:
- tiempo_restante (int): Tiempo restante en segundos.
- tiempo_transcurrido (int): Tiempo que ha pasado desde el inicio en segundos.
Retorna:
- int: Tiempo restante multiplicado por 2 si el tiempo transcurrido es menor o igual a 10 segundos, 
  de lo contrario, retorna el tiempo restante sin cambios.
"""
def multi_tiempo(tiempo_restante, tiempo_transcurrido):
    if tiempo_transcurrido <= 10:
        return tiempo_restante * 2
    return tiempo_restante