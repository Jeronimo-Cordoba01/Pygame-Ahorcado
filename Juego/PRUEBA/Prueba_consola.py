import random 

def obtener_palabra_aleatoria():
    palabra = ["programacion", "codigo", "juego"]
    palabra_aleatoria = random.choice(palabra)
    return palabra_aleatoria

def mostrar(palabra_secreta, letras_adivinada):
    marcador = ""
    for letra in palabra_secreta:
        if letra in letras_adivinada:
            marcador += letra
        else:
            marcador += "_"
    print(marcador)

def palabra_adivinada(palabra_secreta, letras_adivinadas):
    for letra in palabra_secreta:
        if letra not in letras_adivinadas:
            return False
    return True

def jugar():
    palabra_secreta = obtener_palabra_aleatoria()
    letras_adivinadas = [] 
    intentos_restantes = 6

    while intentos_restantes > 0:
        mostrar(palabra_secreta, letras_adivinadas)
        letra = input("Ingrese una letra: ").lower()

        if letra in letras_adivinadas:
            print("Ya ha intentado con esa letra, pruebe con otra.")
            continue

        if letra in palabra_secreta:
            letras_adivinadas.append(letra)
        else:
            intentos_restantes -= 1
            print(f"Letra incorrecta. Te quedan {intentos_restantes} intentos.")
        
        if palabra_adivinada(palabra_secreta, letras_adivinadas):
            print("Ganaste!, has adivinado la palabra")
            break
    else:
        print(f"Ya no te quedan intentos, perdiste, La palabra era {palabra_secreta}.")

jugar()