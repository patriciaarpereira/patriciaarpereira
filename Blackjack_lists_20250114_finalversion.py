# ALGORITMIA E PROGRAMAÇÃO EM PYTHON - PG ANALYTICS & DATA SCIENCE EMPRESARIAL 2024
# Evaluation Exercises - Python

# Blackjack: Beat your opponent by reaching 21 or getting closer than them without going over.
    # Multiplayer: Two players take turns drawing cards to get closer to 21 without exceeding it. The highest score wins.

# With random library
import random as rd


# DECK CONSTRUCTION

# Ranks from 2 to 10 + King, Queen, Jack and Ace
# Suits: Clubs (♣), Diamonds (♦), Hearts (♥) and Spades (♠)
# Points: 
    # Eack rank has the corresponding point; 
    # King, Queen, Jack: 10 points; 
    # Ace: 11 (correction to 1 in a next function)
# Deck
def deck_construction_shuffle():
    global deck, shuffled_deck, deck_points
    deck = []
    deck_points = []
    for ranks in list(range(2, 11)) + ['K', 'Q', 'J', 'A']:
        for suits in ['C', 'D', 'H', 'S']:
            deck.append(str(ranks) + suits)
    for p in list(range(2, 11)) + [10,10,10,11]:
        for repetion in range(4):
            deck_points.append(p)
    shuffled_deck = deck.copy() # make a copy in order to not modify the deck list
    rd.shuffle(shuffled_deck)


# FUNCTIONS

# Players
# Each element of the list represents the number of the player
def number_players():
    global players
    while True:
        try: # to solve the error message if not an integer
            num_players = int(input('How many people will play?: '))
            if num_players > 0:
                players = list(range(1, num_players + 1))
                break
            else: 
                print('Please enter a positive number.')
        except ValueError:
                print('Please enter a positive number.')
    

# Balance amount
def balance(players):
    global balance_players
    balance_players = []
    for player in players:
        while True:
            try: 
                bal_player = int(input(f'What is the balance of player {player}? Please choose 10, 100, 1000 or 10000: '))
                if bal_player in [10, 100, 1000, 10000]:
                    balance_players.append(bal_player)
                    break
                else: 
                    print('Please write one of the available options.')
            except ValueError:
                print('Please write one of the available options.')


# Cards lists for each player
def create_lists(players):
    global bet_players, list_cards_players, list_cards_dealer, list_player_decisions, list_insurance
    bet_players = []
    list_cards_players = []
    list_cards_dealer = []
    list_player_decisions = []
    list_insurance = []
    for player in players:
        list_cards_players.append([])
        list_player_decisions.append([])


# Bet amount
def bet(players):
    for i, player in enumerate(players):
        while True:
            try:
                bet_player = int(input(f'What is the bet of player {player}? Please choose 1, 5, 10 or 100: '))
                if bet_player in [1, 5, 10, 100] and bet_player <= balance_players[i]:
                    bet_players.append(bet_player)
                    break
                else:
                    print('Please write one of the available options and check your balance.')
            except ValueError:
                print('Please write one of the available options.')
    return bet_players


# Dealer deals the cards in each hand
# shuffled_deck.pop(0) simulates the dealer to get a card from the shuffled deck and remove it
hand = 1
def dealer_deals_cards(players, hand, shuffled_deck):
    if hand == 1:
        for dealer_deals in range(2): # to take one card each time (twice because it is the first hand)
            for i, player in enumerate(players):
                list_cards_players[i].append(shuffled_deck.pop(0))
            list_cards_dealer.append(shuffled_deck.pop(0)) 
    elif hand > 1:
        for i, player in enumerate(players):
            if list_points_players[i] < 21 and list_player_decisions[i][-1] in ['H', 'D']:
                list_cards_players[i].append(shuffled_deck.pop(0))
    return list_cards_players, list_cards_dealer
                
    
# Total points and show total points for each hand
# player_cards is the list inside the list_cards_players that represents each player
# Correction for Ace to be 1 point (instead of 11) if total_points > 21
def calculate_total_points(cards_list): #cards_list should be list_cards_players or list_cards_dealer   
    total_points = sum(deck_points[deck.index(card)] for card in cards_list)
    if total_points > 21:
        for card in cards_list:
            if card in ['AC', 'AD', 'AH', 'AS']:
                    total_points -= 10
    return total_points

def total_points_players(list_cards_players):
    global list_points_players
    list_points_players = [] # needed here to clean the previous points
    for i, player in enumerate(list_cards_players):
        list_points_players.append(calculate_total_points(list_cards_players[i]))
        
def show_players_cards_points(players, list_cards_players, list_points_players, deck_points, deck):
    for i, player in enumerate(players):
        print(f'Cards of player {player}: ', list_cards_players[i], f'Total points of player {player}: ', list_points_players[i])
    print('Dealer first card: ', list_cards_dealer[0], 'Dealer first card point: ', deck_points[deck.index(list_cards_dealer[0])])

  
# Show balance and check balance
def show_balance(players, balance_players):
    for i, player in enumerate(players):
        print(f'Player {player} balance: ', balance_players[i])


def check_balance(players, balance_players):
    list_players_balance0 = []
    for i, player in enumerate(players):
        if balance_players[i] < 1: #the smallest bet
            list_players_balance0.append(player)
    for player in list_players_balance0:
        del balance_players[players.index(player)]
        players.remove(player)
        print (f'Player {player} does not have enough funds to play again. Game over!')
    return players, balance_players


# Player decisions
# In case points >= 21 or previous decision is Stand or Surrender, this function is not activated
def ask_player_decision(players, hand):
    for i, player in enumerate(players):
        if hand == 1 and list_points_players[i] < 21: # Double down and surrender are available
            while True: 
                ask_decision = input(f'Player {player}: Please input "S" (Stand), "H" (Hit), "D" (Double) or "Sur" (Surrender): ')
                if ask_decision == 'D':
                    if bet_players[i] * 2 > balance_players[i]:
                        print('You do not have enough balance. Please choose another option.')
                    else:
                        bet_players[i] *= 2
                        print('Your bet was adjusted: ', bet_players[i])
                        list_player_decisions[i].append(ask_decision)
                        break
                elif ask_decision in ['S', 'H', 'Sur']:
                    list_player_decisions[i].append(ask_decision)
                    break
                else:
                    print('Please choose one of the available options.')
        elif hand > 1 and \
            list_points_players[i] < 21 and \
                list_player_decisions[i][-1] in ['H', 'D']: # after the first hand, neither double down nor surrender are available
            while True: 
                ask_decision = input(f'Player {player}: Please input "S" (Stand) or "H" (Hit): ')
                if ask_decision in ['S', 'H']:
                    list_player_decisions[i].append(ask_decision)
                    break
                else:
                    print('Please choose one of the available options.')
    return list_player_decisions, bet_players


# Insurance: if the first dealer's card is an Ace
# The payoff waits until the end of the round
def insurance(list_cards_dealer, players):
    if list_cards_dealer[0] in ['AC', 'AD', 'AH', 'AS']:
        for i, player in enumerate(players):
            while True:
                ask_insurance = input(f'Would player {player} like taking insurance? Please answer "Yes" or "No": ')
                if ask_insurance in ['Yes', 'No']:
                    list_insurance.append(ask_insurance)
                    if ask_insurance == 'Yes':
                        bet_players[i] *= 0.5
                        balance_players[i] -= bet_players[i]
                        print('Your bet was adjusted: ', bet_players[i])
                    break
                else:
                    print('Please choose one of the available options.')
    return bet_players, balance_players, list_insurance


# Total points for dealer after finishing a game round
def points_dealer(list_cards_dealer):
    global total_points_dealer
    total_points_dealer = calculate_total_points(list_cards_dealer)
    while total_points_dealer < 17:
        list_cards_dealer.append(shuffled_deck.pop(0))
        total_points_dealer = calculate_total_points(list_cards_dealer)
        

# Check winner
def check_winner_finish_round():
    for i, player in enumerate(players):
        if list_player_decisions[i] and list_player_decisions[i][-1] == 'Sur':
            print(f'Player {player}: Surrender!')
            balance_players[i] -= 0.5 * bet_players[i]
        elif len(list_cards_players) == 5 and list_points_players[i] <= 21:
            print(f'Player {player}: Charlie Rule!')
            balance_players[i] += bet_players[i]
        elif list_points_players[i] == 21 and len(list_cards_players[i]) == 2:
            if total_points_dealer == 21 and len(list_cards_dealer) == 2:
                print(f'Player {player}: Push!')
            else:
                print(f'Player {player}: Blackjack!')
                balance_players[i] += 1.5 * bet_players[i]
        elif list_points_players[i] > 21:
            print(f'Player {player}: Bust!')
            balance_players[i] -= bet_players[i]
        elif list_points_players[i] <= 21:
            if total_points_dealer == 21 and len(list_cards_dealer) == 2:
                print(f'Player {player}: Dealer has a Blackjack!')
                if list_insurance and list_insurance[i] == 'No': #to prevent an error when the insurance list is empty
                    balance_players[i] -= bet_players[i]
            elif total_points_dealer > 21:
                print(f'Player {player}: You won!')
                balance_players[i] += bet_players[i]
            elif total_points_dealer > list_points_players[i] and total_points_dealer <= 21:
                print(f'Player {player}: You lost!')
                balance_players[i] -= bet_players[i]
            elif total_points_dealer < list_points_players[i] and list_points_players[i] <= 21:
                print(f'Player {player}: You won!')
                balance_players[i] += bet_players[i]
            elif total_points_dealer == list_points_players[i] and total_points_dealer < 21:
                print(f'Player {player}: Push!')
    print('Dealer cards: ', list_cards_dealer, 'Dealer total points: ', total_points_dealer)
    show_balance(players, balance_players)


# Check if the game round is over
# len(list_player_decisions[i]) > 0 was used because otherwise there would be an error when there was no decision
def check_game_over(players, list_points_players, list_player_decisions, list_cards_players):
    if all(list_points_players[i] >= 21 or
           (len(list_player_decisions[i]) > 0 and list_player_decisions[i][-1] in ['S', 'Sur']) or
           len(list_cards_players[i]) == 5
           for i, player in enumerate(players)):
        points_dealer(list_cards_dealer)
        check_winner_finish_round()
        return True
                  
              
# After the first round, ask players if they want to continue
def ask_continue_game(players):
    list_continue_game = []
    for player in players:
        while True:
            continue_game = input(f'Player {player} would like to continue? Please answer "Yes" or "No": ')
            if continue_game in ['Yes', 'No']:
                list_continue_game.append(continue_game)
                break
            else:
                print('Please choose one of the available options.')
    for i, answer in enumerate(list_continue_game):
        if answer == 'No':
            del balance_players[i]
            del players[i]
    return players, balance_players
            
                                                                    
# Add a new deck
# As a rule of thumb, it is used a deck < 20 cards        
def check_deck(shuffled_deck):
    if len(shuffled_deck) < 20:
        new_shuffled_deck = deck[:] # make a copy in order to not modify the deck list
        rd.shuffle(new_shuffled_deck)
        shuffled_deck += new_shuffled_deck
        print ('A new deck was added!')
              

# PLAY BLACKJACK
deck_construction_shuffle()
number_players()
balance(players)
while True:
    hand = 1 # to allow double down and surrender, and to reiniate the play
    create_lists(players)
    bet(players)
    dealer_deals_cards(players, hand, shuffled_deck)
    total_points_players(list_cards_players)
    show_players_cards_points(players, list_cards_players, list_points_players, deck_points, deck)
    insurance(list_cards_dealer, players)
    check_game_over(players, list_points_players, list_player_decisions, list_cards_players) 
    while True:
        ask_player_decision(players, hand)
        hand += 1 # after the first hand, it is not possible to double down or surrender
        dealer_deals_cards(players, hand, shuffled_deck)
        total_points_players(list_cards_players)
        show_players_cards_points(players, list_cards_players, list_points_players, deck_points, deck)
        if check_game_over(players, list_points_players, list_player_decisions, list_cards_players) == True:
            break
    check_balance(players, balance_players)
    check_deck(shuffled_deck)
    ask_continue_game(players)
    if players == []: # no player wants to continue playing
        print('Game over!')
        break

    
           
  
            
        
        
