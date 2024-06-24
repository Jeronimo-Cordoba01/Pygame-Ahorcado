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
●	Archivos csv y Json. Se deberán utilizar los dos tipos de archivos tanto para persistir datos (score, premios, etc) como 
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
Si el jugador gana la partida acumulara el puntaje obtenido en su score.

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

import pygame, sys, os
from Funciones import *

SIZE = (1100, 800)
FPS = 30
BLANCO = (255, 255, 255)

pygame.init()

PANTALLA = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Nuestro primer jueguito")

fondo = pygame.image.load(r"Pygame-Ahorcado/Recursos/Imagenes/Pizzaron.png")
fondo = pygame.transform.scale(fondo, SIZE)

icono = pygame.image.load(r"Pygame-Ahorcado/Recursos/Imagenes/Icono.jpg")
pygame.display.set_icon(icono)

pygame.mixer.music.load(r"Pygame-Ahorcado/Recursos/Audio/Musica-de-fondo.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

def cargar_sonidos():
    sonidos = {
        "falla": pygame.mixer.Sound(os.path.join("Pygame-Ahorcado/Recursos/Audio", "Falla-letra.mp3")),
        "correcta": pygame.mixer.Sound(os.path.join("Pygame-Ahorcado/Recursos/Audio", "Letra-correcta.mp3")),
        "fondo": pygame.mixer.Sound(os.path.join("Pygame-Ahorcado/Recursos/Audio", "Musica-de-fondo.mp3")),
    }
    return sonidos

sonidos = cargar_sonidos()

PANTALLA.blit(fondo, (0, 0))

horca = Horca(PANTALLA) 
palabra = Palabra()

puntuacion = Puntuacion()

Jugando = True
clock = pygame.time.Clock()

while Jugando:
    PANTALLA.blit(fondo, (0, 0))
    horca.dibujar()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Jugando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Jugando = False
            elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                letra = chr(event.key)
                if palabra.validar_letra(letra):
                    sonidos["correcta"].play()
                    if palabra.palabra_completa():
                        puntuacion.aumentar(10)
                        palabra.palabra_aleatoria()
                else:
                    sonidos["falla"].play()
                    horca.actualizar()
                    if horca.partes >= 6:
                        puntuacion.disminuir(5)
                        palabra.palabra_aleatoria()
                        horca.partes = 0

    palabra_mostrada, letras_incorrectas_mostradas = palabra.obtener_palabra_mostrada()
    
    font = pygame.font.SysFont(None, 55)
    texto_puntuacion = font.render(f'Puntuación: {puntuacion.puntuacion}', True, BLANCO)
    texto_palabra = font.render(f'Palabra: {palabra_mostrada}', True, BLANCO)
    texto_letras_incorrectas = font.render(f'Letras incorrectas: {letras_incorrectas_mostradas}', True, BLANCO)
    
    PANTALLA.blit(texto_puntuacion, (50, 50))
    PANTALLA.blit(texto_palabra, (50, 150))
    PANTALLA.blit(texto_letras_incorrectas, (50, 250))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
