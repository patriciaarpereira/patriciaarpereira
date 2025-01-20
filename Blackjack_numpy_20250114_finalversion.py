# ALGORITMIA E PROGRAMAÇÃO EM PYTHON - PG ANALYTICS & DATA SCIENCE EMPRESARIAL 2024
# Evaluation Exercises - Python

# Blackjack: Beat your opponent by reaching 21 or getting closer than them without going over.
    # Multiplayer: Two players take turns drawing cards to get closer to 21 without exceeding it. The highest score wins.

# Random and numpy libraries
import random as rd
import numpy as np


# DECK CONSTRUCTION

# Ranks from 2 to 10 + King, Queen, Jack and Ace
# Suits: Clubs (♣), Diamonds (♦), Hearts (♥) and Spades (♠)
# Points: 
    # Eack rank is the corresponding point; 
    # King, Queen, Jack: 10 points; 
    # Ace: 11 (correction to 1 in a next function);
    # np.sort to order, np.tile to repeat, np.concatenate to group
# Deck

def deck_construction_shuffle():
    global deck, shuffled_deck, deck_points
    ranks = np.concatenate((np.arange(2,11), np.array(['K', 'Q', 'J', 'A'])))
    suits = np.array(['C', 'D', 'H', 'S'])
    deck = np.array([(rank + suit) for rank in ranks for suit in suits])
    deck_points = np.sort(np.tile(np.concatenate((np.arange(2,11), [10, 10, 10, 11])), 4))
    shuffled_deck = deck.copy() # make a copy in order to not modify the deck list
    rd.shuffle(shuffled_deck)


# FUNCTIONS

# Players
# Each element of the array represents the number of the player
def number_players():
    global players
    while True:
        try:
            num_players = int(input('How many people will play?: '))
            if num_players > 0:
                players = np.arange(1, num_players + 1) 
                break
            else:
                print('Please enter a positive number.')
        except ValueError:
            print('Please enter a positive number.')


# Balance amount
def balance(players):
    global balance_players
    balance_players = np.array([])
    for player in players:
        while True:
            try: 
                bal_player = int(input(f'What is the balance of player {player}? Please choose 10, 100, 1000 or 10000: '))
                if bal_player in [10, 100, 1000, 10000]:
                    balance_players = np.append(balance_players, bal_player)
                    break
                else: 
                    print('Please write one of the available options.')
            except ValueError:
                print('Please write one of the available options.')


# Useful arrays for each player and dealer
def create_arrays(players):
    global bet_players, array_cards_players, array_cards_dealer, array_player_decisions, array_points_players, array_insurance
    bet_players = np.array([])
    array_cards_players = [np.array([]) for player in range(len(players))]
    array_cards_dealer = np.array([])
    array_player_decisions = [np.array([]) for player in range(len(players))]
    array_insurance = np.array([])
        

# Bet amount
def bet(players):
    global bet_players
    for i, player in enumerate(players):
        while True:
            try:
                bet_player = int(input(f'What is the bet of player {player}? Please choose 1, 5, 10 or 100: '))
                if bet_player in [1, 5, 10, 100] and bet_player <= balance_players[i]:
                    bet_players = np.append(bet_players, bet_player)
                    break
                else:
                    print('Please write one of the available options and check your balance.')
            except ValueError:
                print('Please write one of the available options.') 


# Dealer deals the cards in each hand
# np.delete removes the card from the shuffled deck 
hand = 1
def dealer_deals_cards(players, hand):
    global array_cards_players, array_cards_dealer, shuffled_deck
    if hand == 1:
        for dealer_deals in range(2): # to take one card each time (twice because it is the first hand)
            for i, player in enumerate(players):
                array_cards_players[i] = np.append(array_cards_players[i], shuffled_deck[0])
                shuffled_deck = np.delete(shuffled_deck, 0)
            array_cards_dealer = np.append(array_cards_dealer, shuffled_deck[0]) 
            shuffled_deck = np.delete(shuffled_deck, 0)
    elif hand > 1:
        for i, player in enumerate(players):
            if array_points_players[i] < 21 and array_player_decisions[i][-1] in ['H', 'D']:
                array_cards_players[i] = np.append(array_cards_players[i], shuffled_deck[0])
                shuffled_deck = np.delete(shuffled_deck, 0)
        
        
# Total points and show total points for each hand
# Correction for Ace to be 1 point (instead of 11) if total_points > 21
def calculate_total_points(cards_array): #cards_array should be array_cards_players or array_cards_dealer   
    total_points = np.sum(deck_points[np.where(np.isin(deck, cards_array))])
    if total_points > 21 and np.any(np.isin(cards_array, ['AC', 'AD', 'AH', 'AS'])):
            total_points -= 10 * np.count_nonzero(np.isin(cards_array, ['AC', 'AD', 'AH', 'AS']))
    return total_points

def total_points_players(array_cards_players):
    global array_points_players
    array_points_players = np.array([]) # needed here to clean the previous points
    for i, player in enumerate(array_cards_players):
        array_points_players = np.append(array_points_players, calculate_total_points(array_cards_players[i]))
        
def show_players_cards_points(players, array_cards_players, array_points_players):
    for i, player in enumerate(players):
        print(f'Cards of player {player}: ', array_cards_players[i], f'Total points of player {player}: ', array_points_players[i])
    print('Dealer first card: ', array_cards_dealer[0], 'Dealer first card point: ', deck_points[np.where(np.isin(deck, array_cards_dealer[0]))])


# Show balance and check balance
def show_balance(players, balance_players):
    for i, player in enumerate(players):
        print(f'Player {player} balance: ', balance_players[i])

def check_balance():
    global players, balance_players
    for i, player in enumerate(players):
        if balance_players[i] < 1: # check if balance is lower than the minimum possible bet amount
            print (f'Player {player} does not have enough funds to play again. Game over!')   
    players = np.delete(players, np.where(balance_players < 1))
    balance_players = np.delete(balance_players, np.where(balance_players < 1))


# Player decisions
# In case points >= 21 or previous decision is Stand or Surrender, this function is not activated
def ask_player_decision(players, hand):
    for i, player in enumerate(players):
        if hand == 1 and array_points_players[i] < 21: # Double down and surrender are available
            while True: 
                ask_decision = input(f'Player {player}: Please input "S" (Stand), "H" (Hit), "D" (Double) or "Sur" (Surrender): ')
                if ask_decision == 'D':
                    if bet_players[i] * 2 > balance_players[i]:
                        print('You do not have enough balance. Please choose another option.')
                    else:
                        bet_players[i] *= 2
                        print('Your bet was adjusted: ', bet_players[i])
                        array_player_decisions[i] = np.append(array_player_decisions[i], ask_decision)
                        break
                elif ask_decision in ['S', 'H', 'Sur']:
                    array_player_decisions[i] = np.append(array_player_decisions[i], ask_decision)
                    break
                else:
                    print('Please choose one of the available options.')
        elif hand > 1 and \
            array_points_players[i] < 21 and \
                array_player_decisions[i][-1] in ['H', 'D']: # after the first hand, neither double down nor surrender are available
            while True: 
                ask_decision = input(f'Player {player}: Please input "S" (Stand) or "H" (Hit): ')
                if ask_decision in ['S', 'H']:
                    array_player_decisions[i] = np.append(array_player_decisions[i], ask_decision)
                    break
                else:
                    print('Please choose one of the available options.')
    return array_player_decisions, bet_players


# Insurance: if the first dealer's card is an Ace
# The payoff waits until the end of the round
def insurance(array_cards_dealer, players):
    global array_insurance
    if array_cards_dealer[0] in ['AC', 'AD', 'AH', 'AS']:
        for i, player in enumerate(players):
            while True:
                ask_insurance = input(f'Would player {player} like taking insurance? Please answer "Yes" or "No": ')
                if ask_insurance in ['Yes', 'No']:
                    array_insurance = np.append(array_insurance, ask_insurance)
                    if ask_insurance == 'Yes':
                        bet_players[i] *= 0.5
                        balance_players[i] -= bet_players[i]
                        print('Your bet was adjusted: ', bet_players[i])
                    break
                else:
                    print('Please choose one of the available options.')
    return bet_players, balance_players


# Total points for dealer after finishing a game round
def points_dealer():
    global total_points_dealer, shuffled_deck, array_cards_dealer
    total_points_dealer = calculate_total_points(array_cards_dealer)
    while total_points_dealer < 17:
        array_cards_dealer = np.append(array_cards_dealer, shuffled_deck[0])
        shuffled_deck = np.delete(shuffled_deck, 0)
        total_points_dealer = calculate_total_points(array_cards_dealer)


# Check winner
def check_winner_finish_round():
    for i, player in enumerate(players):
        if np.all(len(array_player_decisions[i]) > 0 and array_player_decisions[i][-1] == 'Sur'):
            print(f'Player {player}: Surrender!')
            balance_players[i] -= 0.5 * bet_players[i]
        elif len(array_cards_players) == 5 and array_points_players[i] <= 21:
            print(f'Player {player}: Charlie Rule!')
            balance_players[i] += bet_players[i]
        elif array_points_players[i] == 21 and len(array_cards_players[i]) == 2:
            if total_points_dealer == 21 and len(array_cards_dealer) == 2:
                print(f'Player {player}: Push!')
            else:
                print(f'Player {player}: Blackjack!')
                balance_players[i] += 1.5 * bet_players[i]
        elif array_points_players[i] > 21:
            print(f'Player {player}: Bust!')
            balance_players[i] -= bet_players[i]
        elif array_points_players[i] <= 21:
            if total_points_dealer == 21 and len(array_cards_dealer) == 2:
                print(f'Player {player}: Dealer has a Blackjack!')
                if array_insurance and array_insurance[i] == 'No': #to prevent an error when the insurance list is empty
                    balance_players[i] -= bet_players[i]
            elif total_points_dealer > 21:
                print(f'Player {player}: You won!')
                balance_players[i] += bet_players[i]
            elif total_points_dealer > array_points_players[i] and total_points_dealer <= 21:
                print(f'Player {player}: You lost!')
                balance_players[i] -= bet_players[i]
            elif total_points_dealer < array_points_players[i] and array_points_players[i] <= 21:
                print(f'Player {player}: You won!')
                balance_players[i] += bet_players[i]
            elif total_points_dealer == array_points_players[i] and total_points_dealer < 21:
                print(f'Player {player}: Push!')
    print('Dealer cards: ', array_cards_dealer, 'Dealer total points: ', total_points_dealer)
    show_balance(players, balance_players)


# Check if the game round is over
# Using len(array_player_decisions[i]) > 0 in order to avoid an error due to empty array 
def check_game_over():
    if all(array_points_players[i] >= 21 or
                (len(array_player_decisions[i]) > 0 and
                    array_player_decisions[i][-1] in ['S', 'Sur']) or
                    len(array_cards_players[i]) == 5
                        for i, player in enumerate(players)):
             points_dealer()
             check_winner_finish_round()
             return True

                          
# After the first round, ask players if they want to continue
def ask_continue_game():
    global balance_players, players
    continue_game_array = np.array([])
    for player in players:
        while True:
            continue_game = input(f'Player {player} would like to continue? Please answer "Yes" or "No": ')
            if continue_game in ['Yes', 'No']:
                continue_game_array = np.append(continue_game_array, continue_game)
                break
            else:
                print('Please choose one of the available options.')
    balance_players = np.delete(balance_players, np.where(continue_game_array == 'No'))
    players = np.delete(players, np.where(continue_game_array == 'No'))
            
                          
# Add a new deck
# As a rule of thumb, it is used a deck < 20 cards        
def check_deck():
    global shuffled_deck
    if len(shuffled_deck) < 20:
        new_shuffled_deck = deck.copy() # make a copy in order to not modify the deck list
        rd.shuffle(new_shuffled_deck)
        shuffled_deck = np.concatenate((shuffled_deck, new_shuffled_deck))
        print ('A new deck was added!')
              

# PLAY BLACKJACK
deck_construction_shuffle()
number_players()
balance(players)
while True:
    hand = 1 # to allow double down and surrender, and to reiniate the play
    create_arrays(players)
    bet(players)
    dealer_deals_cards(players, hand)
    total_points_players(array_cards_players)
    show_players_cards_points(players, array_cards_players, array_points_players)
    insurance(array_cards_dealer, players)
    check_game_over()
    while True:
        ask_player_decision(players, hand)
        hand += 1 # after the first hand, it is not possible to double down or surrender
        dealer_deals_cards(players, hand)
        total_points_players(array_cards_players)
        show_players_cards_points(players, array_cards_players, array_points_players)
        if check_game_over() == True:
            break
    check_balance()
    check_deck()
    ask_continue_game()
    if len(players) == 0: # no player wants to continue playing
        print('Game over!')
        break
        
        
