#Black Jack
import sys
import random
#Rules:
blackjack = 1.5 #3:2 or 6:5 #works
decks = 1 #1, 2, 4, 6, 8 #works
peek10 = True #dealer peeks when his up card is 10 #works

times = int(input("How many times do you want to play?"))
new_balence = float(input("How much money do you have?")) 
print("bal: "+str(new_balence))
# Deck Creation

shoe = []
for i in range(1,10):
    for j in range(0,(4*decks)):
        shoe.append(i)
for i in range(10,14):
    for j in range(0,(4*decks)):
        shoe.append(10)
shuffle = shoe
print("")
print("")


def hand(balence):
    
    while True:
        bet = int(input("How much do you want to bet?"))
        if bet > balence or bet < 0:
            print("You cannot bet over your balence or lower than 1")
        else:
            break
    balence = balence - bet
    
    # Deal
    
    one_card = random.choice(shoe)
    shoe.pop(one_card)
    down_card = random.choice(shoe)
    shoe.pop(down_card)
    two_card = random.choice(shoe)
    shoe.pop(two_card)
    up_card = random.choice(shoe)
    shoe.pop(up_card)
    player_hand = [one_card,two_card] 
    dealer_hand = [up_card,down_card]
    player_aces = 0
    dealer_aces = 0
    player_hands = 1
    player_side = [[],[],[],[]] #Needed for splits, most of the game they will be empty spots
    splits = 0 #tracking of splits
    for i in range(2):
        if player_hand[i] == 1:
            player_aces += 1
        if dealer_hand[i] == 1:
            dealer_aces += 1

    print("Dealer has "+str(dealer_hand[1]))
    print("You have "+str(player_hand[0])+", "+str(player_hand[1]))
    
    # player blackjack
    if player_aces == 1:
        if player_hand[0] + player_hand[1] == 11:
            print("Black Jack!")
            balence = balence + bet*2.5
            return balence

    # dealer blackjack
    if dealer_hand[1] == 1:
        insurance = input("Do you want insurance (yes/no)?")
        if dealer_hand[0] == 10:
            print("Dealer has Blackjack")
            if insurance == "yes":
                balence = balence + bet
            return balence
        else:
            print("Dealer doesn't have Blackjack")
            if insurance == "yes":
                balence = balence - (bet/2)
    if peek10 == True:
        if dealer_hand[0] == 10:
            if dealer_hand[1] == 1:
                return balence

    #player choice
    current_hands = 0
    player_side[0] = player_hand
    print(player_side[0])
    for i in range(4):
        while True:
            if len(player_side[i]) > 1:
                print("Your hand" + str(player_side[i]))
                choice = input("(hit, stand, double, split)?: ")
                if choice == "double" and len(player_hand) > 2:
                    bet = bet
                elif choice == "hit" or choice == "double":
                    if choice == "double" and balence > bet:
                        balence = balence - bet
                        bet = bet*2
                    new_card = random.choice(shoe)
                    player_side[i].append(new_card)
                    shoe.pop(new_card)
                    print("You drawn "+str(player_side[i][-1]))
                    if player_aces > 0 and sum(player_side[i]) <= 11:
                        print("Your hand is: "+str(sum(player_side[i])+10))
                    else:
                        print("Your hand is: "+str(sum(player_side[i])))
                    if sum(player_side[i]) > 21:
                        print("You bust")
                        player_side[i] = [0,0]
                        break
                    if choice == "double":
                        break
                elif choice == "stand":
                    print("You stand.")
                    break
                elif choice == "split":
                    if player_side[i][0] == player_side[i][1] and balence >= bet:
                        balence = balence - bet
                        player_side[i+2-splits].append(player_side[i][1]) 
                        new_card = random.choice(shoe)
                        player_side[i][1] = new_card
                        print(player_side[i])
                        shoe.pop(new_card)
                        new_card = random.choice(shoe)
                        player_side[i+2-splits].append(new_card)
                        print(player_side[i+2-splits])
                        shoe.pop(new_card)
                        split += 1
                    else:
                        bet = bet
            else:
                break
                            
                            

    # dealer choice
    dealer_bust = False
    dealer_value = sum(dealer_hand)
    print("Dealer has "+str(sum(dealer_hand)))
    while True:
        dealer_value = sum(dealer_hand) #Value including aces to make choices. Needed due to S17 vs H17 rules.
        if dealer_aces > 0 and (sum(dealer_hand)+10) < 21:
            dealer_value = (sum(dealer_hand)+10)
            
        if dealer_value < 17: #hit
            new_card = random.choice(shoe)
            dealer_hand.append(new_card)
            shoe.pop(new_card)
            print("Dealer drawn "+str(dealer_hand[-1]))
            if dealer_hand[-1] == 1:
                dealer_aces += 1
            if (dealer_value + dealer_hand[-1] - (dealer_aces*10)) > 21:
                print("Dealer bust!")
                balence = balence + bet*2
                dealer_bust = True
                break
        if sum(dealer_hand) >= 17: #stand
            print("Dealer stands")
            break
            
            
    #who wins?

    for i in range(4):
        if len(player_side[i]) > 1:
            if dealer_aces > 0 and sum(dealer_hand[i]) <= 11:
                dealer_hand.append(10)
            if player_aces > 0 and sum(player_hand) <= 11:
                player_hand.append(10)
            if dealer_bust == False:
                if sum(player_side[i]) > sum(dealer_hand):
                    balence = balence + bet*2
                elif sum(player_side[i]) == sum(dealer_hand):
                    balence = balence + bet
            elif dealer_bust == True:
                if sum(player_side[i]) > 2:
                    balence = balence + bet
    return balence
            
            
            
for i in range(1,times+1):
    new_balence = hand(new_balence)
    print("You now have "+str(new_balence)+" dollars")
    print("")
    print("")
    if i % 7== 0:
        print("Shuffling")
        shoe = shuffle
    if new_balence == 0:
        print("You have no money. Game Over.")
        sys.exit()
