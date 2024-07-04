"""
Miembros: Jerónimo Facundo Lucas Córdoba, Sophia Antonella Augusto Valenzuela
---
2° Parcial - Pygame - Ahorcado 
---
Enunciado:
Dada la consigna asignada, deberán desarrollar de a dos el juego. Aplicando los siguientes requerimientos:

Desde lo funcional:
●	Aplicar tipos de datos avanzados: listas, diccionarios, tuplas, sets.
●	Funciones. El código debe estar debidamente modularizado y documentado. Tengan en cuenta los objetivos de la programación 
    con funciones. Realizar módulos.py para la correcta organización de las mismas.
●	Manejo de strings: para normalizar datos, realizar validaciones, funcionamiento inherente a la lógica del juego, etc.
●	Archivos csv y Json. Se deberán utilizar los dos tipos de archivos tanto para persistir datos (puntuacion, premios, etc) como 
    para leer los elementos del juego (rutas de imágenes, preguntas, respuestas, palabras, puntuaciones, etc)
●	Matrices: deberán aplicar por lo menos una matriz dentro de la lógica del juego.
●	Funciones lambda: deberán aplicar por lo menos una función lambda.

Desde lo visual:
●	Imágenes. Según la temática del juego a desarrollar, habrá imágenes estáticas y/o dinámicas 
    (que van cambiando con cada acción del jugador)
●	Texto: toda interacción con el jugador implica que esos mensajes se muestran por la ventana del juego.
●	Figuras:  para representar botones, o cualquier elemento del juego que necesiten.
●	Manejo de eventos: para la interacción con el usuario.

ENTREGA
Deberán crear un repositorio privado en git (compartido con todos los profesores), en el cual subirán:
    a.	El proyecto del juego.
    b.	Markdown con instrucciones, capturas y todo lo que consideren necesario para presentar su juego.

DEFENSA
El día del parcial evaluaremos los grupos en clase. Deberán hacer un gameplay (el programa debe estar preparado ante cualquier fallo. 
Si falla 3 veces o más, el parcial estará desaprobado). Luego evaluaremos su defensa y calificaremos individualmente a 
cada integrante del grupo.
----------------------------------------------------------------------------------------------------------------------------------
Idea del juego:
El juego del ahorcado tiene como tema principal adivinar la palabra relacionada con una materia específica, 
como matemáticas, historia, ciencias, etc. Por ejemplo, se elige de manera al azar una palabra sobre alguna temática en cuestión 
(historia, entretenimiento, deportes, matemáticas, programación, etc)

Funcionamiento del juego:
Selección de palabra: Al comienzo de cada partida, el juego elige aleatoriamente una palabra relacionada con una 
temática aleatoria por ejemplo: 
        Temática: Programación
        _ a _ _ a _ _ _
Palabra: Variable

Adivinanza de letras: El jugador ingresa una letra desde la pantalla (o teclado). Si la letra es parte de la palabra oculta, 
se revela en su posición correcta en la palabra. Si la letra no está en la palabra, se dibuja una parte de la figura del ahorcado.

Puntuación: Por cada letra adivinada correctamente, el jugador ganará +10 puntos y perderá 5 puntos por cada intento fallido. 
Si el jugador gana la partida acumulara el puntaje obtenido en su puntuacion.

Tiempo: El jugador tiene 60 segundos para adivinar cada palabra si se queda sin tiempo pierde.

El jugador si adivina la palabra correctamente antes de que se complete la figura del ahorcado, gana y sigue jugando 
(Se selecciona al azar otra temática y otra palabra) también va a acumular los puntos adicionales basados en el tiempo restante: 
(1 punto por segundo que le sobre), cada vez que se adivina una palabra el tiempo se reinicia.
Si el jugador se queda sin tiempo o agota todos los intentos y la figura del ahorcado se completa pierde.

Comodines:
●	Descubrir una letra: al elegir este comodín el juego descubre una letra al azar. Si existen más incidencias de esa letra 
    no las descubre. 
●	Tiempo extra: al elegir este comodín, se aumentará 30 segundos a la partida actual.
●	Multiplicar tiempo restante: este comodín se podrá elegir al comienzo de la partida (durante los primeros 10 segundos). 
    El mismo duplicará el tiempo restante una vez encontrada la palabra. Si el jugador no la descubre, el comodín queda sin efecto.
"""

import pygame, sys, json
from Funciones import *
from Pantallas import *
from Letritas import *
from Comodines import *
from Imagenes_y_sonido import *

# Inicialización de Pygame
pygame.init()

#posicion de los comodines 
comodin_letra_pos = comodin_letra.get_rect(topleft=(50, 500))
comodin_tiempo_pos = comodin_tiempo_extra.get_rect(topleft=(200, 500))
comodin_multiplicar_pos = comodin_multiplicar_tiempo.get_rect(topleft=(350, 500))

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

    limpiar_letras_incorrectas()
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

    font = pygame.font.SysFont("appleberry", 30)
    clock = pygame.time.Clock()
    tiempo_inicial = pygame.time.get_ticks() #desde que inicializo el programa

    mostrar_texto = lambda texto, pos: screen.blit(font.render(texto, True, (255,255,255)), pos)

    jugando = True
    while jugando:
        screen.fill((255, 255, 255))
        screen.blit(pizarra, (0, 0))
        screen.blit(comodin_letra, comodin_letra_pos)
        screen.blit(comodin_tiempo_extra, comodin_tiempo_pos)
        screen.blit(comodin_multiplicar_tiempo, comodin_multiplicar_pos)
        screen.blit(ahorcado_imagenes[6 - intentos_restantes], (400, 50))
        dibujar_letras(screen, font, letras_ingresadas)

        palabra_mostrada = ' '.join([letra if letra in letras_adivinadas else '_' for letra in palabra])
        mostrar_texto(f"Temática: {tematica}", (50, 50))
        mostrar_texto(palabra_mostrada, (50, 150))
        mostrar_texto(f"Puntuación: {round(puntuacion)}", (50, 250))
        mostrar_texto(f"Tiempo: {round(tiempo_restante)}", (50, 350))
        mostrar_texto(f"Letras Incorrectas: {', '.join(letras_incorrectas)}", (50, 450))
        mostrar_texto(f"Intentos restantes: {intentos_restantes}", (50,600))

        pygame.display.flip()

        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicial)  * 0.001
        tiempo_restante -= tiempo_transcurrido
        tiempo_inicial = tiempo_actual
        if tiempo_restante <= 0:
            print("¡Se acabó el tiempo!")
            mostrar_mensaje_final(screen, pizarra, "¡Se acabo el tiempo!", palabra, ANCHO, ALTO )
            pygame.mixer.Sound.stop(musica_fondo)
            pygame.mixer.Sound.play(musica_perdedor)
            pygame.time.delay(4000)
            break

        for event in pygame.event.get():
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

                elif comodin_letra_pos.collidepoint(pos) and not comodin_letra_usado:
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

        if set(palabra) <= set(letras_adivinadas):
            print("¡Adivinaste la palabra!")
            mostrar_mensaje_final(screen, pizarra, "¡Adivinaste la palabra!", palabra, ANCHO, ALTO)
            puntuacion += int(tiempo_restante)
            actualizar_puntuacion(int(tiempo_restante), nombre_jugador) 
            pygame.mixer.Sound.stop(musica_fondo)
            pygame.mixer.Sound.play(musica_ganador)
            pygame.time.delay(4000)
            
            continuar_jugando = desea_seguir_jugando(screen, pizarra, ANCHO, ALTO)
            if continuar_jugando:
                limpiar_letras_incorrectas()
                tematica, palabra = seleccionar_palabra(tematicas_palabras)
                letras_adivinadas = []
                letras_incorrectas = []
                puntuacion = 0
                tiempo_restante = 60
                letras_ingresadas = set()
                comodin_letra_usado = False
                comodin_tiempo_extra_usado = False
                comodin_multiplicar_tiempo_usado = False
                intentos_restantes = 6
                tiempo_inicial = pygame.time.get_ticks()
            else:
                jugando = False
    
    clock.tick(30)

if __name__ == "__main__":
    main()
