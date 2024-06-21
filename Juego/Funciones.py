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
        self.alto_viga_chiquita = 50

    def dibujar(self):
        base_inicial = (self.base_x, self.base_y)
        base_final = (self.base_x + self.largo_base, self.base_y)
        pygame.draw.line(self.pantalla, self.color_blanco, base_inicial, base_final, 5)

        alto_viga_inicial = (self.base_x + self.largo_base // 2, self.base_y)
        alto_viga_final = (self.base_x+ self.largo_base // 2, self.base_y - self.alto_viga)
        pygame.draw.line(self.pantalla, self.color_blanco, alto_viga_inicial, alto_viga_final, 5)

        largo_viga_horizontal_inicial = (self.base_x + self.largo_base // 2, self.base_y - self.alto_viga)
        largo_viga_horizontal_final = (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga )
        pygame.draw.line(self.pantalla, self.color_blanco, largo_viga_horizontal_inicial, largo_viga_horizontal_final, 5)

        viga_vertical_chiquita_inical = (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga)
        viga_vertical_chiquita_final = (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita)
        pygame.draw.line(self.pantalla, self.color_blanco, viga_vertical_chiquita_inical, viga_vertical_chiquita_final, 5)

