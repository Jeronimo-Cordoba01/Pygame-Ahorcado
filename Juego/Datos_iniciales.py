from Funciones import *

def inicializar_datos():
    limpiar_letras_incorrectas()
    tematicas_palabras = leer_palabras(r'Recursos\Archivos\tematicas_palabras.csv')
    tematica, palabra = seleccionar_palabra(tematicas_palabras)
    letras_adivinadas = []
    data_jugador = cargar_json(r"Recursos\Archivos\Data_jugador.json")
    letras_incorrectas = data_jugador.get('letras_incorrectas', [])
    puntuacion = data_jugador.get('puntuacion', 0)
    tiempo_restante = 60
    letras_ingresadas = set()
    comodin_letra_usado = False
    comodin_tiempo_extra_usado = False
    comodin_multiplicar_tiempo_usado = False 
    intentos_restantes = 6 
    
    return (tematica, palabra, letras_adivinadas, letras_incorrectas, puntuacion, tiempo_restante,
            letras_ingresadas, comodin_letra_usado, comodin_tiempo_extra_usado, comodin_multiplicar_tiempo_usado, 
            intentos_restantes)
