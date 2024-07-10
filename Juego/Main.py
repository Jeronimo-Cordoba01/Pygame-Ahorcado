"""
Miembros: Jerónimo Facundo Lucas Córdoba, Sophia Antonella Augusto Valenzuela
---
2° Parcial - Pygame - Ahorcado 
---
"""

import pygame, sys
from Funciones import *; from Letritas import *;from Pantallas import *; from Comodines import *; 
from Imagenes_y_sonido import *; from Datos_iniciales import *

# Inicialización de Pygame
pygame.init()

# Cargar palabras desde el CSV
tematicas_palabras = leer_palabras(r'Recursos\Archivos\tematicas_palabras.csv')

# Función principal del juego
def main():
    font = pygame.font.SysFont("appleberry", 50)
    pantalla_de_inicio(screen, pizarra, font, ANCHO, ALTO)
    nombre_jugador = pantalla_ingresar_nombre(screen, pizarra, font, ANCHO, ALTO)
    
    data_jugador = {
        "nombre": nombre_jugador,
        "puntuacion": 0,
        "letras_incorrectas": []
    }
    guardar_json(r"Recursos\Archivos\Data_jugador.json", data_jugador)
    estado_juego = inicializar_datos(tematicas_palabras, comodin_letra, comodin_tiempo_extra, comodin_multiplicar_tiempo)

    font = pygame.font.SysFont("appleberry", 30)
    clock = pygame.time.Clock()
    tiempo_inicial = pygame.time.get_ticks() #desde que inicializo el programa
    tiempo_restante = 60 

    jugando = True
    while jugando:
        renderizar_pantalla(screen, pizarra, comodin_letra, comodin_tiempo_extra, comodin_multiplicar_tiempo, ahorcado_imagenes, estado_juego, font)
        mostrar_textos(screen, font, estado_juego, tiempo_restante)
        pygame.display.flip()

        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicial)  * 0.001
        tiempo_restante -= tiempo_transcurrido
        tiempo_inicial = tiempo_actual
        if tiempo_restante <= 0:
            print("¡Se acabó el tiempo!")
            mostrar_mensaje_final(screen, pizarra, "¡Se acabo el tiempo!", estado_juego["palabra"], ANCHO, ALTO, estado_juego["puntuacion"] )
            reproducir_musica(musica_fondo, musica_perdedor)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                letra = pygame.key.name(event.key).lower()
                if letra.isalpha() and letra not in estado_juego["letras_ingresadas"]:
                    estado_juego["letras_ingresadas"].add(letra)
                    if letra in estado_juego["palabra"]:
                        estado_juego["letras_adivinadas"].append(letra)
                        pygame.mixer.Sound.play(sonido_acierto)
                        actualizar_puntuacion(10, nombre_jugador, estado_juego["comodin_multiplicar_tiempo_usado"])
                        estado_juego["puntuacion"] += 10
                    else:
                        estado_juego["letras_incorrectas"].append(letra)
                        pygame.mixer.Sound.play(sonido_falla)
                        actualizar_puntuacion(-5, nombre_jugador, estado_juego["comodin_multiplicar_tiempo_usado"])
                        estado_juego["puntuacion"] -= 5
                        registrar_letra_incorrecta(letra, nombre_jugador)
                        estado_juego["intentos_restantes"] -= 1
                        if estado_juego["intentos_restantes"] == 0:
                            print("No te quedan más intentos, perdiste!")
                            screen.blit(ahorcado_imagenes[6], (400, 50))
                            pygame.display.flip()
                            pygame.time.delay(1000)
                            mostrar_mensaje_final(screen, pizarra, "No te quedan más intentos, perdiste!", estado_juego["palabra"], ANCHO, ALTO, estado_juego["puntuacion"])
                            reproducir_musica(musica_fondo, musica_perdedor)
                            sys.exit()
                            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                letra_clic = letra_click(pos)
                if letra_clic and letra_clic not in estado_juego["letras_ingresadas"]:
                    estado_juego["letras_ingresadas"].add(letra_clic)
                    if letra_clic in estado_juego["palabra"]:
                        estado_juego["letras_adivinadas"].append(letra_clic)
                        pygame.mixer.Sound.play(sonido_acierto)
                        actualizar_puntuacion(10, nombre_jugador, estado_juego["comodin_multiplicar_tiempo_usado"])
                        estado_juego["puntuacion"] += 10
                    else:
                        estado_juego["letras_incorrectas"].append(letra_clic)
                        pygame.mixer.Sound.play(sonido_falla)
                        actualizar_puntuacion(-5, nombre_jugador, estado_juego["comodin_multiplicar_tiempo_usado"])
                        estado_juego["puntuacion"] -= 5
                        registrar_letra_incorrecta(letra_clic, nombre_jugador)
                        estado_juego["intentos_restantes"] -= 1
                        if estado_juego["intentos_restantes"] == 0:
                            print("No te quedan más intentos, perdiste!")
                            screen.blit(ahorcado_imagenes[6], (400, 50))
                            pygame.display.flip()
                            pygame.time.delay(1000)
                            mostrar_mensaje_final(screen, pizarra, "No te quedan más intentos, perdiste!", estado_juego["palabra"], ANCHO, ALTO, estado_juego["puntuacion"])
                            reproducir_musica(musica_fondo, musica_perdedor)
                            return

                tiempo_restante = manejar_comodines(estado_juego, "letra", pos, tiempo_restante, tiempo_transcurrido)
                tiempo_restante = manejar_comodines(estado_juego, "tiempo", pos, tiempo_restante, tiempo_transcurrido)
                tiempo_restante = manejar_comodines(estado_juego, "multiplicar_tiempo", pos, tiempo_restante, tiempo_transcurrido)

        if set(estado_juego["palabra"]) <= set(estado_juego["letras_adivinadas"]):
            print("¡Adivinaste la palabra!")
            estado_juego["puntuacion"] += int(tiempo_restante)
            actualizar_puntuacion(int(tiempo_restante), nombre_jugador, estado_juego["comodin_multiplicar_tiempo_usado"]) 
            mostrar_mensaje_final(screen, pizarra, "¡Adivinaste la palabra!", estado_juego["palabra"], ANCHO, ALTO, estado_juego["puntuacion"])
            reproducir_musica(musica_fondo, musica_ganador)
            
            continuar_jugando = desea_seguir_jugando(screen, pizarra, ANCHO, ALTO)
            if continuar_jugando:
                estado_juego = inicializar_datos(tematicas_palabras, comodin_letra, comodin_tiempo_extra, comodin_multiplicar_tiempo)
                tiempo_restante = 60
                tiempo_inicial = pygame.time.get_ticks()
            else:
                jugando = False
    
    clock.tick(30)

if __name__ == "__main__":
    main()