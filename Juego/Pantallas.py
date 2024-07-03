import pygame, sys

#BIENVENIDA Y PLAY
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

#INGRESAR NOMBRE
def pantalla_ingresar_nombre(screen, pizarra, font, ANCHO, ALTO):
    input_box = pygame.Rect(ANCHO // 2 - 150, ALTO // 2, 300, 50)
    color_inactivo = pygame.Color((255, 255, 255))
    color_activo = pygame.Color((255, 182, 193))
    color_actual = color_inactivo
    activo = False
    text = ""
    mensaje = ""

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
                        if len(text.strip()) > 0: #asegura que cualquier nombre ingresado solo con espacios en blanco (o incluso vacío) no sea considerado válido.
                            return text
                        else:
                            mensaje = "Debe ingresar un nombre para continuar"
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

        if mensaje:
            mensaje_surface = font.render(mensaje, True, (255,255,255))
            screen.blit(mensaje_surface,(ANCHO // 2 - mensaje_surface.get_width() // 2, ALTO // 2 + 50 ))
        pygame.draw.rect(screen, color_actual, input_box, 2)
        pygame.display.flip()
        
    return text

#PANTALLA VOLVER A JUGAR
def pantalla_volver_a_jugar(screen, pizarra, font, ANCHO, ALTO):
    screen.fill((255, 255, 255))
    screen.blit(pizarra, (0, 0))

    pregunta = font.render("¿Quieres volver a jugar?", True, (255, 255, 255))
    boton_si = font.render("Sí", True, (255, 255, 255), (255, 182, 193))
    boton_no = font.render("No", True, (255, 255, 255), (255, 182, 193))

    pregunta_rect = pregunta.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    boton_si_rect = boton_si.get_rect(center=(ANCHO // 2 - 50, ALTO // 2 + 50))
    boton_no_rect = boton_no.get_rect(center=(ANCHO // 2 + 50, ALTO // 2 + 50))

    screen.blit(pregunta, pregunta_rect)
    screen.blit(boton_si, boton_si_rect)
    screen.blit(boton_no, boton_no_rect)

    pygame.display.flip()

    esperando_respuesta = True
    while esperando_respuesta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if boton_si_rect.collidepoint(pos):
                        return True
                    elif boton_no_rect.collidepoint(pos):
                        return False

#PANTALLAS FINALES
def mostrar_mensaje_final(screen, pizarra, mensaje, palabra, ANCHO, ALTO):
    font = pygame.font.SysFont("appleberry", 50)
    screen.fill((255,255,255))
    screen.blit(pizarra, (0,0))

    mensaje_final = font.render(mensaje, True,(255,255,255))
    palabra_oculta = font.render(f"La palabra era: {palabra}", True, (255,255,255))

    mensaje_rect = mensaje_final.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    palabra_rect = palabra_oculta.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))

    screen.blit(mensaje_final, mensaje_rect)
    screen.blit(palabra_oculta, palabra_rect)
    pygame.display.flip()
    pygame.time.delay(1000)