from game_classes import *

suit_tp = ("diamonds", "clubs", "hearts", "spades")
rank_tp = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

#dictionary used when i calculate prize based on game scenario
win_rate = {'black jack': 2.5, 'by score': 2, 'dealer bust': 2, 'draw': 1}

print("Welcome to Black Jack game!\n")
print("Rules are simple:\n1.Approach value 21 as much as you can\n2.Beat the dealer\n3.Don`t super value 21!\n")

print("Are you ready to start ?\n")

input_right = False
while not input_right:
    ans = input("Yes or no?: ")

    if ans.lower() in ('yes', 'no'):
        input_right = True
    else:
        print("Answer is not clear. Please repeat again\n")
    
if ans == 'yes':

    print("\nHow many players are going to play ?")

    input_right = False
    while not input_right:
        try:
            num_pl = int(input('#players: '))
        except TypeError:
            print('\nIt must be a digit. Try again')
        else:
            input_right = True
    
    members = []
    #Create num_pl players
    for n in range(num_pl):
        
        print(f'\nPlease, insert the name and the balance of a player {n+1}')
        
        #Create instance of player

        input_right = False
        while not input_right:
            try:
                members.append(Player(input('Name: '), int(input('Balance:'))))
            except:
                print('\nBalance must be a digit. Try again')
            else:
                input_right = True
    
    #create instance of dealer
    dealer = Dealer()

    #generate cards
    for suit in suit_tp:
        for rank in rank_tp:
            card = Card(suit, rank)
            dealer.fill_stack(card)

    print("\nPrepare, we start the round!")

    game_on = True
    bet = 10
    
    for member in members:
        print(f"\n{member.name}\nBet amount is {bet}\nCurrent balance is {member.balance}\nDo you want to play ?")

        input_right = False
        while not input_right:
            ans = input("Type yes or no?: ")

            if ans.lower() in ('yes', 'no'):
                input_right = True
            else:
                print("\nAnswer wasn`t clear. Please, repeat")

        if ans.lower() == 'yes':
            member.stay = False
        else:
            member.to_stay()
    
    #check if game continues
    game_on = False
    for member in members:

        #if at least one player decided to play
        if not member.stay:
            game_on = True
    
    #game continues untill there`s some players playing in game 
    while game_on and members:

        dealer.stay = False

        #shuffle the stack
        dealer.shuffle()

        #players who decided to play place a bet
        for member in members:
            if not member.stay:
                try:
                    member.place(bet)
                except Exception as err:
                    
                    #if there`s not enough money on a balance
                    if err.args[0] == 'Exhausted balance':

                        print(f"{member.name} your money are not enough. Do you want to fill your balance?")

                        input_right = False
                        while not input_right:
                            ans = input("Type yes or no?: ")

                            if ans.lower() in ('yes', 'no'):
                                input_right = True
                            else:
                                print("\nAnswer wasn`t clear. Please, repeat")

                        if ans.lower() == 'yes':

                            print("Type the wanted credit")
                            
                            input_right = False
                            while not input_right:
                                try:
                                    credit = int(input("Type here:"))
                                except:
                                    print("It wasn`t a digit. Try again")
                                else:
                                    input_right = True
                                    member.earn(credit)
                                    member.place(bet)
                        else:
                            members.remove(member)

                finally:
                    dealer.earn(bet)

        #adds to member`s hand the last card from dealer stack
        for n in range(2):
            for member in members:
                if not member.stay:
                    member.hit(dealer.deal())

                    #calculate all possible combination
                    member.calc()

        #adds to dealer`s hand 2 cards, last one facedown
        dealer.hit(dealer.deal())
        dealer.hit(dealer.deal(faceup = False))
        dealer.calc()
        
        #print cards of each player
        for member in members:

            if member.hand:
                print(f"\n{member.name}")

                for card in member.hand:
                
                    #show only faceup cards
                    if card.faceup:
                        print(card)

                print(f"Score is {member.comb_cost['min']} ({member.comb_cost['max']})")
            else:
                print(f"\n{member.name} is out of the game")

        #print dealer`s shown card
        print(f"\nDealer {dealer.name}")
        print(dealer.hand[0])
        print(f"Score is {dealer.comb_cost['min']} ({dealer.comb_cost['max']})")

        #check if someone has a blackjack
        for member in members:

            if 21 in member.comb_cost:
                print("\n" + member.name + " has a backjack!")
                prize = bet*win_rate['black jack']

                member.earn(prize)
                dealer.pay(prize)

                #Member cannot play any more and empties his hand
                for card in member.empty_hand():
                    #cards are passed to dealers stack
                    dealer.fill_stack(card)

        #read player`s decision and start the round
        for member in members:

            #Asking only those players that decided to continue 
            #Ask player untill he stays
            while not member.stay:
                #dictionary used when i prompt the choice from a player
                options = {'hit': 1, 'stay': 2}

                print(f"\n{member.name}\nCurrent balance: {member.balance}\nYour hand is:")

                for card in member.hand:
                    
                    #show only faceup cards
                    if card.faceup:
                        print(card)
                    
                print(f"\nYour score is {member.comb_cost['min']} ({member.comb_cost['max']})")

                #if player able to split i add a new option for his move
                if (not member.split) and (member.hand[0].rank == member.hand[1].rank):
                    #create a new option
                    options['split'] = 3

                print(f"{member.name}, do you want to ", end = '')
                print(*options, sep = ' or ', end = " ?\n")
                    
                input_right = False
                while not input_right:
                    try:
                        for option in options:
                            print(f"To {option} type {options[option]}", end = ' ')

                        ans = int(input())
                        
                        if not (ans in options.values()):
                            raise ValueError
                    except:
                        print("Input wasn`t a digit or a digit was wrong. Try again!")
                    else:
                        input_right = True
                
                #player decided to hit
                if ans == 1:
                    member.hit(dealer.deal())
                    member.calc()

                    #if player busts
                    #must consider the minimal possible cost
                    if member.comb_cost['min'] > 21:
                        print(f"\n{member.name}\nYour score is {member.comb_cost['min']}, ({member.comb_cost['max']})")
                        
                        for card in member.bust():
                            print(card)
                            dealer.fill_stack(card)
                
                #player decided to stay
                elif ans == 2:
                    member.to_stay()
                
                #player decided to split
                elif ans == 3:
                    #make a player place a bet due to the fact that he splitted
                    member.place(bet)
                    member.split = True

                    indx = members.index(member)

                    #insert splitted player right after original player
                    members.insert(indx+1, SplitPlayer(member))

                    #add one more card to original player
                    member.hit(dealer.deal())
                    member.calc()

                    #add one more card to split player
                    members[indx+1].hit(dealer.deal())
                    members[indx+1].calc()

        #Turn up last dealers card
        dealer.hand[-1].faceup = True
        dealer.calc()

        print(f"\n{dealer.name}:")
        for card in dealer.hand:
            print(card)

        print(f"Score is {dealer.comb_cost['min']} ({dealer.comb_cost['max']})")

        #additional hits for dealer
        while dealer.comb_cost['max'] < 17:

            dealer.hit(dealer.deal())
            dealer.calc()

            print(f"\n{dealer.name}:")
            for card in dealer.hand:
                print(card)

            print(f"Score is {dealer.comb_cost['min']} ({dealer.comb_cost['max']})")
        
        #dealer busted, each player takes twice his bet
        if dealer.comb_cost['min'] > 21:
            print("\nDealer busts! Each player takes twice his bet")
            for card in dealer.bust():
                dealer.fill_stack(card)

            for member in members:

                #win only those who didn`t busted or winned with blackjack (they haven`t emptied their hands)
                if member.hand:
                    prize = bet*win_rate['dealer bust']
                    try:
                        dealer.pay(prize)
                    except ValueError as err:
                        if err.args[0] == "Low balance":
                            print('Dealer has not enouhg money to pay you. Dealer fills his balance!')
                            dealer.earn(1000)
                            dealer.pay(prize)
                    finally:
                        member.earn(prize)

        # define who is winner
        else:
            #suppose that dealer wins
            win_lst = {'max': dealer.comb_cost['max'], 'winners': [dealer]}

            for member in members:

                #chose only those who haven`t emptied their hand yet
                if member.hand:
                    
                    #player has greater hand value
                    if member.comb_cost['max'] > win_lst['max']:
                        win_lst['max'] = member.comb_cost['max']
                        win_lst['winners'] = [member]
                    
                    #player has exact same value, so he makes part of round winners
                    elif member.comb_cost['max'] == win_lst['max']:
                        win_lst['winners'].append(member)

            print("\nWinners of this round are:\n")
            for winner in win_lst['winners']:

                if winner is not dealer:
                    #There are more than one winner so it`s a draw
                    if len(win_lst['winners']) > 1:
                        prize = bet*win_rate['draw']
                        print("There`s a draw. Nobody won. Players return their bet\n")
                    #Only one winner wins by score
                    else:
                        print(f"\n{winner.name} won with score {winner.comb_cost['max']}\n")
                        prize = bet*win_rate['by score']

                    try:
                        dealer.pay(prize)
                    except ValueError as err:
                        if err.args[0] == "Low balance":
                            print('Dealer has not enough money to pay you. Dealer fills his balance!')
                            dealer.earn(1000)
                            dealer.pay(prize)
                    finally:
                        winner.earn(prize)
                    

        #resetting players and dealer`s hands
        for member in members:
            for card in member.empty_hand():
                dealer.fill_stack(card)

            if type(member) is SplitPlayer:
                #remove split player
                members.remove(member)
        
        for card in dealer.empty_hand():
                dealer.fill_stack(card)

        clear = " "*100
        print(clear)
        
        for member in members:
            print(f"\n{member.name}\nBet amount is {bet}\nYour balance is {member.balance}\nDo you want to play ?")

            input_right = False
            while not input_right:
                ans = input("Type yes or no?: ")

                if ans.lower() in ('yes', 'no'):
                    input_right = True
                else:
                    print("\nAnswer wasn`t clear. Please, repeat")

            if ans.lower() == 'yes':
                member.stay = False
            else:
                member.to_stay()
        
        #check if game continues
        game_on = False
        for member in members:
            #if at least one player decided to play
            if not member.stay:
                game_on = True

    print("Goodbye and come soon!")
else:
    print('Goodbye')
