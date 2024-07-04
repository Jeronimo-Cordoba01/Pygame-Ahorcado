import pygame,sys
from Funciones import actualizar_puntuacion, registrar_letra_incorrecta, letra_click, mostrar_mensaje_final

def manejar_eventos(eventos, letras_ingresadas, letras_adivinadas, palabra, puntuacion, nombre_jugador, letras_incorrectas, intentos_restantes, screen, ahorcado_imagenes, pizarra, musica_fondo, sonido_acierto, sonido_falla, musica_perdedor, ANCHO, ALTO):
    for event in eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            letra = pygame.key.name(event.key).lower()
            if letra.isalpha() and letra not in letras_ingresadas:
                letras_ingresadas.add(letra)
                if letra in palabra:
                    letras_adivinadas.append(letra)
                    pygame.mixer.Sound.play(sonido_acierto)
                    actualizar_puntuacion(10, nombre_jugador)
                    puntuacion += 10
                else:
                    letras_incorrectas.append(letra)
                    pygame.mixer.Sound.play(sonido_falla)
                    actualizar_puntuacion(-5, nombre_jugador)
                    puntuacion -= 5
                    registrar_letra_incorrecta(letra, nombre_jugador)
                    intentos_restantes -= 1
                    if intentos_restantes == 0:
                        print("No te quedan mas intentos, perdiste!")
                        screen.blit(ahorcado_imagenes[6], (400, 50))
                        pygame.display.flip()
                        pygame.time.delay(1000)
                        pygame.mixer.Sound.stop(musica_fondo)
                        pygame.mixer.Sound.play(musica_perdedor)
                        mostrar_mensaje_final(screen, pizarra, "No te quedan mas intentos, perdiste!", palabra, ANCHO, ALTO)
                        pygame.time.delay(4000)
                        sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            letra_clic = letra_click(pos)
            if letra_clic and letra_clic not in letras_ingresadas:
                letras_ingresadas.add(letra_clic)
                if letra_clic in palabra:
                    letras_adivinadas.append(letra_clic)
                    pygame.mixer.Sound.play(sonido_acierto)
                    actualizar_puntuacion(10, nombre_jugador)
                    puntuacion += 10
                else:
                    letras_incorrectas.append(letra_clic)
                    pygame.mixer.Sound.play(sonido_falla)
                    actualizar_puntuacion(-5, nombre_jugador)
                    puntuacion -= 5
                    registrar_letra_incorrecta(letra_clic, nombre_jugador)
                    intentos_restantes -= 1
                    if intentos_restantes == 0:
                        print("No te quedan mas intentos, perdiste!")
                        screen.blit(ahorcado_imagenes[6], (400, 50))
                        pygame.display.flip()
                        pygame.time.delay(1000)
                        pygame.mixer.Sound.stop(musica_fondo)
                        pygame.mixer.Sound.play(musica_perdedor)
                        mostrar_mensaje_final(screen, pizarra, "No te quedan mas intentos, perdiste!", palabra, ANCHO, ALTO)
                        pygame.time.delay(4000)
                        return
