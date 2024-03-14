import random
import time
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

start_time = time.time()


def check_for_ace(cards, total):
    if 11 in cards and total > 21:
        ace_index = cards.index(11)
        cards[ace_index] = 1

    return cards


def check_for_push(player_total, dealer_total):
    return player_total == dealer_total


def check_for_blackjack(hand, total):
    return len(hand) == 2 and total == 21


def reshuffle(deck, deck_count):

    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * (4 * deck_count)
    l = len(deck)
    random.shuffle(deck)
    cutting_card = random.randrange(int(0.45 * l), int(0.55 * l))
    return cutting_card,deck


def simulate_blackjack1(deck_count, num_simulations):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * (4 * deck_count)
    cutting_card = random.randrange(int(0.45 * len(deck)), int(0.55 * len(deck)))
    print(cutting_card)
    random.shuffle(deck)

    win_probabilities = []
    moneyrecord=[]
    wins = 0
    losses = 0
    pushes = 0
    actual_sims = 0
    money = 0

    with tqdm(total=num_simulations, ncols=80,
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [Time elapsed: {elapsed}, Time remaining: {remaining}, '
                         '{rate_fmt}{postfix}]',
              unit='hands', dynamic_ncols=True) as pbar:
        while actual_sims < sims:

            player_hand = [deck.pop(), deck.pop()]
            player_total = sum(player_hand)
            player_hand = check_for_ace(player_hand, player_total)
            player_total2 = 0
            player_hand2=0
            double = 0
            split = 0
            dealer_hand = [deck.pop(), deck.pop()]
            dealer_total = sum(dealer_hand)

            #print("-----")
            #print("Player's Hand:", player_hand)
            #print("Dealer's Hand:", [dealer_hand[0], "?"])

            if check_for_blackjack(dealer_hand, dealer_total):
                if check_for_blackjack(player_hand, player_total):
                    #print("Dealer's hand : [11, 10] \nBoth the player and the dealer have blackjack. Push(tie)")
                    pushes += 1
                    if len(deck) <= cutting_card:
                        cutting_card,deck = reshuffle(deck, deck_count)
                    continue
                else:
                    #print("Dealer's hand : [11, 10] \nDealer has blackjack. Player loses")
                    losses += 1
                    money -= 5
                    if len(deck) <= cutting_card:
                        cutting_card,deck = reshuffle(deck, deck_count)
                    continue

            if check_for_blackjack(player_hand, player_total):
                #print("Player has blackjack. Player wins")
                wins += 1
                money += 7.5
                if len(deck) <= cutting_card:
                    cutting_card,deck = reshuffle(deck, deck_count)
                continue
            if player_total == 12 and (player_hand[0] == 1 or player_hand[1] == 1):
                #print("split aces")
                split = 1
                player_hand = [11, deck.pop()]
                player_hand2 = [11, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 9 and (2 <= dealer_hand[0] <= 6 or 8 <= dealer_hand[0] <= 9):
                #print("split nines")
                split = 1
                player_hand = [9, deck.pop()]
                player_hand2 = [9, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 8:
                #print("split eights")
                split = 1
                player_hand = [8, deck.pop()]
                player_hand2 = [8, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 7 and dealer_hand[0] <= 7:
                #print("split sevens")
                split = 1
                player_hand = [7, deck.pop()]
                player_hand2 = [7, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 6 and dealer_hand[0] <= 6:
                #print("split sixs")
                split = 1
                player_hand = [6, deck.pop()]
                player_hand2 = [6, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 4 and (dealer_hand[0] == 5 or dealer_hand[0] == 6):
                #print("split fours")
                split = 1
                player_hand = [4, deck.pop()]
                player_hand2 = [4, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 3 and dealer_hand[0] <= 7:
                #print("split threes")
                split = 1
                player_hand = [3, deck.pop()]
                player_hand2 = [3, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 2 and dealer_hand[0] <= 7:
                #print("split twos")
                split = 1
                player_hand = [2, deck.pop()]
                player_hand2 = [2, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)

            while player_total < 21:
                if 11 in player_hand:
                    if player_total == 20:
                        #print("Player stands")
                        break
                    elif player_total == 19:
                        if dealer_hand[0] == 6 and len(player_hand)==2:
                            #print("Player doubles")
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1

                            break
                        else:
                            #print("Player stands")
                            break
                    elif player_total == 18:
                        if 2 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            #print("Player doubles")
                            player_hand.append(deck.pop())
                            player_total=sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        elif 9 <= dealer_hand[0] <= 11:
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                        else:
                            #print("Player stands")
                            break
                    elif player_total == 17:
                        if 3 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            #print("Player doubles")
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                    elif player_total == 16:
                        if 4 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            #print("Player doubles")
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                    elif player_total == 15:
                        if 4 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            #print("Player doubles")
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                    elif player_total == 14:
                        if 5 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            #print("Player doubles")
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                    elif player_total == 13:
                        if 5 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            #print("Player doubles")
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                else:
                    if player_total >= 17:
                        #print("Player stands")
                        break
                    elif player_total == 16 and 2 <= dealer_hand[0] <= 6:
                        #print("Player stands")
                        break
                    elif player_total == 15 and 2 <= dealer_hand[0] <= 6:
                        #print("Player stands")
                        break
                    elif player_total == 14 and 2 <= dealer_hand[0] <= 6:
                        #print("Player stands")
                        break
                    elif player_total == 13 and 2 <= dealer_hand[0] <= 6:
                        #print("Player stands")
                        break
                    elif player_total == 12 and 4 <= dealer_hand[0] <= 6:
                        #print("Player stands")
                        break
                    elif player_total == 11 and len(player_hand)==2:
                        #print("Player doubles")
                        player_hand.append(deck.pop())
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 10 and 2 <= dealer_hand[0] <= 9 and len(player_hand)==2:
                        #print("Player doubles")
                        player_hand.append(deck.pop())
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 9 and 3 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                        #print("Player doubles")
                        player_hand.append(deck.pop())
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    else:
                        player_hand.append(deck.pop())
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        #print("Player hits. New Hand:", player_hand)
            if split == 1:
                while player_total2 < 21:
                    if 11 in player_hand2:
                        if player_total2 == 20:
                            #print("Player stands")
                            break
                        elif player_total2 == 19:
                            if dealer_hand[0] == 6 and len(player_hand2)==2:
                                #print("Player doubles")
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                double = 1

                                break
                            else:
                                #print("Player stands")
                                break
                        elif player_total2 == 18:
                            if 2 <= dealer_hand[0] <= 6 and len(player_hand2)==2:
                                #print("Player doubles")
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                double = 1
                                break
                            elif 9 <= dealer_hand[0] <= 11:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                            else:
                                #print("Player stands")
                                break
                        elif player_total2 == 17:
                            if 3 <= dealer_hand[0] <= 6 and len(player_hand2)==2:
                                #print("Player doubles")
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 16:
                            if 4 <= dealer_hand[0] <= 6 and len(player_hand2)==2:
                                #print("Player doubles")
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 15:
                            if 4 <= dealer_hand[0] <= 6 and len(player_hand2)==2:
                                #print("Player doubles")
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 14:
                            if 5 <= dealer_hand[0] <= 6 and len(player_hand2)==2:
                                #print("Player doubles")
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 13:
                            if 5 <= dealer_hand[0] <= 6 and len(player_hand2)==2:
                                #print("Player doubles")
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                    else:
                        if player_total2 >= 17:
                            #print("Player stands")
                            break
                        elif player_total2 == 16 and 2 <= dealer_hand[0] <= 6:
                            #print("Player stands")
                            break
                        elif player_total2 == 15 and 2 <= dealer_hand[0] <= 6:
                            #print("Player stands")
                            break
                        elif player_total2 == 14 and 2 <= dealer_hand[0] <= 6:
                            #print("Player stands")
                            break
                        elif player_total2 == 13 and 2 <= dealer_hand[0] <= 6:
                            #print("Player stands")
                            break
                        elif player_total2 == 12 and 4 <= dealer_hand[0] <= 6:
                            #print("Player stands")
                            break
                        elif player_total2 == 11 and len(player_hand2)==2:
                            #print("Player doubles")
                            player_hand2.append(deck.pop())
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            double = 1
                            break
                        elif player_total2 == 10 and 2 <= dealer_hand[0] <= 9 and len(player_hand2)==2:
                            #print("Player doubles")
                            player_hand2.append(deck.pop())
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            double = 1
                            break
                        elif player_total2 == 9 and 3 <= dealer_hand[0] <= 6 and len(player_hand2)==2:
                            #print("Player doubles")
                            player_hand2.append(deck.pop())
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            double = 1
                            break
                        else:
                            player_hand2.append(deck.pop())
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            #print("Player hits. New Hand:", player_hand)
            #print("Player's Hand:", player_hand)
            #if split==1:
                #print("Player's Hand 2: ", player_hand2)

            if player_total <= 21 or (player_total2 <= 21 and split==1):
                while dealer_total < 17:
                    dealer_hand.append(deck.pop())
                    dealer_total = sum(dealer_hand)
                    if dealer_total > 21 and 11 in dealer_hand:
                        dealer_hand = check_for_ace(dealer_hand, dealer_total)
                        dealer_total = sum(dealer_hand)

            #print("Dealer's Hand:", dealer_hand)

            actual_sims += 1

            if player_total > 21 or (21 >= dealer_total > player_total):
                #print("Player loses")
                losses += 1
                if double == 1:
                    money -= 10
                else:
                    money -= 5
            elif check_for_push(player_total, dealer_total):
                #print("Push (Tie)")
                pushes += 1
            else:
                #print("Player wins")
                wins += 1
                if double == 1:
                    money += 10
                else:
                    money += 5
            if split == 1:
                if player_total2 > 21 or (21 >= dealer_total > player_total2):
                    #print("Player loses")
                    losses += 1
                    if double == 1:
                        money -= 10
                    else:
                        money -= 5
                elif check_for_push(player_total2, dealer_total):
                    #print("Push (Tie)")
                    pushes += 1
                else:
                    #print("Player wins")
                    wins += 1
                    if double == 1:
                        money += 10
                    else:
                        money += 5

            if len(deck) <= cutting_card:
                cutting_card,deck = reshuffle(deck, deck_count)
            win_probabilities.append(wins / actual_sims)
            moneyrecord.append(money)
            pbar.update(1)

        pbar.update(num_simulations - pbar.n)

    return win_probabilities, wins, losses, pushes, money,moneyrecord


def simulate_blackjack2(deck_count, num_simulations):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * (4 * deck_count)
    cutting_card = random.randrange(int(0.45 * len(deck)), int(0.55 * len(deck)))
    random.shuffle(deck)
    moneyrecord2=[]
    win_probabilities = []
    wins = 0
    losses = 0
    pushes = 0
    actual_sims = 0
    money = 0
    bet_unit = 5
    count = 0

    with tqdm(total=num_simulations, ncols=80,
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [Time elapsed: {elapsed}, Time remaining: {remaining}, '
                         '{rate_fmt}{postfix}]',
              unit='hands', dynamic_ncols=True) as pbar:
        while actual_sims < sims:
            insurance = 0
            player_hand = [deck.pop(), deck.pop()]
            # print("Initial Player hand: ",player_hand)
            if player_hand[0] < 7:
                count += 1
            elif player_hand[0] > 9:
                count -= 1
            if player_hand[1] < 7:
                count += 1
            elif player_hand[1] > 9:
                count -= 1
            player_total = sum(player_hand)
            player_hand = check_for_ace(player_hand, player_total)
            double = 0
            dealer_hand = [deck.pop(), deck.pop()]
            # print("Dealer hand: ", dealer_hand)
            if dealer_hand[0] < 7:
                count += 1
            elif dealer_hand[0] > 9:
                count -= 1
            dealer_total = sum(dealer_hand)
            true_count = count / (len(deck) / 52)
            bet_size = (true_count - 1) * bet_unit * 2
            if bet_size <= 0:
                bet_size = 1

                # print("-----")
                # print("Player's Hand:", player_hand)
                # print("Dealer's Hand:", [dealer_hand[0], "?"])
            if dealer_hand[0] == 11 and check_for_blackjack(player_hand, player_total) == 0:
                if true_count > 3:
                    insurance = 1
                    bet_size += bet_size / 2

            if check_for_blackjack(dealer_hand, dealer_total):

                if check_for_blackjack(player_hand, player_total):
                    # print("Dealer's hand : [11, 10] \nBoth the player and the dealer have blackjack. Push(tie)")
                    pushes += 1
                    count -= 1
                    if len(deck) <= cutting_card:
                        cutting_card,deck = reshuffle(deck, deck_count)
                        count = 0
                    continue

                if insurance == 1:
                    pushes += 1
                    count -= 1
                    if len(deck) <= cutting_card:
                        cutting_card,deck = reshuffle(deck, deck_count)
                        count = 0
                    continue
                else:
                    # print("Dealer's hand : [11, 10] \nDealer has blackjack. Player loses")
                    losses += 1
                    count -= 1
                    money -= bet_size
                    if len(deck) <= cutting_card:
                        cutting_card,deck = reshuffle(deck, deck_count)
                        count = 0
                    continue

            if check_for_blackjack(player_hand, player_total):
                # print("Player has blackjack. Player wins")
                wins += 1
                if dealer_hand[1] < 7:
                    count += 1
                elif dealer_hand[1] > 9:
                    count -= 1
                money += bet_size * 1.5
                if len(deck) <= cutting_card:
                    cutting_card,deck = reshuffle(deck, deck_count)
                    count = 0
                continue

            while player_total < 21:
                # print("Player hand: ",player_hand)
                # print("Dealer hand: ",dealer_hand)
                # print("True count: ",true_count)

                if 11 in player_hand:
                    if player_total == 20:
                        # print("Player stands")
                        break
                    elif player_total == 19:
                        if true_count > 2 and dealer_hand[0] == 4:
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                        elif true_count > 0 and (dealer_hand[0] == 5 or dealer_hand[0] == 6):
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)

                        elif dealer_hand[0] == 6 and len(player_hand)==2:
                            # print("Player doubles")
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            # print("Player stands")
                            break
                    elif player_total == 18:
                        if 2 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            # print("Player doubles")
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        elif 9 <= dealer_hand[0] <= 11:
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                        else:
                            # print("Player stands")
                            break
                    elif player_total == 17:
                        if true_count > 0 and dealer_hand[0] == 2:
                            break
                        elif 3 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            # print("Player doubles")
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                    elif player_total == 16:
                        if 4 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            # print("Player doubles")
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                    elif player_total == 15:
                        if 4 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            # print("Player doubles")
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)

                    elif player_total == 14:
                        if 5 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            # print("Player doubles")
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                    elif player_total == 13:
                        if 5 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                            # print("Player doubles")
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1
                            break
                        else:
                            player_hand.append(deck.pop())
                            if (player_hand[len(player_hand) - 1]) < 7:
                                count += 1
                            elif (player_hand[len(player_hand) - 1]) > 9:
                                count -= 1
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)

                else:
                    if player_total >= 17:
                        # print("Player stands")
                        break
                    elif player_total == 16 and true_count > -1 and dealer_hand[0] == 10:
                        break
                    elif player_total == 16 and true_count > 3 and dealer_hand[0] == 9:
                        break
                    elif player_total == 15 and true_count > 3 and dealer_hand[0] == 10:
                        break
                    elif player_total == 13 and true_count < 0 and dealer_hand[0] == 2:
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                    elif player_total == 12 and true_count > 2 and dealer_hand[0] == 2:
                        break
                    elif player_total == 12 and true_count > 1 and dealer_hand[0] == 3:
                        break
                    elif player_total == 12 and true_count < 0 and dealer_hand[0] == 4:
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                    elif player_total == 11 and true_count > 0 and dealer_hand[0] == 11 and len(player_hand)==2:
                        # print("Player doubles")
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 10 and true_count > 3 and (dealer_hand == 11 or dealer_hand == 10) and len(player_hand)==2:
                        # print("Player doubles")
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 9 and true_count > 0 and dealer_hand == 2 and len(player_hand)==2:
                        # print("Player doubles")
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 9 and true_count > 2 and dealer_hand == 7 and len(player_hand)==2:
                        # print("Player doubles")
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 8 and true_count > 1 and dealer_hand == 6 and len(player_hand)==2:
                        # print("Player doubles")
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 16 and 2 <= dealer_hand[0] <= 6:
                        # print("Player stands")
                        break
                    elif player_total == 15 and 2 <= dealer_hand[0] <= 6:
                        # print("Player stands")
                        break
                    elif player_total == 14 and 2 <= dealer_hand[0] <= 6:
                        # print("Player stands")
                        break
                    elif player_total == 13 and 2 <= dealer_hand[0] <= 6:
                        # print("Player stands")
                        break
                    elif player_total == 12 and 4 <= dealer_hand[0] <= 6:
                        # print("Player stands")
                        break
                    elif player_total == 11 and len(player_hand)==2:
                        # print("Player doubles")
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 10 and 2 <= dealer_hand[0] <= 9 and len(player_hand)==2:
                        # print("Player doubles")
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 9 and 3 <= dealer_hand[0] <= 6 and len(player_hand)==2:
                        # print("Player doubles")
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    else:
                        player_hand.append(deck.pop())
                        if (player_hand[len(player_hand) - 1]) < 7:
                            count += 1
                        elif (player_hand[len(player_hand) - 1]) > 9:
                            count -= 1
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        # print("Player hits. New Hand:", player_hand)

            # print("Player's Hand:", player_hand)

            if player_total <= 21:
                while dealer_total < 17:
                    dealer_hand.append(deck.pop())
                    if (dealer_hand[len(dealer_hand) - 1]) < 7:
                        count += 1
                    elif (dealer_hand[len(dealer_hand) - 1]) > 9:
                        count -= 1
                    dealer_total = sum(dealer_hand)
                    if dealer_total > 21 and 11 in dealer_hand:
                        dealer_hand = check_for_ace(dealer_hand, dealer_total)
                        dealer_total = sum(dealer_hand)

            # print("Dealer's Hand:", dealer_hand)

            actual_sims += 1
            if dealer_hand[1] < 7:
                count += 1
            elif dealer_hand[1] > 9:
                count -= 1

            if player_total > 21 or (21 >= dealer_total > player_total):
                # print("Player loses")
                losses += 1
                if double == 1:
                    money -= bet_size * 2
                else:
                    money -= bet_size
            elif check_for_push(player_total, dealer_total):
                # print("Push (Tie)")
                pushes += 1
            else:
                # print("Player wins")
                wins += 1
                if double == 1:
                    money += bet_size * 2
                else:
                    money += bet_size

            if len(deck) <= cutting_card:
                cutting_card,deck = reshuffle(deck, deck_count)
                count = 0
            win_probabilities.append(wins / actual_sims)
            moneyrecord2.append(money)
            pbar.update(1)

        pbar.update(num_simulations - pbar.n)

    return win_probabilities, wins, losses, pushes, money,moneyrecord2


decks = 8
sims = 1000000
win_probabilities, wins, losses, pushes, money,moneyrecord = simulate_blackjack1(decks, sims)
win_probabilities2, wins2, losses2, pushes2, money2,moneyrecord2 = simulate_blackjack2(decks, sims)
print(money)
print(int(money2))
window_size = 10000  # Adjust this value to control the smoothing
moving_average = np.convolve(win_probabilities, np.ones(window_size) / window_size, mode='valid')
moving_average2 = np.convolve(win_probabilities2, np.ones(window_size) / window_size, mode='valid')

# Win Probability Over Time with Moving Average
plt.figure(figsize=(10, 6))
plt.plot(range(window_size, sims + 1), moving_average)
plt.xlabel('Number of Simulations')
plt.ylabel('Win Probability')
plt.title(f'Win Probability Over Time (Moving Average, Window Size: {window_size})')
plt.grid(True)
plt.show()

# Win Probability Over Time with Moving Average
plt.figure(figsize=(10, 6))
plt.plot(range(window_size, sims + 1), moving_average2)
plt.xlabel('Number of Simulations')
plt.ylabel('Win Probability')
plt.title(f'Win Probability Over Time (Moving Average2, Window Size: {window_size})')
plt.grid(True)
plt.show()


# Win/Loss/Draw Distribution
outcome_labels = ['Wins', 'Losses', 'Pushes']
outcome_counts = [wins, losses, pushes]

plt.figure(figsize=(8, 6))
plt.bar(outcome_labels, outcome_counts)
plt.xlabel('Outcome')
plt.ylabel('Count')
plt.title('Win/Loss/Draw Distribution')
plt.grid(True)
plt.show()

outcome_labels = ['Wins', 'Losses', 'Pushes']
outcome_counts = [wins2, losses2, pushes2]

plt.figure(figsize=(8, 6))
plt.bar(outcome_labels, outcome_counts)
plt.xlabel('Outcome')
plt.ylabel('Count')
plt.title('Win/Loss/Draw Distribution')
plt.grid(True)
plt.show()
# print(f"Runtime: %s seconds (approx {prob_sec} hands analysed per second)." % (time.time() - start_time))
#Money fluctuations over time1
plt.figure(figsize=(10, 6))
plt.plot(range(sims), moneyrecord)
plt.xlabel('Number of Simulations')
plt.ylabel('Money in the Bank')
plt.title('Monetary Fluctuation')
plt.xlim(0, len(moneyrecord))  # Set the x-axis limits
plt.grid(True)
plt.show()

#Money fluctuations over time2
plt.figure(figsize=(10, 6))
plt.plot(range(sims), moneyrecord2)
plt.xlabel('Number of Simulations')
plt.ylabel('Money in the Bank')
plt.title('Monetary fluctuation2')
plt.xlim(0, len(moneyrecord2))  # Set the x-axis limits
plt.grid(True)
plt.show()