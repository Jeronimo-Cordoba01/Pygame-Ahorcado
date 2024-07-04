def mostrar_parametros_juego(screen, pizarra, comodin_letra, comodin_letra_pos, comodin_tiempo_extra, comodin_tiempo_pos, comodin_multiplicar_tiempo, comodin_multiplicar_pos, ahorcado_imagenes, intentos_restantes, dibujar_letras, font, letras_ingresadas, mostrar_texto, tematica, palabra, letras_adivinadas, puntuacion, tiempo_restante, letras_incorrectas):
    screen.fill((255, 255, 255))
    screen.blit(pizarra, (0, 0))
    screen.blit(comodin_letra, comodin_letra_pos)
    screen.blit(comodin_tiempo_extra, comodin_tiempo_pos)
    screen.blit(comodin_multiplicar_tiempo, comodin_multiplicar_pos)
    screen.blit(ahorcado_imagenes[6 - intentos_restantes], (400, 50))
    dibujar_letras(screen, font, letras_ingresadas)
    
    # screen.fill((255, 255, 255))
    # screen.blit(pizarra, (0, 0))

    # for comodin, pos in comodines:
    #     screen.blit(comodin, pos)
    
    # screen.blit(ahorcado_imagenes[6 - intentos_restantes], (400, 50))
    # dibujar_letras(screen, font, letras_ingresadas)

    palabra_mostrada_lista = []
    for letra in palabra:
        if letra in letras_adivinadas:
            palabra_mostrada_lista.append(letra)
        else:
            palabra_mostrada_lista.append('_')

    palabra_mostrada = ' '.join(palabra_mostrada_lista)
    mostrar_texto(f"Temática: {tematica}", (50, 50))
    mostrar_texto(palabra_mostrada, (50, 150))
    mostrar_texto(f"Puntuación: {round(puntuacion)}", (50, 250))
    mostrar_texto(f"Tiempo: {round(tiempo_restante)}", (50, 350))
    mostrar_texto(f"Letras Incorrectas: {', '.join(letras_incorrectas)}", (50, 450))
    mostrar_texto(f"Intentos restantes: {intentos_restantes}", (50, 600))
