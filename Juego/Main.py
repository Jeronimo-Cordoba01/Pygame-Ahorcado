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
    """
    Función principal del juego
    Inicializa el juego y gestiona el bucle principal del mismo.
    """
    font = pygame.font.SysFont("appleberry", 50)
    pantalla_de_inicio(screen, pizarra, font, ANCHO, ALTO)
    nombre_jugador = pantalla_ingresar_nombre(screen, pizarra, font, ANCHO, ALTO)
    
    data_jugador = {
        "nombre": nombre_jugador,
        "puntuacion": 0,
        "letras_incorrectas": []
    }
    guardar_json(r"Recursos\Archivos\Data_jugador.json", data_jugador)
    """
    Cargar el archivo JSON con los datos del jugador y actualizarlo con los datos del nuevo jugador.
    """

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
    """
    Reiniciar los estados del juego para una nueva partida:
    - limpiar_letras_incorrectas(): Limpia las letras incorrectas registradas del jugador.
    - tematica, palabra = seleccionar_palabra(tematicas_palabras): Selecciona una nueva palabra y su temática.
    - letras_adivinadas = []: Reinicia la lista de letras adivinadas.
    - data_jugador = cargar_json(r"Recursos\\Archivos\\Data_jugador.json"): Carga los datos del jugador desde el archivo JSON.
    - letras_incorrectas = data_jugador.get('letras_incorrectas', []): Obtiene la lista de letras incorrectas del jugador.
    - puntuacion = data_jugador.get('puntuacion', 0): Obtiene la puntuación del jugador.
    - tiempo_restante = 60: Reinicia el tiempo restante a 60 segundos.
    - letras_ingresadas = set(): Reinicia el conjunto de letras ingresadas.
    - comodin_letra_usado = False: Reinicia el estado del comodín "descubrir letra".
    - comodin_tiempo_extra_usado = False: Reinicia el estado del comodín "tiempo extra".
    - comodin_multiplicar_tiempo_usado = False: Reinicia el estado del comodín "multiplicar tiempo".
    - intentos_restantes = 6: Reinicia el número de intentos restantes.
    """

    font = pygame.font.SysFont("appleberry", 30)
    clock = pygame.time.Clock()
    tiempo_inicial = pygame.time.get_ticks() #desde que inicializo el programa
    """
    Configuraciones iniciales para la partida:
    - font = pygame.font.SysFont("appleberry", 30): Establece la fuente y el tamaño del texto para el juego.
    - clock = pygame.time.Clock(): Inicializa el reloj para controlar la velocidad de actualización del juego.
    - tiempo_inicial = pygame.time.get_ticks(): Registra el tiempo inicial en milisegundos desde que Pygame fue inicializado.
    """

    mostrar_texto = lambda texto, pos: screen.blit(font.render(texto, True, (255,255,255)), pos)
    """
    Definición de una función lambda para mostrar texto en la pantalla:
    - mostrar_texto = lambda texto, pos: screen.blit(font.render(texto, True, (255, 255, 255)), pos):
    Esta función lambda toma un texto y una posición como parámetros, y dibuja el texto en la pantalla en la posición especificada.
    Utiliza la fuente definida anteriormente y establece el color del texto en blanco (RGB: 255, 255, 255).
    """

    jugando = True
    while jugando:
        screen.fill((255, 255, 255))
        screen.blit(pizarra, (0, 0))
        screen.blit(comodin_letra, comodin_letra_pos)
        screen.blit(comodin_tiempo_extra, comodin_tiempo_pos)
        screen.blit(comodin_multiplicar_tiempo, comodin_multiplicar_pos)
        screen.blit(ahorcado_imagenes[6 - intentos_restantes], (400, 50))
        dibujar_letras(screen, font, letras_ingresadas)
        """
        Bucle principal del juego:
        - jugando = True: Inicializa el estado del juego como activo.
        - while jugando:: Bucle que continúa ejecutándose mientras el estado del juego sea activo.
        - screen.fill((255, 255, 255)): Llena la pantalla con un color blanco.
        - screen.blit(pizarra, (0, 0)): Dibuja la imagen de fondo en la pantalla.
        - screen.blit(comodin_letra, comodin_letra_pos): Dibuja el ícono del comodín "descubrir letra" en su posición.
        - screen.blit(comodin_tiempo_extra, comodin_tiempo_pos): Dibuja el ícono del comodín "tiempo extra" en su posición.
        - screen.blit(comodin_multiplicar_tiempo, comodin_multiplicar_pos): Dibuja el ícono del comodín "multiplicar tiempo" en su posición.
        - screen.blit(ahorcado_imagenes[6 - intentos_restantes], (400, 50)): Dibuja la imagen correspondiente al estado actual del ahorcado.
        - dibujar_letras(screen, font, letras_ingresadas): Dibuja las letras del abecedario en la pantalla, excluyendo las letras ya ingresadas.
        """

        palabra_mostrada = ' '.join([letra if letra in letras_adivinadas else '_' for letra in palabra])
        mostrar_texto(f"Temática: {tematica}", (50, 50))
        mostrar_texto(palabra_mostrada, (50, 150))
        mostrar_texto(f"Puntuación: {round(puntuacion)}", (50, 250))
        mostrar_texto(f"Tiempo: {round(tiempo_restante)}", (50, 350))
        mostrar_texto(f"Letras Incorrectas: {', '.join(letras_incorrectas)}", (50, 450))
        mostrar_texto(f"Intentos restantes: {intentos_restantes}", (50,600))

        pygame.display.flip()
        
        """
        Actualizar la pantalla con la información del juego:
        - palabra_mostrada = ' '.join([letra if letra in letras_adivinadas else '_' for letra in palabra]):
        Crea una cadena que muestra la palabra con las letras adivinadas y guiones bajos para las letras no adivinadas.
        - mostrar_texto(f"Temática: {tematica}", (50, 50)):
        Muestra la temática de la palabra en la posición (50, 50).
        - mostrar_texto(palabra_mostrada, (50, 150)):
        Muestra la palabra con las letras adivinadas en la posición (50, 150).
        - mostrar_texto(f"Puntuación: {puntuacion}", (50, 250)):
        Muestra la puntuación actual del jugador en la posición (50, 250).
        - mostrar_texto(f"Tiempo: {round(tiempo_restante)}", (50, 350)):
        Muestra el tiempo restante en la posición (50, 350).
        - mostrar_texto(f"Letras Incorrectas: {', '.join(letras_incorrectas)}", (50, 450)):
        Muestra las letras incorrectas ingresadas por el jugador en la posición (50, 450).
        - mostrar_texto(f"Intentos restantes: {intentos_restantes}", (50, 600)):
        Muestra el número de intentos restantes en la posición (50, 600).
        - pygame.display.flip():
        Actualiza toda la pantalla para que los cambios se vean reflejados.
        """

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
        """
        Gestión del tiempo en el juego:
        - tiempo_actual = pygame.time.get_ticks():
        Obtiene el tiempo actual en milisegundos desde que Pygame fue inicializado.
        - tiempo_transcurrido = (tiempo_actual - tiempo_inicial) * 0.001:
        Calcula el tiempo transcurrido desde la última actualización en segundos.
        - tiempo_restante -= tiempo_transcurrido:
        Resta el tiempo transcurrido del tiempo restante.
        - tiempo_inicial = tiempo_actual:
        Actualiza el tiempo inicial para la próxima iteración.
        - if tiempo_restante <= 0:
        Verifica si el tiempo restante se ha agotado.
        - print("¡Se acabó el tiempo!"):
            Imprime un mensaje en la consola indicando que el tiempo se ha agotado.
        - mostrar_mensaje_final(screen, pizarra, "¡Se acabo el tiempo!", palabra, ANCHO, ALTO):
            Muestra un mensaje final indicando que se ha acabado el tiempo.
        - pygame.mixer.Sound.stop(musica_fondo):
            Detiene la música de fondo.
        - pygame.mixer.Sound.play(musica_perdedor):
            Reproduce el sonido de perdedor.
        - pygame.time.delay(4000):
            Espera 4 segundos antes de continuar.
        - break:
            Sale del bucle del juego.
        """

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
                            """
                            Gestión de eventos del juego:
                            - for event in pygame.event.get():
                            Itera sobre la lista de eventos en la cola de eventos.
                            - if event.type == pygame.QUIT:
                                Verifica si el evento es de tipo QUIT (cerrar la ventana).
                                - pygame.quit():
                                Finaliza todos los módulos de Pygame.
                                - sys.exit():
                                Sale del programa.
                            - elif event.type == pygame.KEYDOWN:
                                Verifica si se ha presionado una tecla.
                                - letra = pygame.key.name(event.key).lower():
                                Obtiene el nombre de la tecla presionada y lo convierte a minúsculas.
                                - if letra.isalpha() and letra not in letras_ingresadas:
                                Verifica si la tecla presionada es una letra y si no ha sido ingresada antes.
                                - letras_ingresadas.add(letra):
                                    Añade la letra a la lista de letras ingresadas.
                                - if letra in palabra:
                                    Verifica si la letra está en la palabra.
                                    - letras_adivinadas.append(letra):
                                    Añade la letra a la lista de letras adivinadas.
                                    - pygame.mixer.Sound.play(sonido_acierto):
                                    Reproduce el sonido de acierto.
                                    - actualizar_puntuacion(10, nombre_jugador):
                                    Actualiza la puntuación del jugador añadiendo 10 puntos.
                                    - puntuacion += 10:
                                    Incrementa la puntuación en 10 puntos.
                                - else:
                                    Si la letra no está en la palabra.
                                    - letras_incorrectas.append(letra):
                                    Añade la letra a la lista de letras incorrectas.
                                    - pygame.mixer.Sound.play(sonido_falla):
                                    Reproduce el sonido de fallo.
                                    - actualizar_puntuacion(-5, nombre_jugador):
                                    Actualiza la puntuación del jugador restando 5 puntos.
                                    - puntuacion -= 5:
                                    Decrementa la puntuación en 5 puntos.
                                    - registrar_letra_incorrecta(letra, nombre_jugador):
                                    Registra la letra incorrecta en los datos del jugador.
                                    - intentos_restantes -= 1:
                                    Decrementa el número de intentos restantes.
                                    - if intentos_restantes == 0:
                                    Verifica si no quedan más intentos.
                                    - print("No te quedan mas intentos, perdiste!"):
                                        Imprime un mensaje en la consola indicando que se han agotado los intentos.
                                    - screen.blit(ahorcado_imagenes[6], (400, 50)):
                                        Dibuja la imagen completa del ahorcado.
                                    - pygame.display.flip():
                                        Actualiza toda la pantalla para que los cambios se vean reflejados.
                                    - pygame.time.delay(1000):
                                        Espera 1 segundo antes de continuar.
                                    - pygame.mixer.Sound.stop(musica_fondo):
                                        Detiene la música de fondo.
                                    - pygame.mixer.Sound.play(musica_perdedor):
                                        Reproduce el sonido de perdedor.
                                    - mostrar_mensaje_final(screen, pizarra, "No te quedan mas intentos, perdiste!", palabra, ANCHO, ALTO):
                                        Muestra un mensaje final indicando que se han agotado los intentos.
                                    - pygame.time.delay(4000):
                                        Espera 4 segundos antes de continuar.
                                    - break:
                                        Sale del bucle del juego.
                            """

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
                            """
                            Gestión del evento de clic del mouse:
                            - elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            Verifica si se ha presionado el botón izquierdo del mouse.
                            - pos = pygame.mouse.get_pos():
                                Obtiene la posición actual del mouse.
                            - letra_clic = letra_click(pos):
                                Determina si la posición del clic coincide con alguna letra y la retorna.
                            - if letra_clic and letra_clic not in letras_ingresadas:
                                Verifica si la letra clickeada es válida y no ha sido ingresada antes.
                                - letras_ingresadas.add(letra_clic):
                                Añade la letra clickeada a la lista de letras ingresadas.
                                - if letra_clic in palabra:
                                Verifica si la letra clickeada está en la palabra.
                                - letras_adivinadas.append(letra_clic):
                                    Añade la letra clickeada a la lista de letras adivinadas.
                                - pygame.mixer.Sound.play(sonido_acierto):
                                    Reproduce el sonido de acierto.
                                - actualizar_puntuacion(10, nombre_jugador):
                                    Actualiza la puntuación del jugador añadiendo 10 puntos.
                                - puntuacion += 10:
                                    Incrementa la puntuación en 10 puntos.
                                - else:
                                Si la letra clickeada no está en la palabra.
                                - letras_incorrectas.append(letra_clic):
                                    Añade la letra clickeada a la lista de letras incorrectas.
                                - pygame.mixer.Sound.play(sonido_falla):
                                    Reproduce el sonido de fallo.
                                - actualizar_puntuacion(-5, nombre_jugador):
                                    Actualiza la puntuación del jugador restando 5 puntos.
                                - puntuacion -= 5:
                                    Decrementa la puntuación en 5 puntos.
                                - registrar_letra_incorrecta(letra_clic, nombre_jugador):
                                    Registra la letra incorrecta en los datos del jugador.
                                - intentos_restantes -= 1:
                                    Decrementa el número de intentos restantes.
                                - if intentos_restantes == 0:
                                    Verifica si no quedan más intentos.
                                    - print("No te quedan mas intentos, perdiste!"):
                                    Imprime un mensaje en la consola indicando que se han agotado los intentos.
                                    - screen.blit(ahorcado_imagenes[6], (400, 50)):
                                    Dibuja la imagen completa del ahorcado.
                                    - pygame.display.flip():
                                    Actualiza toda la pantalla para que los cambios se vean reflejados.
                                    - pygame.time.delay(1000):
                                    Espera 1 segundo antes de continuar.
                                    - pygame.mixer.Sound.stop(musica_fondo):
                                    Detiene la música de fondo.
                                    - pygame.mixer.Sound.play(musica_perdedor):
                                    Reproduce el sonido de perdedor.
                                    - mostrar_mensaje_final(screen, pizarra, "No te quedan mas intentos, perdiste!", palabra, ANCHO, ALTO):
                                    Muestra un mensaje final indicando que se han agotado los intentos.
                                    - pygame.time.delay(4000):
                                    Espera 4 segundos antes de continuar.
                                    - return:
                                    Sale del bucle del juego y termina la función.
                            """

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
                """
                Gestión del uso de comodines:
                - elif comodin_letra_pos.collidepoint(pos) and not comodin_letra_usado:
                Verifica si se ha clickeado el comodín "descubrir letra" y si no ha sido usado.
                - letra_descubierta = descubrir_letra(palabra, letras_adivinadas):
                    Descubre una letra de la palabra que aún no haya sido adivinada.
                - if letra_descubierta:
                    Verifica si se ha descubierto una letra.
                    - letras_adivinadas.append(letra_descubierta):
                    Añade la letra descubierta a la lista de letras adivinadas.
                - comodin_letra_usado = True:
                    Marca el comodín "descubrir letra" como usado.

                - elif comodin_tiempo_pos.collidepoint(pos) and not comodin_tiempo_extra_usado:
                Verifica si se ha clickeado el comodín "tiempo extra" y si no ha sido usado.
                - tiempo_restante = tiempo_extra(tiempo_restante):
                    Añade 30 segundos al tiempo restante.
                - comodin_tiempo_extra_usado = True:
                    Marca el comodín "tiempo extra" como usado.

                - elif comodin_multiplicar_pos.collidepoint(pos) and not comodin_multiplicar_tiempo_usado and tiempo_transcurrido >= 10:
                Verifica si se ha clickeado el comodín "multiplicar tiempo", si no ha sido usado y si han transcurrido menos de 10 segundos.
                - tiempo_restante = multi_tiempo(tiempo_restante, tiempo_transcurrido):
                    Duplica el tiempo restante.
                - comodin_multiplicar_tiempo_usado = True:
                    Marca el comodín "multiplicar tiempo" como usado.
                """

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
    
"""
    Punto de entrada del programa:
    - if __name__ == "__main__":
    Verifica si el archivo se está ejecutando como programa principal.
    - main():
        Llama a la función principal del juego para iniciar la ejecución.
"""