import pygame

pygame.mixer.init()

"""
Configuración de pantalla
Define las dimensiones de la ventana del juego y establece el modo de pantalla y el título.
"""
ANCHO = 1000
ALTO = 800
DIMENSIONES = (ANCHO, ALTO)
screen = pygame.display.set_mode(DIMENSIONES)
pygame.display.set_caption("Ahorcado")

"""
Carga de imágenes
Se cargan y transforman las imágenes necesarias para el juego.
"""
icono = pygame.image.load(r"Recursos\Imagenes\Icono.jpg")
pygame.display.set_icon(icono)
pizarra = pygame.image.load(r'Recursos\Imagenes\Pizzaron.png')
pizarra = pygame.transform.scale(pizarra, DIMENSIONES)
comodin_letra = pygame.image.load(r"Recursos\Imagenes\Comodines\Adivinar_letra.jpg")
comodin_letra = pygame.transform.scale(comodin_letra, (100,100))
comodin_tiempo_extra = pygame.image.load(r"Recursos\Imagenes\Comodines\Tiempo_extra.jpg")
comodin_tiempo_extra = pygame.transform.scale(comodin_tiempo_extra, (100,100))
comodin_multiplicar_tiempo = pygame.image.load(r"Recursos\Imagenes\Comodines\Multiplicar_tiempo.jpg")
comodin_multiplicar_tiempo = pygame.transform.scale(comodin_multiplicar_tiempo, (100,100))

ahorcado_imagenes = [
    pygame.image.load(r"Recursos\Imagenes\Horca\1.horca.png"),
    pygame.image.load(r"Recursos\Imagenes\Horca\2.Ahorcado_cabeza.png"),
    pygame.image.load(r"Recursos\Imagenes\Horca\3.Ahorcado_torse.png"),
    pygame.image.load(r"Recursos\Imagenes\Horca\4.Ahorcado_brazo.png"),
    pygame.image.load(r"Recursos\Imagenes\Horca\5.Ahorcado_dos_brazos.png"),
    pygame.image.load(r"Recursos\Imagenes\Horca\6.Ahorcado_pierna.png"),
    pygame.image.load(r"Recursos\Imagenes\Horca\7.ahorcado_completo.png"),
]

ahorcado_imagenes = [pygame.transform.scale(img, (450,450)) for img in ahorcado_imagenes]

"""
Carga de sonidos
Se cargan y configuran los sonidos y la música del juego.
"""
sonido_falla = pygame.mixer.Sound(r'Recursos\Audio\Falla-letra.mp3')
pygame.mixer.Sound.set_volume(sonido_falla, 0.1)
sonido_acierto = pygame.mixer.Sound(r'Recursos\Audio\Letra-correcta.mp3')
pygame.mixer.Sound.set_volume(sonido_acierto, 0.1)
musica_fondo = pygame.mixer.Sound(r'Recursos\Audio\Musica-de-fondo.mp3')
pygame.mixer.Sound.play(musica_fondo, loops=-1)
pygame.mixer.Sound.set_volume(musica_fondo, 0.1)
musica_ganador = pygame.mixer.Sound(r'Recursos\Audio\Happy-wheels.mp3')
musica_perdedor = pygame.mixer.Sound(r"Recursos\Audio\Sonido de perdedor.mp3")
pygame.mixer.Sound.set_volume(musica_perdedor, 0.1)

def reproducir_musica(musica_fondo, musica):
    """
    Reproduce una música específica deteniendo la música de fondo actual.

    Parámetros:
    musica_fondo: Objeto de sonido de Pygame que representa la música de fondo.
    musica: Objeto de sonido de Pygame que representa la música que se quiere reproducir.
    """
    pygame.mixer.Sound.stop(musica_fondo)
    pygame.mixer.Sound.play(musica)
    pygame.time.delay(4000)