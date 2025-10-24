# Proyecto TC1028
## Contexto
Alrededor de los 1800, se comenzó a jugar veintiuno, un juego de cartas que, de una manera u otra, evolucionó a lo que
ahora conocemos como [Blackjack](https://en.wikipedia.org/wiki/Blackjack). El objetivo del juego es tomar cartas hasta tener lo más cerca posible a 21, sin pasarse
de 21.
## Algoritmo
El programa debe crear una [baraja estándar](https://en.wikipedia.org/wiki/Standard_52-card_deck) de 52 cartas.\
Luego, debe mezclar las cartas y repartir 2 a cada jugador, en este caso, al dealer y al usuario.\
El jugador debe poder elegir si tomar otra carta o quedarse con su mano actual\
Basándose en eso, el programa debe decidir quién ganó:
- Gana el jugador si la suma de su mano es 21, si la suma de su mano es mayor a la del dealer o si la suma de la mano del dealer es mayor a 21
- Gana el dealer si la suma de su mano es 21, si la suma de su mano es mayor a la del jugador o si la suma de la mano del jugador es mayor a 21

El dinero del jugador debe cambiar dependiendo del resultado y de cuánto haya apostado al inicio de la ronda.\
EL programa deberá preguntarle al usuario si desea seguir jugando, o terminar el programa si el usuario tiene dinero negativo.\
Será posible jugar con dinero igual a 0, o jugar sin apostar al inicio de una ronda.
## Funciones de la librería estandar de python
- `isnumeric()` Recibe un valor y regresa `True` si dicho valor contiene unicamente números.
- `isalpha()` Recibe un valor y regresa `True` si dicho valor contiene unicamente letras del alfabeto latino.
 
## Imports
- `random` tiene varias funciones que sirven para obtener datos al azar. En éste caso, utilizé la función `sort()`, que recibe una lista y la regresa en un orden al azar.\
- `time` fue usado para la función `sleep()`, que pausa el código por un número determinado de segundos.\
- `os` fue usado para limpiar el output de la consola usando `cls` (o `clear` si se está corriendo el programa en python) tras la actualización de la UI y para borrar el menú.\
- `sys` fue usado para terminar el programa usando `exit()` una vez que el usuario lo indica.
