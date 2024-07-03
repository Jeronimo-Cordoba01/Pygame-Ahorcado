# Juego del Ahorcado - 2° Parcial Pygame

## :ghost: Miembros del equipo: :ghost:
- Jerónimo Facundo Lucas Córdoba :man:
- Sophia Antonella Augusto Valenzuela :woman:

## Enunciado:
### Requerimientos Funcionales:
- **Tipos de datos avanzados**: Aplicación de listas, diccionarios, tuplas y sets. :white_check_mark:
- **Funciones**: Modularización y documentación del código en módulos.py. :white_check_mark:
- **Manejo de strings**: Normalización de datos, validaciones y lógica del juego. :white_check_mark:
- **Archivos CSV y JSON**: Uso para persistir datos (puntuación, premios) y leer elementos del juego (rutas de imágenes, preguntas, respuestas, palabras, puntuaciones). :white_check_mark:
- **Matrices**: Aplicación dentro de la lógica del juego.
- **Funciones lambda**: Implementación de al menos una función lambda. :white_check_mark:

### Requerimientos Visuales:
- **Imágenes**: Estáticas y/o dinámicas según la acción del jugador. :white_check_mark:
- **Texto**: Interacción con el jugador mostrada en la ventana del juego. :white_check_mark:
- **Figuras**: Representación de botones u otros elementos del juego. :white_check_mark:
- **Manejo de eventos**: Para la interacción con el usuario. :white_check_mark:

## Idea del Juego:
El juego del ahorcado consiste en adivinar una palabra relacionada con una temática específica, seleccionada de manera aleatoria. Las temáticas pueden incluir historia, entretenimiento, deportes, matemáticas, programación, entre otras.

### :video_game: Funcionamiento: :video_game:
1. **:books: Selección de palabra :books:**:
   - Se elige una palabra al azar relacionada con una temática.
   - Ejemplo:
     - Temática: Programación
     - _ a _ _ a _ _ _
     - Palabra: Variable

2. **:eyeglasses: Adivinanza de letras :eyeglasses:**:
   - El jugador ingresa una letra.
   - Si la letra está en la palabra, se revela en su posición correcta.
   - Si la letra no está, se dibuja una parte de la figura del ahorcado.

3. **:moneybag: Puntuación :moneybag:**:
   - +10 puntos por letra adivinada correctamente. :dollar:
   - -5 puntos por intento fallido. :money_with_wings:
   - Puntos adicionales basados en el tiempo restante (1 punto por segundo sobrante). :chart_with_upwards_trend:

4. **:clock130: Tiempo :clock130:**:
   - El jugador tiene 60 segundos para adivinar cada palabra.
   - Si se queda sin tiempo, pierde.

5. **:recycle: Continuación del juego :recycle:** :
   - Si adivina la palabra antes de completar la figura del ahorcado, gana y sigue jugando con otra palabra y temática al azar.

### :black_joker: Comodines: :black_joker:
- **Descubrir una letra**: Revela una letra al azar en la palabra.
<img src="Recursos/Imagenes/Comodines/Adivinar_letra.jpg" alt="Descubrir una letra" width="200"/>
- **Tiempo extra**: Aumenta 30 segundos al tiempo de la partida actual.
<img src="Recursos/Imagenes/Comodines/Tiempo_extra.jpg" alt="Tiempo extra" width="200"/>
- **Multiplicar tiempo restante**: Duplica el tiempo restante al encontrar la palabra (disponible solo durante los primeros 10 segundos de la partida).
<img src="Recursos/Imagenes/Comodines/Multiplicar_tiempo.jpg" alt="Multiplicar tiempo" width="200"/>
