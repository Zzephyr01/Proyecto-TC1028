import random as rd
import time
import sys
import os

def clear_screen():
    """
    Limpia la pantalla.
    revisa si el sistema operativo es windows o linux,
    donde los comandos para limpiar pantalla son distintos.
    No recibe nada
    No regresa nada
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def validate_input_numerical(answer):
    """
    Revisa que los inputs que solicitan un número son correctos.
    Recibe un input
    Regresa un número, hasta que el usuario ingrese uno válido
    """
    checking_input = True
    while checking_input:
        if answer.isnumeric():
            checking_input = False
        else:
            print("Input must be a valid number!")
            answer = input("Please enter a number: ")
    return int(answer)

def validate_input_string(answer):
    """
    Revisa que los inputs que solicitan un string son correctos,
    específicamente usado cuando se le pregunta al usuario si
    quiere continuar.
    Recibe un input
    Regresa un string, hasta que el usuario ingrese uno válido
    """
    checking_input = True
    while checking_input:
        if answer.isalpha() and (answer=="y" or answer=="n"):
            checking_input = False
        elif answer.isalpha() and (answer != "y" or answer != "n"):
            print("Input must be either 'y' or 'n'!")
            answer = input("Please enter a valid input: ").lower()
        else:
            print("Input must be a letter!")
            answer = input("Please enter a valid input: ").lower()
    return answer

def create_deck(deck_num):
    """
    Crea una lista con todas las cartas en una baraja normal,
    con el número de barajas indicadas por el usuario.
    Cada elemento se encuentra dentro de su propia lista, para ser
    modificado después.
    Recibe el número de barajas a crear
    Regresa una lista en formato [["A♤"], ["A♦"], ..., ["K♥"]]
    """
    counter = 13 * deck_num
    suit = ["♤", "♦", "♧", "♥"]
    deck = []
    card_num = 1
    disp_num = ""
    idx = 0
    while counter > 0:
        if card_num > 13:
            card_num = 1
        for vi in suit:
            deck.append([])
            if card_num == 1:
                disp_num = "A"
            elif 1 < card_num <= 10:
                disp_num = str(card_num)
            elif card_num == 11:
                disp_num = "J"
            elif card_num == 12:
                disp_num = "Q"
            elif card_num == 13:
                disp_num = "K"
            phold = disp_num + str(vi)
            deck[idx].append(phold)
            idx += 1
        card_num += 1
        counter -= 1
    return deck

def add_card_values(deck):
    """
    Agrega los valores de cada carta a una lista existente de cartas.
    Los valores de las cartas numéricas son iguales a su número.
    Los valores de cartas con A puede ser 1 u 11, de acuerdo con las reglas
    de blackjack, indicado por un "SP" (special).
    Los valores de cartas J, Q, y K son 10.
    Recibe una lista de cartas
    Regresa la misma lista, con el valor de cada carta añadido después de su
    símbolo, en formato [["A♤", "SP"], ..., ["K♥", 10]]
    """
    idx = 0
    for vi in deck:
        if len(vi[0]) == 2:
            if vi[0][0] == "A":
                deck[idx].append("SP")
            elif vi[0][0].isnumeric():
                deck[idx].append(int(vi[0][0]))
            elif vi[0][0] == "J" or vi[0][0] == "Q" or vi[0][0] == "K":
                deck[idx].append(10)
        elif len(vi[0]) == 3:
            deck[idx].append(10)
        idx += 1
    return deck

def shuffle_deck(deck):
    """
    Revuelve las cartas de la baraja.
    Recibe la baraja
    Regresa la baraja en orden aleatorio
    """
    rd.shuffle(deck)
    return deck

def new_deck():
    """
    Crea una nueva baraja. Simplifica las funciones anteriores.
    No recibe nada
    Regresa una baraja nueva, en orden aleatorio
    """
    deck = create_deck(6)
    deck = add_card_values(deck)
    deck = shuffle_deck(deck)
    return deck

def draw_card(hand, deck):
    """
    Añade una carta de la baraja a una mano.
    Recibe la mano a la que añadir, y la baraja
    Devuelve la mano con la primera carta de la baraja,
    y la baraja (con una carta menos)
    """
    hand.append(deck[0])
    deck.pop(0)
    return hand, deck

def draw_cards_init(deck):
    """
    Da 2 cartas al dealer y al jugador.
    Recibe la baraja (en orden aleatorio)
    Devuelve la baraja, la mano del jugador, y la mano del dealer
    """
    p_hand = []
    d_hand = []
    counter = 4
    flag = 0
    while counter > 0:
        if flag == 0:
            draw_card(p_hand, deck)
            flag = 1
        elif flag == 1:
            draw_card(d_hand, deck)
            flag = 0
        counter -= 1
    return deck, p_hand, d_hand

def get_hand_sum(hand):
    """
    Suma el valor de las cartas que tiene una mano.
    La suma suave se considera con los A teniendo un valor de 11.
    La suma dura se considera con los A teniendo un valor de 1.
    Recibe una mano
    Regresa el valor de la suma suave y suma dura de la mano
    """
    soft_sum = 0
    hard_sum = 0
    for card in hand:
        if card[1] == "SP":
            hard_sum += 1
            soft_sum += 11
        else:
            hard_sum += card[1]
            soft_sum += card[1]
    return hard_sum, soft_sum

def get_all_hand_sums(d_hand, p_hand):
    """
    Encuentra la suma de las manos del dealer y el jugador.
    Simplifica el proceso de adquirir las sumas de las manos.
    El dealer siempre se considera con los A teniendo un valor de 11.
    Recibe la mano del dealer, y la mano del jugador
    Regresa el valor de la suma de las manos del jugador y del dealer
    """
    d_hard, d_soft = get_hand_sum(d_hand)
    if d_soft > 21:
        sum_dealer = d_hard
    else:
        sum_dealer = d_soft
    p_hard, p_soft = get_hand_sum(p_hand)
    return p_hard, p_soft, sum_dealer

def renderer(p_hand, d_hand, money, p_soft, p_hard, d_sum, bet):
    """
    Se encarga de mostrarle la información al usuario.
    Recibe las manos del jugador y del dealer, así como otros valores
    a imprimir
    Imprime la UI principal del juego
    No regresa nada
    """
    d_hold = []
    p_hold = []
    for card in d_hand:
        d_hold.append(card[0])
    for card in p_hand:
        p_hold.append(card[0])
    dealer = ("Dealer has:\n" + str(d_hold) + "\n...for a total of "
              + str(d_sum)) + ".\n"
    if p_soft == p_hard:
        player  = ("You have:\n" + str(p_hold) + "\n...for a total of "
                   + str(p_hard)) + ".\n"
    else:
        player = ("You have:\n" + str(d_hold) + "\n...for a total of "
                  + str(p_hard) + " or " + str(p_soft)) + ".\n"
    print("===== Current money: $%d" % money)
    print("===== Current bet: $%d" % bet)
    print(dealer)
    print(player)

def player_action(p_hand, d_hand, deck, d_sum):
    """
    Se encarga de manejar las decisiones que puede hacer el jugador.
    Una vez que el jugador se queda con su mano, el dealer tiene que
    tomar cartas hasta que la suma de su mano sea de 17, en caso
    de no serlo.
    Recibe las manos del jugador y del dealer, la baraja, y la
    suma de la mano del dealer
    Regresa las manos del jugador y del dealer, la baraja, y si el
    jugador decidió quedarse con su mano
    """
    stay = 0
    print("(1) Draw (2) Stay\n")
    choice = validate_input_numerical(input("..?"))
    if choice == 1:
        p_hand, deck = draw_card(p_hand, deck)
        drawn = p_hand[len(p_hand) - 1]
        print("You draw %s" % drawn[0])
    elif choice == 2:
        stay = 1
        while d_sum < 17:
            d_hand, deck = draw_card(d_hand, deck)
            drawn = d_hand[len(d_hand) - 1]
            print("Dealer draws %s" % drawn[0])
            hold = get_hand_sum(d_hand)
            d_sum = hold[1]
    time.sleep(1)
    return p_hand, d_hand, deck, stay

def get_bet(money):
    """
    Se encarga de verificar que el valor a apostar sea correcto
    Recibe el dinero total del jugador
    Regresa el valor de la apuesta actual
    """
    checking_bet = 1
    bet = 0
    while checking_bet:
        clear_screen()
        print("Current money: $%d" % money)
        bet = validate_input_numerical(input("Place your bet: "))
        if bet > money:
            print("Not enough money!")
            time.sleep(1)
            clear_screen()
        elif bet < 0:
            print("Bet can't be negative!")
            time.sleep(1)
            clear_screen()
        else:
            checking_bet = 0
    return bet

def play_game():
    """
    Función principal del juego.
    Ya que podemos jugar manos hasta que el jugador se quede sin dinero, o
    hasta que el jugador quiera cerrar el programa, usamos un ciclo while para
    repetir el juego.
    La pantalla se limpia cada que cambia la UI.
    Cada mano termina una vez que se cumplan condiciones de ganar/perder
    (Tener 21, pasarse de 21, etc.)
    Se calcula el dinero total dependiendo de la apuesta, y se pregunta al
    usuario si desea continuar.
    No recibe nada
    No regresa nada
    """
    playing = 1
    money = 500
    while playing:
        clear_screen()
        deck = new_deck()
        deck, p_hand, d_hand = draw_cards_init(deck)
        end_res = 0
        bet = get_bet(money)
        p_hard, p_soft, sum_dealer = get_all_hand_sums(d_hand, p_hand)
        while end_res == 0:
            clear_screen()

            renderer(p_hand, d_hand, money, p_soft, p_hard, sum_dealer, bet)

            p_hand, d_hand, deck, stay = player_action(p_hand, d_hand, deck, sum_dealer)

            p_hard, p_soft, sum_dealer = get_all_hand_sums(d_hand, p_hand)

            if p_soft == 21 or p_hard == 21:
                end_res = 2
            elif sum_dealer > 21:
                end_res = 1
            elif sum_dealer == 21:
                end_res = 5
            elif p_hard > 21:
                end_res = 4

            if stay and end_res == 0:
                if sum_dealer < p_soft <= 21:
                    end_res = 3
                elif sum_dealer < p_hard <= 21 < p_soft:
                    end_res = 3
                elif p_soft < sum_dealer and p_soft <= 21:
                    end_res = 5
                elif p_hard < sum_dealer and p_soft > 21:
                    end_res = 5
                elif (sum_dealer == p_soft) or (sum_dealer == p_hard and p_soft > 21):
                    end_res = 6
        if end_res == 1:
            payout = bet
            money += payout
            print("Dealer busts! You won $%d" % payout)
        elif end_res == 2:
            payout = bet*1.5
            money += payout
            print("Blackjack! You won $%d" % payout)
        elif end_res == 3:
            payout = bet
            money += payout
            print("You win! You won $%d" % payout)
        elif end_res == 4:
            payout = bet
            money -= payout
            print("You bust! You lost $%d" % payout)
        elif end_res == 5:
            payout = bet
            money -= payout
            print("You lose! You lost $%d" % payout)
        elif end_res == 6:
            print("It's a draw! Nothing happens...")
        elif money <= 0:
            print("You went bankrupt! Closing...")
            time.sleep(2)
            playing = 0
        time.sleep(1)
        choice = validate_input_string(input("Would you like to play again? (y/n)")).lower()
        if choice == "n":
            print("Final score: $%d" % money)
            playing = 0
    sys.exit()

def menu():
    """
    Se encarga de mostrar el menú al iniciar el juego, y de preguntar
    al usuario si desea jugar.
    No recibe nada.
    Regresa un número dependiendo de la respuesta del usuario.
    """
    print(" _____               _       _____         ")
    print("|_   _|_ _ _ ___ ___| |_ _ _|     |___ ___ ")
    print("  | | | | | | -_|   |  _| | |  |  |   | -_|")
    print("  |_| |_____|___|_|_|_| |_  |_____|_|_|___|")
    print("                        |___|              ")
    print("                                           ")
    print("            1)  Start Game                 ")
    print("            2)  Exit                       ")
    choice = validate_input_numerical(input("\n..? "))
    return choice

def twentyone():
    """
    Se encarga de comenzar el juego si el usuario se desea jugar,
    o de terminar el programa si el usuario desea salirse.
    Empieza el juego si el usuario ingresa un valor inválido, ya que
    el usuario tomó la decisión de abrir el programa en primer lugar.
    No recibe nada
    No regresa nada
    """
    choice = menu()
    if choice == 1:
        play_game()
    elif choice == 2:
        sys.exit()
    else:
        print("Invalid input! Starting game anyway!")
        play_game()

if __name__ == '__main__':
    twentyone()