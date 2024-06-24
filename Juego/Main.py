"""
Miembros: Jerónimo Facundo Lucas Córdoba, Sophia Antonella Augusto Valenzuela
---
2° Parcial - Pygame - Ahorcado 
---
Enunciado:
Dada la consigna asignada, deberán desarrollar de a dos el juego. Aplicando los siguientes requerimientos:

Desde lo funcional:
●	Aplicar tipos de datos avanzados: listas, diccionarios, tuplas, sets.
●	Funciones. El código debe estar debidamente modularizado y documentado. Tengan en cuenta los objetivos de la programación 
    con funciones. Realizar módulos.py para la correcta organización de las mismas.
●	Manejo de strings: para normalizar datos, realizar validaciones, funcionamiento inherente a la lógica del juego, etc.
●	Archivos csv y Json. Se deberán utilizar los dos tipos de archivos tanto para persistir datos (score, premios, etc) como 
    para leer los elementos del juego (rutas de imágenes, preguntas, respuestas, palabras, puntuaciones, etc)
●	Matrices: deberán aplicar por lo menos una matriz dentro de la lógica del juego.
●	Funciones lambda: deberán aplicar por lo menos una función lambda.

Desde lo visual:
●	Imágenes. Según la temática del juego a desarrollar, habrá imágenes estáticas y/o dinámicas 
    (que van cambiando con cada acción del jugador)
●	Texto: toda interacción con el jugador implica que esos mensajes se muestran por la ventana del juego.
●	Figuras:  para representar botones, o cualquier elemento del juego que necesiten.
●	Manejo de eventos: para la interacción con el usuario.

ENTREGA
Deberán crear un repositorio privado en git (compartido con todos los profesores), en el cual subirán:
    a.	El proyecto del juego.
    b.	Markdown con instrucciones, capturas y todo lo que consideren necesario para presentar su juego.

DEFENSA
El día del parcial evaluaremos los grupos en clase. Deberán hacer un gameplay (el programa debe estar preparado ante cualquier fallo. 
Si falla 3 veces o más, el parcial estará desaprobado). Luego evaluaremos su defensa y calificaremos individualmente a 
cada integrante del grupo.
----------------------------------------------------------------------------------------------------------------------------------
Idea del juego:
El juego del ahorcado tiene como tema principal adivinar la palabra relacionada con una materia específica, 
como matemáticas, historia, ciencias, etc. Por ejemplo, se elige de manera al azar una palabra sobre alguna temática en cuestión 
(historia, entretenimiento, deportes, matemáticas, programación, etc)

Funcionamiento del juego:
Selección de palabra: Al comienzo de cada partida, el juego elige aleatoriamente una palabra relacionada con una 
temática aleatoria por ejemplo: 
        Temática: Programación
        _ a _ _ a _ _ _
Palabra: Variable

Adivinanza de letras: El jugador ingresa una letra desde la pantalla (o teclado). Si la letra es parte de la palabra oculta, 
se revela en su posición correcta en la palabra. Si la letra no está en la palabra, se dibuja una parte de la figura del ahorcado.

Puntuación: Por cada letra adivinada correctamente, el jugador ganará +10 puntos y perderá 5 puntos por cada intento fallido. 
Si el jugador gana la partida acumulara el puntaje obtenido en su score.

Tiempo: El jugador tiene 60 segundos para adivinar cada palabra si se queda sin tiempo pierde.

El jugador si adivina la palabra correctamente antes de que se complete la figura del ahorcado, gana y sigue jugando 
(Se selecciona al azar otra temática y otra palabra) también va a acumular los puntos adicionales basados en el tiempo restante: 
(1 punto por segundo que le sobre), cada vez que se adivina una palabra el tiempo se reinicia.
Si el jugador se queda sin tiempo o agota todos los intentos y la figura del ahorcado se completa pierde.

Comodines:
●	Descubrir una letra: al elegir este comodín el juego descubre una letra al azar. Si existen más incidencias de esa letra 
    no las descubre. 
●	Tiempo extra: al elegir este comodín, se aumentará 30 segundos a la partida actual.
●	Multiplicar tiempo restante: este comodín se podrá elegir al comienzo de la partida (durante los primeros 10 segundos). 
    El mismo duplicará el tiempo restante una vez encontrada la palabra. Si el jugador no la descubre, el comodín queda sin efecto.
"""

import pygame, json, csv, random, time

class JuegoAhorcado:
    def __init__(self, pantalla):
        self.intentos = 6
        self.tiempo_limite = 60
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.puntuacion = 0
        self.pantalla = pantalla
        self.font = pygame.font.SysFont(None, 55)
        self.palabra_oculta = []
        self.tiempo_inicial = 0

    def obtener_palabras_csv(self):
        palabras = {}
        with open('tematicas_palabras.csv', 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                tema = fila['Tema']
                palabra = fila['Palabra']
                if tema not in palabras:
                    palabras[tema] = []
                palabras[tema].append(palabra)
        return palabras

    def guardar_estado_json(self, estado):
        with open('Estado.json', 'w', encoding='utf-8') as archivo:
            json.dump(estado, archivo, ensure_ascii=False, indent=4)

    def cargar_estado_json(self):
        with open('Estado.json', 'r', encoding='utf-8') as archivo:
            estado = json.load(archivo)
        return estado

    def seleccionar_palabra(self, palabras, tema):
        return random.choice(palabras[tema])

    def normalizar_palabra(self, palabra):
        return palabra.lower().strip()

    def verificar_letra(self, palabra, letra):
        return letra in palabra

    def obtener_indices(self, palabra, letra):
        return [i for i, l in enumerate(palabra) if l == letra]

    def actualizar_estado(self, palabra):
        estado = {
            "palabra": palabra,
            "intentos_restantes": self.intentos,
            "letras_adivinadas": list(self.letras_adivinadas),
            "letras_incorrectas": list(self.letras_incorrectas),
            "puntuacion": self.puntuacion
        }
        self.guardar_estado_json(estado)

    def dibujar_texto(self, texto, pos):
        texto_superficie = self.font.render(texto, True, (255, 255, 255))
        self.pantalla.blit(texto_superficie, pos)

    def jugar(self, palabra):
        self.palabra_oculta = ["_"] * len(palabra)
        self.tiempo_inicial = time.time()
        jugando = True
        
        while jugando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False
                elif event.type == pygame.KEYDOWN:
                    letra = event.unicode.lower()
                    if letra.isalpha() and len(letra) == 1:
                        if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
                            pass
                        elif letra in palabra:
                            self.letras_adivinadas.add(letra)
                            indices = self.obtener_indices(palabra, letra)
                            for i in indices:
                                self.palabra_oculta[i] = letra
                            self.puntuacion += 10
                        else:
                            self.intentos -= 1
                            self.letras_incorrectas.add(letra)
                            self.puntuacion -= 5
                
            self.pantalla.fill((0, 0, 0))
            self.dibujar_texto(" ".join(self.palabra_oculta), (50, 150))
            self.dibujar_texto(f"Intentos restantes: {self.intentos}", (50, 50))
            self.dibujar_texto(f"Puntuación: {self.puntuacion}", (50, 100))
            pygame.display.flip()
            
            if "_" not in self.palabra_oculta or self.intentos <= 0 or time.time() - self.tiempo_inicial >= self.tiempo_limite:
                jugando = False
        
        if "_" not in self.palabra_oculta:
            self.puntuacion += 50
        else:
            self.puntuacion -= 20
        
        self.actualizar_estado(palabra)

    def main(self):
        palabras = self.obtener_palabras_csv()
        temas = list(palabras.keys())
        
        tema = random.choice(temas)
        palabra = self.seleccionar_palabra(palabras, tema)
        palabra = self.normalizar_palabra(palabra)
        
        self.jugar(palabra)

if __name__ == "__main__":
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Juego del Ahorcado")
    juego = JuegoAhorcado(pantalla)
    juego.main()
    pygame.quit()
