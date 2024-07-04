from Comodines import *

def usar_comodines(pos, comodin_letra_pos, comodin_letra_usado, palabra, letras_adivinadas, comodin_tiempo_pos, comodin_tiempo_extra_usado, tiempo_restante, tiempo_extra, comodin_multiplicar_pos, comodin_multiplicar_tiempo_usado, tiempo_transcurrido, multi_tiempo):
    if comodin_letra_pos.collidepoint(pos) and not comodin_letra_usado:
        letra_descubierta = descubrir_letra(palabra, letras_adivinadas)
        if letra_descubierta:
            letras_adivinadas.append(letra_descubierta)
        comodin_letra_usado = True
    elif comodin_tiempo_pos.collidepoint(pos) and not comodin_tiempo_extra_usado:
        tiempo_restante = tiempo_extra(tiempo_restante)
        comodin_tiempo_extra_usado = True
    elif comodin_multiplicar_pos.collidepoint(pos) and not comodin_multiplicar_tiempo_usado:
        if tiempo_transcurrido <= 10:
            tiempo_restante = multi_tiempo(tiempo_restante, tiempo_transcurrido)
            comodin_multiplicar_tiempo_usado = True
    return all
