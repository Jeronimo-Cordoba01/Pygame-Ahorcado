from Funciones import *

def inicializar_datos(tematicas_palabras, comodin_letra, comodin_tiempo_extra, comodin_multiplicar_tiempo):
    """
    Inicializa el estado del juego con los datos necesarios.

    Parámetros:
    tematicas_palabras: Diccionario que contiene las temáticas y sus respectivas palabras.
    comodin_letra: Objeto de imagen del comodín de letra.
    comodin_tiempo_extra: Objeto de imagen del comodín de tiempo extra.
    comodin_multiplicar_tiempo: Objeto de imagen del comodín de multiplicar tiempo.

    Retorna:
    Un diccionario con el estado inicial del juego.
    """
    estado_juego = {}

    limpiar_letras_incorrectas()
    estado_juego["tematica"], estado_juego["palabra"] = seleccionar_palabra(tematicas_palabras)
    estado_juego["letras_adivinadas"] = []
    estado_juego["data_jugador"] = cargar_json(r"Recursos/Archivos/Data_jugador.json")
    estado_juego["letras_incorrectas"] = estado_juego["data_jugador"].get('letras_incorrectas', [])
    estado_juego["puntuacion"] = estado_juego["data_jugador"].get('puntuacion', 0)
    estado_juego["letras_ingresadas"] = set()
    estado_juego["comodin_letra_usado"] = False
    estado_juego["comodin_tiempo_extra_usado"] = False
    estado_juego["comodin_multiplicar_tiempo_usado"] = False
    estado_juego["intentos_restantes"] = 6

    #defino la pocision de los comodines 
    estado_juego["comodin_letra_pos"] = comodin_letra.get_rect(topleft=(50, 500))
    estado_juego["comodin_tiempo_pos"] = comodin_tiempo_extra.get_rect(topleft=(200, 500))
    estado_juego["comodin_multiplicar_pos"] = comodin_multiplicar_tiempo.get_rect(topleft=(350, 500))

    return estado_juego
