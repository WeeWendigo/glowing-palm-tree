import random

BOT_NUM = 1
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

#cards = [card_face, card_value]
cards = [
    ['A', 1],
    ['2', 2],
    ['3', 3],
    ['4', 4],
    ['5', 5],
    ['6', 6],
    ['7', 7],
    ['8', 8],
    ['9', 9],
   ['10', 10],
    ['J', 11],
    ['Q', 12],
    ['K', 13]
]

######## -MAKES A STANDARD 52 CARD DECK- (jokers not included)
def make_deck(cards):
    suites = ["s", "c", "h", "d"]
    deck = []
    for card in cards:
        for suit in suites:
            deck.append([card[0] + suit, card[1]])
    return deck

######## -SLOTS SYMBOLS-
symbol_count = {
    '*': 3,
    '0': 5,
    '%': 5,
    '#': 9
}

symbol_value = {
    '*': 5,
    '0': 3 ,
    '%': 2,
    '#': 1
}

#-----------------------------------------------------------------------------------------------------------------------
#                                                BLACK JACK

def make_21_deck(cards):
    suites = ["s", "c", "h", "d"]
    done_deck = []
    for card in cards:
        for suit in suites:
            done_deck.append([card[0] + suit, card[1]])
    for card in done_deck:
        if card[-1] > 10:
            card[-1] = 10

    return done_deck

def draw_card(hand, deck, check_in):
    new_card = random.choice(deck)
    deck.remove(new_card)
    hand.append(new_card)
    value, check_in = check_hand_value(hand, check_in)
    if value >= 21:
        check_in = False
    return hand, check_in

def check_hand_value(hand, check_in):
    total = 0
    aces = 0
    for card in hand:
        value = card[-1]
        if card[0] in ("As", "Ac", "Ah", "Ad"):
            aces += 1
        else:
            total += value
    for _ in range(aces):
        if total + 11 <= 21:
            total += 11
        else:
            total += 1
    if total > 21:
        check_in = False

    return total, check_in


def player_round(player_in, player_hand, deck):
    while True:
        hit = input('''
        "h" hit
        ""  pass
        ''')
        if hit == 'h':
            player_hand, player_in = draw_card(player_hand, deck, player_in)
            print('    Your hand: ' + ", ".join([f'{card[0]}' for card in player_hand]))
            if not player_in:
                break
        else:
            break
    return player_hand, player_in


def dealer_round(dealer_hand, dealer_in, deck):
    while True:
        hit_chance, dealer_in = check_hand_value(dealer_hand, dealer_in)
        if hit_chance < 15:
            print('Hit')
            dealer_hand, dealer_in = draw_card(dealer_hand, deck, dealer_in)
            print(f'  {dealer_hand[-1][0]}')
            if not dealer_in:
                break
        else:
            print("Pass")
            break
    return dealer_hand, dealer_in

def call_raise_fold(player_in, wallet):
    bet_raise = 0
    while True:
        crf_choice = input("'enter' call, 'r' raise bet, 'f' fold")
        if crf_choice == 'r':
            while True:
                bet_raise += get_bet()
                if bet_raise > wallet:
                    print(f"You don't have enough money to bet that high."
                          f" Your current balance is ${wallet}.")
                else:
                    break
        elif crf_choice == 'f':
            bet_raise = 0
            print("\nFold\n")
            player_in = False
            break
        else:
            bet_raise = 0
            break
    return bet_raise, player_in

def ranking(player_hand, dealer_hand, player_in, dealer_in, bet_pool):
    winnings = 0
    player_score, dud = check_hand_value(player_hand, player_in)
    dealer_score, dud = check_hand_value(dealer_hand, dealer_in)
    group = [
        ["You", player_score],
        ["Dealer", dealer_score]
    ]
    for player in group:
        if player[1] > 21:
            player[1] = 0
    group.sort(key = lambda x: x[1], reverse = True)
    if group[0][0] == "You":
        winnings += bet_pool * 2
    print(f'\nWinner: {group[0][0]} with {group[0][1]}')
    if group[0][0] == "You":
        print(f'Earnings: {winnings}')
    return winnings


def blackjack(wallet, deck):
    bet_pool = 0
    winnings = 0
    player_in = True
    dealer_in = True
    while True:
        if wallet < 10:
            print("\nYou don't have enough to pay entry\n")
            break
        else:
             bet_pool +=10


        player_hand = random.sample(deck, 2)
        dealer_hand = random.sample(deck, 2)
        print('    Your hand: |'+ "|".join([f'{card[0]}' for card in player_hand]) +"|")
        print(f'    Dealer: |' + "|".join([f'{dealer_hand[0][0]}']) +"|")
        if check_hand_value(player_hand, player_in) == 21 and len(player_hand) == 2:
            print('You got 21!')
            winnings += ranking(player_hand, dealer_hand,player_in, dealer_in, bet_pool)
            break
        elif check_hand_value(dealer_hand,dealer_in) == 21 and len(dealer_hand) == 2:
            print("Dealer got 21")
            winnings += ranking(player_hand, dealer_hand,player_in, dealer_in, bet_pool)
            break
        bet = get_bet()
        if bet > wallet:
            print(f"You don't have enough money to bet that high."
                  f" Your current balance is ${wallet}.")
        bet_pool += bet

        print('Your turn')
        player_hand, player_in = player_round(player_in, player_hand, deck)
        if not player_in:
            print("Your hand went over 21")
            winnings += ranking(player_hand, dealer_hand, player_in, dealer_in, bet_pool)
            break
        print("Dealer's turn")
        dealer_hand, dealer_in = dealer_round(dealer_hand,dealer_hand, deck)
        if not dealer_in:
            print('Dealer went over 21\nYou win!')
            winnings += ranking(player_hand, dealer_hand, player_in, dealer_in, bet_pool)
            break

        crf_choice, player_in = call_raise_fold(player_in, wallet)
        if not player_in :
            break
        bet_pool += crf_choice
        winnings += ranking(player_hand, dealer_hand, player_in, dealer_in, bet_pool)

        break

    return winnings - bet_pool


def blackjack_table(wallet, cards):
    deck = make_21_deck(cards)
    balance_outcome = 0
    while True:
        if wallet == 0:
            print('You have no money for blackjack right now')
            break
        print(f'\n\n\n----Wallet: ${wallet}')
        play = input("""
        ||||      ||||
       ||||||    |||||
      |||  |||  || |||
      |||  |||     |||
          |||      |||
         |||       |||
        |||        |||
       |||         |||
      ||||||||  |||||||||
      ||||||||  |||||||||
Press 'enter' to pay $10 for entry or 'm' for menu
        """)
        if play == 'm':
            break
        balance_outcome = blackjack(wallet, deck)
        wallet += balance_outcome
    return balance_outcome

#-----------------------------------------------------------------------------------------------------------------------
#                                                 SLOT MACHINE

def get_slot_machine_spins(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)
    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end = " | ")
            else:
                print(column[row], end = "")
        print()

#number of slots to play
def get_number_of_lines():
    while True:
        lines = input('How many lines would you like to bet on'
                      ' (1-'+str(MAX_LINES)+'): ')
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(f'Amount of lines must be (1-{MAX_LINES})')
        else:
            print('Please only enter a numerical amount')
    return lines

#bet amount
def get_bet():
    while True:
        bet = input("what's your bet? $")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f'Bet must be between ${MIN_BET} and ${MAX_BET}.')
        else:
            print('Please only enter a numerical amount')
    return bet

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line +1)

    return winnings, winning_lines


def spin(wallet):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > wallet:
            print(f"You don't have enough money to bet that high."
                  f" Your current balance is ${wallet}.")
        else:
            break

    print(f'You are betting ${bet} on {lines} lines.'
          f' Total bet is equal to: ${total_bet}.')

    slots = get_slot_machine_spins(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f'You won ${winnings}!')
    print(f'You won on lines: ', *winning_lines)
    return winnings - total_bet

def at_the_slots(wallet):
    balance_outcome = 0
    while True:
        if wallet == 0:
            print('You have no money for slots right now')
            break
        print(f'\n\n\n----Wallet: ${wallet}')
        play = input("\nPress 'enter' to spin or 'm' for menu.\n")
        if play == 'm':
            break
        balance_outcome = spin(wallet)
        wallet += balance_outcome
    return balance_outcome

#-----------------------------------------------------------------------------------------------------------------------
#                                                LOAN BANK

def bank_loan(wallet, loan_withdraw):
    withdrawn = 0
    repaid    = 0
    while True:
        print(f'\n\n\n----Wallet: ${wallet+loan_withdraw}')
        bank_menu = input('''
_________________________________________________
___||||||_________||_______||_____||___||___||___
___||___||_______||||______|||____||___||__||____
___||___||______||__||_____||||___||___||_||_____
___||||||______||____||____||_||__||___||||______
___||___||____||||||||||___||__||_||___||||______
___||____||___||______||___||___||||___||_||_____
___||____||___||______||___||____|||___||__||____
___|||||||____||______||___||_____||___||___||___
_________________________________________________
                    "l" - take out a loan
                    "p" - pay active loan
                    "m" - menu
                  ''')
        if bank_menu == 'l':
            withdrawn = withdraw(loan_withdraw)
            loan_withdraw += withdrawn
        elif bank_menu == 'p':
            repaid = repay(loan_withdraw)
            loan_withdraw -= repaid
        elif bank_menu == 'm':
            break

    return withdrawn - repaid

def withdraw(loan_withdraw):
    loan_amount = 0
    if loan_withdraw <= 0:
        loan_amount = input('Take out up to a grand! $')

        if loan_amount.isdigit():
            loan_amount = int(loan_amount)
            if loan_amount <= 0:
                print('loans need to be from 1 - 1000')
        else:
            print('Only enter number')
    else:
        print('You still have an active loan to pay off first')
    return loan_amount

def repay(loan_withdraw):
    debt = loan_withdraw + round(loan_withdraw * 0.17)
    print(f'Active loan remaining: ${debt}')
    repay_amount = 0
    if debt > 0:
        while True:
            repay_amount = input('Repay: $')
            if repay_amount.isdigit():
                repay_amount = int(repay_amount)
                if repay_amount <= 0:
                    print('Amount must be above 0')
                else:
                    break
            else:
                print("Only enter a numerical value")
    else:
        print("You have no active loan")
    return repay_amount

#-----------------------------------------------------------------------------------------------------------------------
#                                               MAIN MENU

def main(wallet, loan_withdraw, cards):
    while True:
        print(f'\n    Wallet: ${wallet}')
        if wallet == 0 and loan_withdraw > 0:
            print("\nYou've gone broke!!")
            print('Better luck next time\n')
            break
        title_select = input("""\n\n\n\n
    Totally Legitimate Casino
    
        s - Play Slots
        b - Play BlackJack
        l - Loan Bank
        e - Exit
        """)

        if title_select == 's':
            wallet += at_the_slots(wallet)
        elif title_select == 'l':
            loan_withdraw += bank_loan(wallet, loan_withdraw)
            wallet += loan_withdraw
        elif title_select == 'b':
            wallet += blackjack_table(wallet, cards)
        elif title_select == 'e':
            break
    print(f'You leave with ${wallet}')

#-----------------------------------------------------------------------------------------------------------------------
#                                              MAIN PROGRAM

#players starting bank balance
def deposit():
    while True:
        given_deposit = input('Enter starting balance: $')
        if given_deposit.isdigit():
            amount = int(given_deposit)
            if amount <= 0:
                print('Balance must be greater than 0')
            else:
                break
        else:
            print('Please only enter a numerical amount')
    return amount


def over_world(cards):
    #wallet = deposit()
    user = login()
    wallet = user[1]
    loan_withdraw = 0
    main(wallet, loan_withdraw, cards)

#-----------------------------------------------------------------------------------------------------------------------
#                                               LOGIN
def save_user(users, filename="users.txt"):
    with open(filename, "w") as file:
        for user in users:
            file.write(user + '\n')

def load_user(filename="users.txt"):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def new_user(all_users):
    while True:
        in_use = False
        entry = input("""\n
                   Create a password
    }""")
        for user in all_users:
            if entry == user:
                print("\nPassword not strong enough")
                in_use = True
        if not in_use:
            break
    all_users.append(entry)
    save_user(all_users)
    return all_users, entry



def login():
    valid = False
    while True:
#getting user list & asking for user data
        all_users = load_user()
        entry = input('''
            Enter "new" to create an account
                           or
                     Enter password
    }''')
#adding new user
        if entry == 'new':
            all_users, entry = new_user(all_users)

#checking if existing user
        for users in all_users:
            if entry in users:
                print('welcome')
                valid = True
#restart if nonexistent
        if valid:
            break
        else:
            print("\n\n\nInvalid\n\n")

    user = f"{entry}.txt"
    return user


over_world(cards)