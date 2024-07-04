import pygame
from Funciones import actualizar_puntuacion, seleccionar_palabra, limpiar_letras_incorrectas, mostrar_mensaje_final, desea_seguir_jugando

def finalizar_juego(screen, pizarra, palabra, letras_adivinadas, puntuacion, tiempo_restante, nombre_jugador, musica_fondo, musica_ganador, tematicas_palabras, ANCHO, ALTO):
    if set(palabra) <= set(letras_adivinadas):
        print("¡Adivinaste la palabra!")
        mostrar_mensaje_final(screen, pizarra, "¡Adivinaste la palabra!", palabra, ANCHO, ALTO)
        puntuacion += int(tiempo_restante)
        actualizar_puntuacion(int(tiempo_restante), nombre_jugador) 
        pygame.mixer.Sound.stop(musica_fondo)
        pygame.mixer.Sound.play(musica_ganador)
        pygame.time.delay(4000)
        
        continuar_jugando = desea_seguir_jugando(screen, pizarra, ANCHO, ALTO)

