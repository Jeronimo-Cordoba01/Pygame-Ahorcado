import pygame
import sys

def manejar_eventos_input_box(event, input_box, activo, text, color_inactivo, color_activo):
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
    texto_surface = font.render(texto, True, color)
    texto_rect = texto_surface.get_rect(center=(x, y))
    screen.blit(texto_surface, texto_rect)
    return texto_rect.width, texto_rect.height

def pantalla_input(screen, pizarra, pregunta, ANCHO, ALTO, font):
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
            text, activo, color_actual, return_text = manejar_eventos_input_box(event, input_box, activo, text, color_inactivo, color_activo)
            if return_text and len(text.strip()) > 0:  # Para que no tome espacios en blanco
                return text
            elif return_text:
                pregunta = "Debe ingresar algo para continuar"
        
        screen.fill((255, 255, 255))
        screen.blit(pizarra, (0, 0))
        
        mostrar_texto_centrado(screen, pregunta, font, ANCHO // 2, ALTO // 2 - 100)
        pygame.draw.rect(screen, color_actual, input_box, 2)
        mostrar_texto_centrado(screen, text, font, ANCHO // 2, input_box.centery, color=color_actual)
        pygame.display.flip()