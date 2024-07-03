import random

# Comodín descubrir letra
def descubrir_letra(palabra, letras_adivinadas):
    letras_disponibles = list(filter(lambda letra: letra not in letras_adivinadas, palabra))
    if letras_disponibles:
        letra = random.choice(letras_disponibles)
        return letra
    return None

# Comodín tiempo extra
def tiempo_extra(tiempo_restante, tiempo_extra=30):
    return tiempo_restante + tiempo_extra

# Comodín multiplicar tiempo
def multi_tiempo(tiempo_restante, tiempo_transcurrido):
    if tiempo_transcurrido <= 10:
        return tiempo_restante * 2
    return tiempo_restante
