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

import pygame, sys, json
from Funciones import *

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
ANCHO = 1000
ALTO = 800
DIMENSIONES = (ANCHO, ALTO)
screen = pygame.display.set_mode(DIMENSIONES)
pygame.display.set_caption("Ahorcado")

# Cargar imágenes
icono = pygame.image.load(r"Recursos\Imagenes\Icono.jpg")
pygame.display.set_icon(icono)
horca = pygame.image.load(r'Recursos\Imagenes\Horca\Horca.png')
horca = pygame.transform.scale(horca, (200,200))
soga = pygame.image.load(r'Recursos\Imagenes\Horca\Soga.png')
soga = pygame.transform.scale(soga, (350,350))
soga_pos = soga.get_rect(topright=(500,500))
pizarra = pygame.image.load(r'Recursos\Imagenes\Pizzaron.png')
pizarra = pygame.transform.scale(pizarra, DIMENSIONES)
comodin_letra = pygame.image.load(r"Recursos\Imagenes\Comodines\descubrir_letra.jpg")
comodin_letra = pygame.transform.scale(comodin_letra, (100,100))
comodin_tiempo_extra = pygame.image.load(r"Recursos\Imagenes\Comodines\tiempo_extra.jpg")
comodin_tiempo_extra = pygame.transform.scale(comodin_tiempo_extra, (100,100))
comodin_multiplicar_tiempo = pygame.image.load(r"Recursos\Imagenes\Comodines\multiplicar_tiempo.jpg")
comodin_multiplicar_tiempo = pygame.transform.scale(comodin_multiplicar_tiempo, (100,100))

#posicion de los comodines 
comodin_letra_pos = comodin_letra.get_rect(topleft=(50, 500))
comodin_tiempo_pos = comodin_tiempo_extra.get_rect(topleft=(200, 500))
comodin_multiplicar_pos = comodin_multiplicar_tiempo.get_rect(topleft=(350, 500))

# Cargar sonidos
sonido_falla = pygame.mixer.Sound(r'Recursos\Audio\Falla-letra.mp3')
sonido_acierto = pygame.mixer.Sound(r'Recursos\Audio\Letra-correcta.mp3')
musica_fondo = pygame.mixer.Sound(r'Recursos\Audio\Musica-de-fondo.mp3')
musica_ganador = pygame.mixer.Sound(r'Recursos\Audio\Happy-wheels.mp3')

# Reproducir música de fondo
pygame.mixer.Sound.play(musica_fondo, loops=-1)

# Cargar palabras desde el CSV
tematicas_palabras = leer_palabras(r'Recursos\Archivos\tematicas_palabras.csv')
puntuacion_inicial = {"score": 0}
guardar_puntuacion = guardar_json(r"Recursos\Archivos\Puntuacion.json", puntuacion_inicial)

# Función principal del juego
def main():
    tematica, palabra = seleccionar_palabra(tematicas_palabras)
    letras_adivinadas = []
    letras_incorrectas = cargar_json(r'Recursos\Archivos\Letras_incorrectas.json').get('letras', [])
    puntuacion = cargar_json(r"Recursos\Archivos\Puntuacion.json").get('score', 0)
    tiempo_restante = 60
    letras_ingresadas = set()
    #usar_comodin = False
    comodin_letra_usado = False
    comodin_tiempo_extra_usado = False
    comodin_multiplicar_tiempo_usado = False 

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    tiempo_inicial = pygame.time.get_ticks() #desde que inicializo el programa

    def mostrar_texto(texto, pos):
        text = font.render(texto, True, (0, 0, 0))
        screen.blit(text, pos)
        
    def pantalla_inicio(screen, font):
        screen.blint(r"Recursos\Imagenes\Pizzaron.png", (0, 0))
        text_surface = font.render("Introduce tu nombre:", True, (0, 0, 0))
        screen.blit(text_surface, (300, 300))
        
        ingreso_nombre = pygame.Rect(300, 350, 140, 32)
        pygame.draw.rect(screen, (255, 255, 255), ingreso_nombre)
        
        boton_rect = pygame.Rect(300, 400, 140, 32)
        pygame.draw.rect(screen, (255, 255, 255), boton_rect)
        text_surface = font.render("Jugar", True, (0, 0, 0))
        screen.blit(text_surface, (boton_rect.x + 10, boton_rect.y + 10))
        
        return ingreso_nombre, boton_rect

    while True:
        screen.fill((255, 255, 255))
        screen.blit(pizarra, (0, 0))
        screen.blit(horca, (150, 100))
        screen.blit(soga, (150, 100))
        screen.blit(comodin_letra, comodin_letra_pos)
        screen.blit(comodin_tiempo_extra, comodin_tiempo_pos)
        screen.blit(comodin_multiplicar_tiempo, comodin_multiplicar_pos)

        palabra_mostrada = ' '.join([letra if letra in letras_adivinadas else '_' for letra in palabra])
        mostrar_texto(f"Temática: {tematica}", (50, 50))
        mostrar_texto(palabra_mostrada, (50, 150))
        mostrar_texto(f"Puntuación: {puntuacion}", (50, 250))
        mostrar_texto(f"Tiempo: {tiempo_restante}", (50, 350))
        mostrar_texto(f"Letras Incorrectas: {', '.join(letras_incorrectas)}", (50, 450))

        pygame.display.flip()

        tiempo_actual = pygame.time.get_ticks() 
        tiempo_transcurrido = (tiempo_actual - tiempo_inicial) * 0.001
        tiempo_restante = 60 - int(tiempo_transcurrido)
        if tiempo_restante == 0:
            print("¡Se acabó el tiempo!")
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
                        actualizar_puntuacion(10)
                        puntuacion += 10
                    else:
                        letras_incorrectas.append(letra)
                        pygame.mixer.Sound.play(sonido_falla)
                        actualizar_puntuacion(-5)
                        puntuacion -= 5
                        registrar_letra_incorrecta(letra)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if comodin_letra_pos.collidepoint(pos) and comodin_letra_usado == False:
                    letra_descubierta = descubrir_letra(palabra, letras_adivinadas)
                    if letra_descubierta:
                        letras_adivinadas.append(letra_descubierta)
                    comodin_letra_usado = True
                elif comodin_tiempo_pos.collidepoint(pos) and not comodin_tiempo_extra_usado:
                    tiempo_restante = tiempo_extra(tiempo_restante)
                    comodin_tiempo_extra_usado = True
                elif comodin_multiplicar_pos.collidepoint(pos) and comodin_multiplicar_tiempo_usado == False and tiempo_transcurrido <= 10:
                    tiempo_restante *= 2
                    comodin_multiplicar_tiempo_usado = True

        if set(palabra) <= set(letras_adivinadas):
            mostrar_texto("¡Adivinaste la palabra!", (ANCHO // 2 - 100, ALTO // 2))
            mostrar_texto(f"La palabra era: {palabra}", (ANCHO // 2 - 100, ALTO // 2 + 50))
            pygame.display.flip()
            pygame.time.delay(3000)
            actualizar_puntuacion(tiempo_restante)
            pygame.mixer.Sound.play(musica_ganador)
            break

        clock.tick(60)

# Ejecutar juego
if __name__ == "__main__":
    main()