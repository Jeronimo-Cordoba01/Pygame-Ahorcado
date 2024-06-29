import csv, json, random, pygame, sys

def pantalla_de_inicio(screen, pizarra, font, ANCHO, ALTO):
    titulo = font.render("Bienvenido al juego del ahorcado", True, (255,255,255))
    boton_play = font.render("Play", True, (255,255,255), (255, 182, 193))
    
    boton_play_rect = boton_play.get_rect()
    boton_play_rect.center = (ANCHO // 2, ALTO // 2)

    pos_titulo = (ANCHO // 2 - titulo.get_width() // 2, 270)

    screen.blit(pizarra, (0,0))
    screen.blit(titulo, pos_titulo)
    screen.blit(boton_play, boton_play_rect)

    pygame.display.flip()
    
    jugando = False
    while not jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    jugando = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if boton_play_rect.collidepoint(pos):
                        jugando = True

def leer_palabras(path: str = r"Recursos\Archivos\tematicas_palabras.csv"):
    tematicas_palabras = {}
    with open(path, newline='', encoding= "utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Leer la primera fila como encabezados
        for row in reader:
            for i, palabra in enumerate(row):
                tematica = headers[i]
                palabra = palabra.lower()
                if tematica not in tematicas_palabras:
                    tematicas_palabras[tematica] = []
                tematicas_palabras[tematica].append(palabra)
    return tematicas_palabras

def seleccionar_palabra(tematicas_palabras):
    tematica = random.choice(list(tematicas_palabras.keys()))
    palabra = random.choice(tematicas_palabras[tematica])
    return tematica, palabra

def cargar_json(path: str):
    try:
        with open(path, 'r', encoding= "utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
    return data

def guardar_json(path: str, data):
    with open(path, 'w', encoding= "utf-8") as file:
        json.dump(data, file)

def actualizar_puntuacion(puntos, path: str =r'Recursos\Archivos\Puntuacion.json'):
    puntuacion = cargar_json(path)
    puntuacion['puntuacion'] = puntuacion.get('puntuacion', 0) + puntos
    guardar_json(path, puntuacion)

def registrar_letra_incorrecta(letra, path: str =r'Recursos\Archivos\Letras_incorrectas.json'):
    letras_incorrectas = cargar_json(path)
    letras_incorrectas['letras'] = letras_incorrectas.get('letras', []) + [letra]
    guardar_json(path, letras_incorrectas)
    
def limpiar_letras_incorrectas(path: str = r'Recursos\Archivos\Letras_incorrectas.json'):
    letras_incorrectas = {'letras': []}
    guardar_json(path, letras_incorrectas)


#comodin descubrir_letra
def descubrir_letra(palabra, letras_adivinadas):
    letras_disponibles = [letra for letra in palabra if letra not in letras_adivinadas]
    if letras_disponibles:
        letra = random.choice(letras_disponibles)
        return letra
    return None

#comodin tiempo extra
def tiempo_extra(tiempo_restante, tiempo_extra=30):
    return tiempo_restante + tiempo_extra