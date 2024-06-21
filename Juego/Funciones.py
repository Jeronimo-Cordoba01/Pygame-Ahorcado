import pygame

class horca: 
    def __init__(self, PANTALLA):
        self.pantalla = PANTALLA
        self.color_blanco = (255,255,255)
        self.base_x = 50
        self.base_y = 400
        self.largo_base = 300
        self.alto_viga = 300
        self.largo_viga = 200
        self.largo_viga_vertical = 50

    def dibujar(self):
        base_inicial = (self.base_x, self.base_y)
        base_final = (self.base_x + self.largo_base, self.base_y)
        pygame.draw.line(self.pantalla, self.color_blanco, base_inicial, base_final, 5)

        

