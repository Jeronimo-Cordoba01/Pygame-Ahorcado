import pygame, sys, csv
from Funciones_prueba import *

SIZE = (1100,800)
FPS = 30
BLANCO = (255,255,255)

pygame.init()

PANTALLA = pygame.display.set_mode(SIZE)

pygame.display.set_caption("Nuestro primer jueguito")

fondo = pygame.image.load(r"Pygame-Ahorcado\Recursos\Imagenes\Pizzaron.png")
fondo = pygame.transform.scale(fondo, SIZE)

icono = pygame.image.load(r"Pygame-Ahorcado\Recursos\Imagenes\Icono.jpg")
pygame.display.set_icon(icono)

pygame.mixer.music.load(r"Pygame-Ahorcado\Recursos\Audio\Musica-de-fondo.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
letra_incorrecta_sonido = pygame.mixer.music.load(r"Pygame-Ahorcado\Recursos\Audio\Falla-letra.mp3")
letra_correcta_sonido = pygame.mixer.music.load(r"Pygame-Ahorcado\Recursos\Audio\Letra-correcta.mp3")
sonido_victoria = pygame.mixer.music.load(r"Pygame-Ahorcado\Recursos\Audio\Happy-wheels.mp3")

PANTALLA.blit(fondo, (0,0))

horca_color = Horca(PANTALLA) 
pygame.draw.line(PANTALLA, BLANCO, (50,500), (100,500), 5)

Jugando = True
while Jugando:
    horca_color.dibujar()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Jugando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                horca_color.dibujar()
                break
        
    pygame.display.update()

pygame.quit()
sys.exit()