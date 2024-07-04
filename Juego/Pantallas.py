import pygame, sys

#BIENVENIDA Y PLAY
def pantalla_de_inicio(screen, pizarra, font, ANCHO, ALTO):
    """
    Pantalla de inicio
    Muestra la pantalla de bienvenida con un botón "Play".
    Parámetros:
    - screen: La superficie de la pantalla donde se dibujará.
    - pizarra: La imagen de fondo de la pantalla.
    - font: La fuente que se utilizará para dibujar el texto.
    - ANCHO: El ancho de la pantalla.
    - ALTO: La altura de la pantalla.
    """
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

#INGRESAR NOMBRE
def pantalla_ingresar_nombre(screen, pizarra, font, ANCHO, ALTO):
    """
    Pantalla para ingresar nombre
    Muestra una pantalla donde el usuario puede ingresar su nombre.
    Parámetros:
    - screen: La superficie de la pantalla donde se dibujará.
    - pizarra: La imagen de fondo de la pantalla.
    - font: La fuente que se utilizará para dibujar el texto.
    - ANCHO: El ancho de la pantalla.
    - ALTO: La altura de la pantalla.
    """
    input_box = pygame.Rect(ANCHO // 2 - 150, ALTO // 2, 300, 50)
    color_inactivo = pygame.Color((255, 255, 255))
    color_activo = pygame.Color((255, 182, 193))
    color_actual = color_inactivo
    activo = False
    text = ""
    pregunta = ""
    pregunta = ""

    run = False
    while not run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    activo = True
                else:
                    activo = False
                
                if activo:
                    color_actual = color_activo
                else:
                    color_actual = color_inactivo
                
            elif event.type == pygame.KEYDOWN:
                if activo:
                    if event.key == pygame.K_RETURN:
                        if len(text.strip()) > 0: #para que no tome los espacios en blanco
                            return text
                        else:
                            pregunta = "Debe ingresar un nombre para continuar"
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < 10:
                        text += event.unicode 
            
        screen.fill((255,255,255))
        screen.blit(pizarra,(0,0))
        texto = font.render("Ingrese su nombre: ", True, (255,255,255))
        screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))
        
        texto_surface = font.render(text, True, color_actual)
        screen.blit(texto_surface,(input_box.x + 5, input_box.y + 5))

        if pregunta:
            pregunta_surface = font.render(pregunta, True, (255,255,255))
            screen.blit(pregunta_surface,(ANCHO // 2 - pregunta_surface.get_width() // 2, ALTO // 2 + 50 ))
        if pregunta:
            pregunta_surface = font.render(pregunta, True, (255,255,255))
            screen.blit(pregunta_surface,(ANCHO // 2 - pregunta_surface.get_width() // 2, ALTO // 2 + 50 ))
        pygame.draw.rect(screen, color_actual, input_box, 2)
        pygame.display.flip()
        
    return text

#PANTALLAS FINALES
def mostrar_mensaje_final(screen, pizarra, pregunta, palabra, ANCHO, ALTO):
    """
    Muestra el mensaje final
    Muestra un mensaje final con la palabra correcta.
    Parámetros:
    - screen: La superficie de la pantalla donde se dibujará.
    - pizarra: La imagen de fondo de la pantalla.
    - pregunta: El mensaje a mostrar.
    - palabra: La palabra correcta.
    - ANCHO: El ancho de la pantalla.
    - ALTO: La altura de la pantalla.
    """
    font = pygame.font.SysFont("appleberry", 50)
    screen.fill((255,255,255))
    screen.blit(pizarra, (0,0))

    pregunta_final = font.render(pregunta, True,(255,255,255))
    palabra_oculta = font.render(f"La palabra era: {palabra}", True, (255,255,255))

    pregunta_rect = pregunta_final.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    palabra_rect = palabra_oculta.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))

    screen.blit(pregunta_final, pregunta_rect)
    screen.blit(palabra_oculta, palabra_rect)
    pygame.display.flip()
    pygame.time.delay(1000)

#PANTALLA PREGUNTA
def desea_seguir_jugando(screen, pizarra, ANCHO, ALTO):
    """
    Pantalla para preguntar si desea seguir jugando
    Muestra una pantalla donde el usuario puede responder si desea seguir jugando.
    Parámetros:
    - screen: La superficie de la pantalla donde se dibujará.
    - pizarra: La imagen de fondo de la pantalla.
    - ANCHO: El ancho de la pantalla.
    - ALTO: La altura de la pantalla.
    Retorna:
    - bool: True si el usuario desea seguir jugando, False en caso contrario.
    """
    input_box = pygame.Rect(ANCHO // 2 - 150, ALTO // 2, 300, 50)
    color_inactivo = pygame.Color((255, 255, 255))
    color_activo = pygame.Color((255, 182, 193))
    color_actual = color_inactivo
    activo = False
    respuesta = ""

    pregunta_font = pygame.font.SysFont("appleberry", 50)
    respuesta_font = pygame.font.SysFont("appleberry", 50)

    run = False
    while not run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    activo = True
                else:
                    activo = False 
                
                if activo:
                    color_actual = color_activo
                else:
                    color_activo = color_inactivo
            elif event.type == pygame.KEYDOWN:
                if activo: 
                    if event.key == pygame.K_RETURN:
                        if respuesta.lower() == "si":
                            return True
                        elif respuesta.lower() == "no":
                            return False
                        else:
                            respuesta = ""
                    elif event.key == pygame.K_BACKSPACE:
                        respuesta = respuesta[:-1]
                    elif len(respuesta) < 10:
                        respuesta += event.unicode
        
        screen.fill((255, 255, 255))
        screen.blit(pizarra, (0, 0))
        pygame.draw.rect(screen, color_actual, input_box, 2)

        pregunta = pregunta_font.render("¿Desea seguir jugando? (Si / No)", True, (255, 255, 255))
        screen.blit(pregunta, (ANCHO // 2 - pregunta.get_width() // 2, ALTO // 2 - 50))

        respuesta_surface = respuesta_font.render(respuesta, True, color_actual)
        screen.blit(respuesta_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()