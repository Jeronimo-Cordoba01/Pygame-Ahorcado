import pygame, json, csv, random, time

class Horca:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.color_blanco = (255, 255, 255)
        self.base_x = 100
        self.base_y = 400
        self.largo_base = 300
        self.alto_viga = 300
        self.largo_viga = 200
        self.alto_viga_chiquita = 50
        self.partes = 0
    
    def dibujar(self):
        base_inicial = (self.base_x, self.base_y)
        base_final = (self.base_x + self.largo_base, self.base_y)
        pygame.draw.line(self.pantalla, self.color_blanco, base_inicial, base_final, 5)
        
        alto_viga_inicial = (self.base_x + self.largo_base // 2, self.base_y)
        alto_viga_final = (self.base_x + self.largo_base // 2, self.base_y - self.alto_viga)
        pygame.draw.line(self.pantalla, self.color_blanco, alto_viga_inicial, alto_viga_final, 5)
        
        largo_viga_horizontal_inicial = (self.base_x + self.largo_base // 2, self.base_y - self.alto_viga)
        largo_viga_horizontal_final = (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga)
        pygame.draw.line(self.pantalla, self.color_blanco, largo_viga_horizontal_inicial, largo_viga_horizontal_final, 5)
        
        viga_vertical_chiquita_inicial = (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga)
        viga_vertical_chiquita_final = (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita)
        pygame.draw.line(self.pantalla, self.color_blanco, viga_vertical_chiquita_inicial, viga_vertical_chiquita_final, 5)
        
        self.dibujar_partes()
    
    def dibujar_partes(self):
        if self.partes > 0:
            pygame.draw.circle(self.pantalla, self.color_blanco, (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita + 25), 25, 5)
        if self.partes > 1:
            pygame.draw.line(self.pantalla, self.color_blanco, (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita + 50), (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita + 150), 5)
        if self.partes > 2:
            pygame.draw.line(self.pantalla, self.color_blanco, (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita + 75), (self.base_x + self.largo_base // 2 + self.largo_viga - 50, self.base_y - self.alto_viga + self.alto_viga_chiquita + 100), 5)
        if self.partes > 3:
            pygame.draw.line(self.pantalla, self.color_blanco, (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita + 75), (self.base_x + self.largo_base // 2 + self.largo_viga + 50, self.base_y - self.alto_viga + self.alto_viga_chiquita + 100), 5)
        if self.partes > 4:
            pygame.draw.line(self.pantalla, self.color_blanco, (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita + 150), (self.base_x + self.largo_base // 2 + self.largo_viga - 50, self.base_y - self.alto_viga + self.alto_viga_chiquita + 200), 5)
        if self.partes > 5:
            pygame.draw.line(self.pantalla, self.color_blanco, (self.base_x + self.largo_base // 2 + self.largo_viga, self.base_y - self.alto_viga + self.alto_viga_chiquita + 150), (self.base_x + self.largo_base // 2 + self.largo_viga + 50, self.base_y - self.alto_viga + self.alto_viga_chiquita + 200), 5)
    
    def actualizar(self):
        self.partes += 1

class Puntuacion:
    def __init__(self):
        self.puntuacion = 0
    
    def aumentar(self, puntos):
        self.puntuacion += puntos
    
    def disminuir(self, puntos):
        self.puntuacion -= puntos
    
    def guardar(self):
        with open('Puntuaciones.json', mode='w') as file:
            json.dump(self.puntuacion, file)
            
class Palabra:
    def __init__(self, path: str = r"Pygame-Ahorcado\Recursos\Archivos\tematicas_palabras.csv"):
        self.palabras = self.leer_palabras(path)
        self.nueva_palabra()
    
    def leer_palabras(self, path: str) -> list:
        with open(path, mode='r', encoding='utf8') as file:
            next(file)
            reader = csv.reader(file)
            return [row[0].strip().lower() for row in reader]
    
    def nueva_palabra(self):
        self.palabra_actual = random.choice(self.palabras)
        self.letras_correctas = set()
        self.letras_incorrectas = set()
        self.tiempo_inicial = time.time()
    
    def validar_letra(self, letra):
        letra = letra.lower()
        if letra in self.palabra_actual:
            self.letras_correctas.add(letra)
            return True
        else:
            self.letras_incorrectas.add(letra)
            return False
    
    def obtener_palabra_mostrada(self):
        palabra_mostrada = ""
        for letra in self.palabra_actual:
            if letra in self.letras_correctas:
                palabra_mostrada += letra
            else:
                palabra_mostrada += '_'
        
        letras_incorrectas_mostradas = ", ".join(sorted(self.letras_incorrectas))
        return palabra_mostrada, letras_incorrectas_mostradas
    
    def palabra_completa(self):
        return set(self.palabra_actual) == self.letras_correctas
    
    def tiempo_restante(self):
        return 60 - (time.time() - self.tiempo_inicial)