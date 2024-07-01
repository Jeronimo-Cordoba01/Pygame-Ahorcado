import pygame

class Boton:
    def __init__(self, tamaño, posicion, color, texto, pantalla, pizarra, ancho, alto):
        self.tamaño = tamaño
        self.posicion = posicion
        self.color = color
        self.texto = texto
        self.pantalla = pantalla
        self.pizarra = pizarra
        self.ancho = ancho
        self.alto = alto
        self.rect = pygame.Rect(posicion, tamaño)
        self.font = pygame.font.Font(None, 36)
        self.render_texto()

    def render_texto(self):
        self.text_surface = self.font.render(self.texto, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def dibujar(self):
        pygame.draw.rect(self.pantalla, self.color, self.rect)
        self.pantalla.blit(self.text_surface, self.text_rect)

def crear_botones(pantalla, pizarra, ancho, alto):
    tamaño_boton = (200, 100)
    letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    posiciones = [(50, 50), (50, 150), (50, 250), (50, 350), (50, 450), (50, 550), 
                (250, 50), (250, 150), (250, 250), (250, 350), (250, 450), (250, 550),
                (450, 50), (450, 150), (450, 250), (450, 350), (450, 450), (450, 550),
                (650, 50), (650, 150), (650, 250), (650, 350), (650, 450), (650, 550),
                (850, 50), (850, 150), (850, 250), (850, 350)]
    
    botones = [Boton(tamaño_boton, posiciones[i], (255, 255, 255), letra, pantalla, pizarra, ancho, alto) for i, letra in enumerate(letras)]
    return botones
