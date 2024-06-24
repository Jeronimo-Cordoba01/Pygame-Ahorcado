import pygame, json, csv, random, time

class JuegoAhorcado:
    def __init__(self):
        self.intentos = 6
        self.tiempo_limite = 60
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.puntuacion = 0

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

    def jugar(self, palabra):
        print(f"Comienza el juego del ahorcado. Debes adivinar la palabra en menos de {self.tiempo_limite} segundos.")
        palabra_oculta = ["_"] * len(palabra)
        tiempo_inicial = time.time()
        
        while self.intentos > 0 and "_" in palabra_oculta and time.time() - tiempo_inicial < self.tiempo_limite:
            print(" ".join(palabra_oculta))
            letra = input("Ingresa una letra: ").lower()
            
            if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
                print("Ya has adivinado esa letra. Intenta con otra.")
            elif letra in palabra:
                print("¡Correcto!")
                self.letras_adivinadas.add(letra)
                indices = self.obtener_indices(palabra, letra)
                for i in indices:
                    palabra_oculta[i] = letra
                self.puntuacion += 10
            else:
                print("Incorrecto.")
                self.intentos -= 1
                self.letras_incorrectas.add(letra)
                self.puntuacion -= 5
                print(f"Te quedan {self.intentos} intentos.")
            
            self.actualizar_estado(palabra)
        
        if "_" not in palabra_oculta:
            print("¡Felicidades! Has adivinado la palabra:", palabra)
            self.puntuacion += 50
        else:
            print("Lo siento, se te acabaron los intentos. La palabra era:", palabra)
            self.puntuacion -= 20 
        
        self.actualizar_estado(palabra)

    def main(self):
        palabras = self.obtener_palabras_csv()
        temas = list(palabras.keys())
        
        print("Temas disponibles:")
        for i, tema in enumerate(temas, 1):
            print(f"{i}. {tema}")
        
        tema_seleccionado = int(input("Selecciona un tema (número): "))
        tema = temas[tema_seleccionado - 1]
        palabra = self.seleccionar_palabra(palabras, tema)
        palabra = self.normalizar_palabra(palabra)
        
        self.jugar(palabra)
    
if __name__ == "__main__":
    juego = JuegoAhorcado()
    juego.main()
