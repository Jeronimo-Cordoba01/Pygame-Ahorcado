import pygame
import sys

def manejar_eventos_input_box(event, input_box, activo, text, color_inactivo, color_activo):
    """
    Maneja los eventos para una caja de entrada de texto.

    Parámetros:
    event: El evento de Pygame.
    input_box: El rectángulo que define la caja de entrada.
    activo: Booleano que indica si la caja de entrada está activa.
    text: El texto actual en la caja de entrada.
    color_inactivo: El color de la caja de entrada cuando no está activa.
    color_activo: El color de la caja de entrada cuando está activa.

    Retorna:
    text: El texto actualizado.
    activo: El estado actualizado de la caja de entrada.
    color_actual: El color actual de la caja de entrada.
    texto_retornado: Booleano que indica si se debe retornar el texto.
    """
    color_actual = color_inactivo

    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_box.collidepoint(event.pos):
            activo = not activo
        else:
            activo = False
    if activo:
        color_actual = color_activo
    else:
        color_actual = color_inactivo
    
    if event.type == pygame.KEYDOWN and activo:
        if event.key == pygame.K_RETURN:
            return text, activo, color_actual, True
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += event.unicode
    
    return text, activo, color_actual, False

def mostrar_texto_centrado(screen, texto, font, x, y, color=(255, 255, 255)):
    """
    Muestra un texto centrado en la pantalla.

    Parámetros:
    screen: La superficie de la pantalla donde se dibujará.
    texto: El texto a mostrar.
    font: La fuente utilizada para el texto.
    x: La coordenada x del centro del texto.
    y: La coordenada y del centro del texto.
    color: El color del texto.

    Retorna:
    width: El ancho del texto renderizado.
    height: La altura del texto renderizado.
    """
    texto_surface = font.render(texto, True, color)
    texto_rect = texto_surface.get_rect(center=(x, y))
    screen.blit(texto_surface, texto_rect)
    return texto_rect.width, texto_rect.height

def pantalla_input(screen, pizarra, pregunta, ANCHO, ALTO, font):
    """
    Muestra una pantalla de entrada de texto con una pregunta.

    Parámetros:
    screen: La superficie de la pantalla donde se dibujará.
    pizarra: La imagen de fondo de la pantalla.
    pregunta: La pregunta a mostrar.
    ANCHO: El ancho de la pantalla.
    ALTO: La altura de la pantalla.
    font: La fuente utilizada para el texto.

    Retorna:
    text: El texto ingresado por el usuario.
    """
    input_box = pygame.Rect(ANCHO // 2 - 150, ALTO // 2, 300, 50)
    color_inactivo = pygame.Color(255, 255, 255)
    color_activo = pygame.Color(255, 182, 193)
    color_actual = color_inactivo
    activo = False
    text = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            text, activo, color_actual, texto_retornado = manejar_eventos_input_box(event, input_box, activo, text, color_inactivo, color_activo)
            if texto_retornado and len(text.strip()) > 0:  # Para que no tome espacios en blanco
                return text
            elif texto_retornado:
                pregunta = "Debe ingresar algo para continuar"
        
        screen.fill((255, 255, 255))
        screen.blit(pizarra, (0, 0))
        
        mostrar_texto_centrado(screen, pregunta, font, ANCHO // 2, ALTO // 2 - 100)
        pygame.draw.rect(screen, color_actual, input_box, 2)
        mostrar_texto_centrado(screen, text, font, ANCHO // 2, input_box.centery, color=color_actual)
        pygame.display.flip()