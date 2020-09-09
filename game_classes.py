from random import shuffle

values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

#Each card has suit, rank and value

class Card():
    
    def __init__(self, suit, rank, faceup = True):
        '''Accept suit, rank and faceup attribute which is True by default'''

        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        self.faceup = faceup

    def __str__(self):
        return self.rank + " of " + self.suit

class Player():

    def __init__(self, name, balance):
        '''Creates player given name and money balance'''

        self.name = name
        self.balance = balance
        self.hand = []

        #comb_cost is a dict, containing min and max values possible with given combination
        self.comb_cost = {'min': 0, 'max': 0}
        self.stay = False

        #becomes true either when player splitted or when insstance is of type SplitPlayer that cannot split
        self.split = False

        if type(self) is Player:
            print("\nPlayer was created!")
        elif type(self) is Dealer:
            print("\nDealer was created!")
        elif type(self) is SplitPlayer:
            print(f"\n{self.name} splitted his cards")

    def place(self, bet):
        '''Subtracts bet amount from balance. Bet must be positive and not greater than balance'''

        if bet < 0:
            raise Exception("Negative bet")

        elif bet > self.balance:
            raise Exception("Exhausted balance")

        else:
            self.balance -= bet
            print(f"\nPlayer {self.name} placed {bet}")
    
    def earn(self, profit):
        '''Increases player`s or dealer`s balance'''

        if profit < 0:
            raise ValueError("Profit can`t be negative")

        else:
            self.balance += profit
            print(f"\n{self.name} received {profit}")

    def hit(self, card):
        '''Adds card to player`s or dealer`s hand and updates value'''

        if type(card) is not Card:
            raise TypeError("Method accepts cards only")

        elif not self.stay:
            print(f"\n{self.name} hits!")
            self.hand.append(card)

        else:
            raise Exception("Player decided to stay. It is not possibe to hit any more")

    def calc(self):
        '''Calculates possible values for player`s hand'''
        #Shown cards are only those that have faceup attribute equal True
        shown_cards = [c for c in self.hand if c.faceup]
        
        #Calculate first possible value that combination can assume
        #The value that considers Ace as a 1
        val = 0
        for c in shown_cards:
            val += c.value

        self.comb_cost['min'] = val

        #Calculate another possible value only if there is an Ace in combination and future value doesn`t super 21
        for c in shown_cards:

            if c.rank == 'A' and val + 10 <= 21:
                val += 10

            self.comb_cost['max'] = val
            

    def to_stay(self):
        '''Player or Dealer cannot hit anymore.Changes attribute stay to True'''
        print(f"\n{self.name} stays!")
        self.stay = True

    def empty_hand(self):
        '''Player`s hand gets cleared and value reset to 0. Stay attribute assumes True. Returns player`s hand'''
        self.comb_cost = {'min': 0, 'max': 0}
        self.stay = True
        return [self.hand.pop() for _ in range(len(self.hand))]

    def bust(self):
        '''Player`s or Dealer`s value super 21. His hand gets cleared and value reset to 0. Stay attribute assumes True. Returns player`s hand'''
        print(f"\n{self.name} busted!")
        return self.empty_hand()

    def __del__(self):
        print(f"\n{self.name} left the game")
    
        
class SplitPlayer(Player):

    def __init__(self, origin):
        '''Creates Instance of split player controlled by original player given it`s instance'''
        Player.__init__(self, origin.name, origin.balance)
        self.origin = origin

        #displace one card from original player
        self.hit(origin.hand.pop())
        self.calc()

        self.split = True

    def place(self, bet):
        '''Subtracts bet amount from balance. Bet must be positive and not greater than balance'''

        if bet < 0:
            raise ValueError("Bet cannot be negative")

        elif bet > self.balance:
            raise ValueError("You don`t have enough money on your balance")

        else:
            #make sure that two balances are equal
            self.balance = self.origin.balance
            self.balance -= bet

            #original player`s balance gets updated
            self.origin.balance = self.balance
            print(f"\nPlayer {self.name} placed {bet}")
    
    def earn(self, profit):
        '''Increases player`s or dealer`s balance'''

        if profit < 0:
            raise ValueError("Profit can`t be negative")

        else:
            #make sure that two balances are equal
            self.balance = self.origin.balance
            self.balance += profit

            #original player receives profit as well
            self.origin.balance = self.balance
            print(f"\n{self.name} received {profit}")

    def __del__(self):
        self.origin.split = False
        print(f"\nSplit player from {self.name} was deleted succesfully!")

class Dealer(Player):
    stack = []

    def __init__(self, name = 'dealer', balance = 1000):
        '''Creates dealer which is particular case of player class'''
        Player.__init__(self, name, balance)

    def place(self):
        '''Dealer doesn`t support place attribute'''
        pass

    def pay(self, amount):
        '''Subtracts amount of money from dealer`s bank so as to pay winner a loot'''

        if amount < 0:
            raise ValueError("Negative amount")
        elif amount > self.balance:
            raise ValueError("Low balance")
        else:
            print(f"\n{self.name} pays {amount}!")
            self.balance -= amount

    def shuffle(self):
        '''Shuffles stack of cards'''
        print("\nDealer shuffles the stack!")
        shuffle(self.stack)
    
    def deal(self, faceup = True):
        '''Returns last card from the stack faceup or facedown'''
        card = self.stack.pop()
        card.faceup = faceup
        return card

    def fill_stack(self, card):
        '''Adds one card to the stack'''
        if type(card) is not Card:
            raise TypeError('Method accepts card only')
        else:
            self.stack.append(card)
