import pygame, sys
from Letritas import dibujar_letras
from Manejo_pantallas import *

#BIENVENIDA Y PLAY
def pantalla_de_inicio(screen, pizarra, font, ANCHO, ALTO):
    """
    Muestra la pantalla de inicio del juego del ahorcado.

    Parámetros:
    screen: La superficie de la pantalla donde se dibujará.
    pizarra: La imagen de fondo de la pantalla.
    font: La fuente utilizada para los textos.
    ANCHO: El ancho de la pantalla.
    ALTO: La altura de la pantalla.
    """
    titulo = font.render("Bienvenido al juego del ahorcado", True, (255, 255, 255))
    boton_play = font.render("Play", True, (255, 255, 255), (255, 182, 193))
    boton_play_rect = boton_play.get_rect(center=(ANCHO // 2, ALTO // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and boton_play_rect.collidepoint(event.pos):
                return
        
        screen.fill((255, 255, 255))
        screen.blit(pizarra, (0, 0))
        screen.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 270))
        screen.blit(boton_play, boton_play_rect)
        pygame.display.flip()

#INGRESAR NOMBRE
def pantalla_ingresar_nombre(screen, pizarra, font, ANCHO, ALTO):
    """ 
    Muestra la pantalla donde se debe ingresar el nombre

    Parámetros:
    screen: La superficie de la pantalla donde se dibujará.
    pizarra: La imagen de fondo de la pantalla.
    font: La fuente utilizada para los textos.
    ANCHO: El ancho de la pantalla.
    ALTO: La altura de la pantalla.

    retorna el nombre 

    """
    pregunta = "Ingrese su nombre:"
    nombre = pantalla_input(screen, pizarra, pregunta, ANCHO, ALTO, font)
    return nombre

#PANTALLAS FINALES
def mostrar_mensaje_final(screen, pizarra, pregunta, palabra, ANCHO, ALTO, puntuacion):
    """
    Muestra el mensaje final
    Muestra un mensaje final con la palabra correcta.
    Muestra la puntuaccion del participante
    Parámetros:
    - screen: La superficie de la pantalla donde se dibujará.
    - pizarra: La imagen de fondo de la pantalla.
    - pregunta: El mensaje a mostrar.
    - palabra: La palabra correcta.
    - ANCHO: El ancho de la pantalla.
    - ALTO: La altura de la pantalla.
    - puntuaccion: la puntuacion del participante
    """
    font = pygame.font.SysFont("appleberry", 50)
    screen.fill((255,255,255))
    screen.blit(pizarra, (0,0))
    pregunta_final = font.render(pregunta, True,(255,255,255))
    palabra_oculta = font.render(f"La palabra era: {palabra}", True, (255,255,255))
    puntuacion_texto = font.render(f"tu puntuacion fue de: {puntuacion}", True, (255, 182, 193) )

    pregunta_rect = pregunta_final.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    palabra_rect = palabra_oculta.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
    puntuacion_rect = puntuacion_texto.get_rect(center=(ANCHO // 2, ALTO // 2))

    screen.blit(pregunta_final, pregunta_rect)
    screen.blit(palabra_oculta, palabra_rect)
    screen.blit(puntuacion_texto, puntuacion_rect)
    pygame.display.flip()
    pygame.time.delay(1000)

#PANTALLA PREGUNTA
def desea_seguir_jugando(screen, pizarra, ANCHO, ALTO):
    """
    Pregunta al jugador si desea seguir jugando.

    Parámetros:
    screen: La superficie de la pantalla donde se dibujará.
    pizarra: La imagen de fondo de la pantalla.
    ANCHO: El ancho de la pantalla.
    ALTO: La altura de la pantalla.

    Retorna:
    True si el jugador desea seguir jugando, False en caso contrario.
    """
    font = pygame.font.SysFont("appleberry", 50)
    pregunta = "¿Desea seguir jugando? (Si / No)"
    respuesta = pantalla_input(screen, pizarra, pregunta, ANCHO, ALTO, font)
    respuesta = respuesta.lower().strip()
    if respuesta == "si":
        return True
    elif respuesta == "no":
        return False

    return desea_seguir_jugando(screen, pizarra, ANCHO, ALTO)

def renderizar_pantalla(screen, pizarra, comodin_letra, comodin_tiempo_extra, comodin_multiplicar_tiempo, ahorcado_imagenes, estado_juego, font):
    """
    Renderiza los elementos visuales del juego en la pantalla.

    Parámetros:
    screen: La superficie de la pantalla donde se dibujará.
    pizarra: La imagen de fondo de la pantalla.
    comodin_letra: La imagen del comodín de letra.
    comodin_tiempo_extra: La imagen del comodín de tiempo extra.
    comodin_multiplicar_tiempo: La imagen del comodín de multiplicar tiempo.
    ahorcado_imagenes: Lista de imágenes del ahorcado.
    estado_juego: Diccionario con el estado actual del juego.
    font: La fuente utilizada para los textos.
    """
    screen.fill((255, 255, 255))
    screen.blit(pizarra, (0, 0))
    screen.blit(comodin_letra, estado_juego["comodin_letra_pos"])
    screen.blit(comodin_tiempo_extra, estado_juego["comodin_tiempo_pos"])
    screen.blit(comodin_multiplicar_tiempo, estado_juego["comodin_multiplicar_pos"])
    screen.blit(ahorcado_imagenes[6 - estado_juego["intentos_restantes"]], (400, 50))
    dibujar_letras(screen, font, estado_juego["letras_ingresadas"])

def mostrar_textos(screen, font, estado_juego, tiempo_restante):
    """
    Muestra los textos informativos en la pantalla del juego.

    Parámetros:
    screen: La superficie de la pantalla donde se dibujará.
    font: La fuente utilizada para los textos.
    estado_juego: Diccionario con el estado actual del juego.
    tiempo_restante: El tiempo restante del juego.
    """
    mostrar_texto = lambda texto, pos: screen.blit(font.render(texto, True, (255,255,255)), pos)
    palabra_mostrada = []
    for letra in estado_juego["palabra"]:
        letra_encontrada = False
        for letra_adivinada in estado_juego["letras_adivinadas"]:
            if letra == letra_adivinada:
                letra_encontrada = True
                break
        if letra_encontrada:
            palabra_mostrada.append(letra)
        else:
            palabra_mostrada.append('_')
    palabra_mostrada = ''.join(palabra_mostrada)          
    mostrar_texto(f"Temática: {estado_juego['tematica']}", (50, 50))
    mostrar_texto(palabra_mostrada, (50, 150))
    mostrar_texto(f"Puntuación: {round(estado_juego['puntuacion'])}", (50, 250))
    mostrar_texto(f"Tiempo: {round(tiempo_restante)}", (50, 350))
    mostrar_texto(f"Letras Incorrectas: {', '.join(estado_juego['letras_incorrectas'])}", (50, 450))
    mostrar_texto(f"Intentos restantes: {estado_juego['intentos_restantes']}", (50, 600))