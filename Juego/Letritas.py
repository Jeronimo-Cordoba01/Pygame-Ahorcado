import pygame, string

def dibujar_letras(screen, font, letras_ingresadas):
    """
    Dibuja las letras del abecedario en la pantalla.
    Parámetros:
    - screen: La superficie de la pantalla donde se dibujarán las letras.
    - font: La fuente que se utilizará para dibujar las letras.
    - letras_ingresadas: Lista de letras que ya han sido ingresadas por el usuario.
    """
    letras = string.ascii_lowercase #para obtener el abecedario
    letra_eje_x = 500 #derecha
    letra_eje_y = 500 #arriba
    espacio_entre_letras = 30
    letras_por_fila = 13 
    font = pygame.font.SysFont("appleberry", 40)

    for i, letra in enumerate(letras):
        fila = 0 if i < letras_por_fila else 1
        columna = i % letras_por_fila

        letra_surface = font.render(letra, True, (255, 255, 255))
        letra_rect = letra_surface.get_rect(topleft=(letra_eje_x + columna * espacio_entre_letras, letra_eje_y + fila * 40))

        if letra not in letras_ingresadas:
            screen.blit(letra_surface, letra_rect)

def letra_click(pos):       
    """
    Detecta si una letra ha sido clickeada.
    Parámetros:
    - pos: La posición (x, y) del clic del mouse.
    Retorna:
    - str: La letra clickeada si está dentro del área de alguna letra.
    - None: Si el clic no está dentro del área de ninguna letra.
    """
    letras = string.ascii_lowercase
    letra_eje_x = 500
    letra_eje_y = 500
    espacio_entre_letras = 30
    letras_por_fila = 13 

    for i, letra in enumerate(letras):
        fila = 0 if i < letras_por_fila else 1
        columna = i % letras_por_fila

        letra_rect = pygame.Rect(letra_eje_x + columna * espacio_entre_letras, letra_eje_y + fila * 40, 20, 20)
        if letra_rect.collidepoint(pos):
            return letra

    return None