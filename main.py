import random
import time
import scipy
import statistics
import seaborn
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
    return cutting_card, deck


def simulate_blackjack1(deck_count, num_simulations):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * (4 * deck_count)
    cutting_card = random.randrange(int(0.45 * len(deck)), int(0.55 * len(deck)))
    print(cutting_card)
    random.shuffle(deck)
    dealer_busts = 0
    player_busts = 0
    win_probabilities = []
    moneyrecord = []
    wins = 0
    losses = 0
    pushes = 0
    actual_sims = 0
    splits = 0
    doubles = 0
    money = 5000

    with tqdm(total=num_simulations, ncols=80,
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [Time elapsed: {elapsed}, Time remaining: {remaining}, '
                         '{rate_fmt}{postfix}]',
              unit='hands', dynamic_ncols=True) as pbar:
        while actual_sims < sims:

            player_hand = [deck.pop(), deck.pop()]
            player_total = sum(player_hand)
            player_hand = check_for_ace(player_hand, player_total)
            player_total = sum(player_hand)
            player_total2 = 0
            player_hand2 = []
            double = 0
            split_double = 0
            split = 0
            dealer_hand = [deck.pop(), deck.pop()]
            dealer_total = sum(dealer_hand)

            # print("-----")
            # print("Player's Hand:", player_hand)
            # print("Dealer's Hand:", [dealer_hand[0], "?"])

            if check_for_blackjack(dealer_hand, dealer_total) and dealer_hand[0] == 11:
                if check_for_blackjack(player_hand, player_total):
                    # print("Dealer's hand : [11, 10] \nBoth the player and the dealer have blackjack. Push(tie)")
                    pushes += 1
                    if len(deck) <= cutting_card:
                        cutting_card, deck = reshuffle(deck, deck_count)
                    continue
                else:
                    # print("Dealer's hand : [11, 10] \nDealer has blackjack. Player loses")
                    losses += 1
                    money -= 5
                    if len(deck) <= cutting_card:
                        cutting_card, deck = reshuffle(deck, deck_count)
                    continue

            if check_for_blackjack(player_hand, player_total):
                # print("Player has blackjack. Player wins")
                wins += 1
                money += 7.5
                if len(deck) <= cutting_card:
                    cutting_card, deck = reshuffle(deck, deck_count)
                continue
            if player_total == 12 and (player_hand[0] == 1 or player_hand[1] == 1):
                # print("split aces")
                splits += 1
                split = 1
                player_hand = [11, deck.pop()]
                player_hand2 = [11, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 9 and (2 <= dealer_hand[0] <= 6 or 8 <= dealer_hand[0] <= 9):
                # print("split nines")
                splits += 1
                split = 1
                player_hand = [9, deck.pop()]
                player_hand2 = [9, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 8:
                # print("split eights")
                splits += 1
                split = 1
                player_hand = [8, deck.pop()]
                player_hand2 = [8, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 7 and dealer_hand[0] <= 7:
                # print("split sevens")
                splits += 1
                split = 1
                player_hand = [7, deck.pop()]
                player_hand2 = [7, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 6 and dealer_hand[0] <= 6:
                # print("split sixs")
                splits += 1
                split = 1
                player_hand = [6, deck.pop()]
                player_hand2 = [6, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 4 and (dealer_hand[0] == 5 or dealer_hand[0] == 6):
                # print("split fours")
                splits += 1
                split = 1
                player_hand = [4, deck.pop()]
                player_hand2 = [4, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 3 and dealer_hand[0] <= 7:
                # print("split threes")
                splits += 1
                split = 1
                player_hand = [3, deck.pop()]
                player_hand2 = [3, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 2 and dealer_hand[0] <= 7:
                # print("split twos")
                splits += 1
                split = 1
                player_hand = [2, deck.pop()]
                player_hand2 = [2, deck.pop()]
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)

            while player_total < 21:
                if 11 in player_hand:
                    if player_total == 20:
                        # print("Player stands")
                        break
                    elif player_total == 19:
                        if dealer_hand[0] == 6 and len(player_hand) == 2:
                            # print("Player doubles")
                            doubles += 1
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
                            player_hand = check_for_ace(player_hand, player_total)
                            player_total = sum(player_hand)
                            double = 1

                            break
                        else:
                            # print("Player stands")
                            break
                    elif player_total == 18:
                        if 2 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            # print("Player doubles")
                            doubles += 1
                            player_hand.append(deck.pop())
                            player_total = sum(player_hand)
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
                            # print("Player stands")
                            break
                    elif player_total == 17:
                        if 3 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            # print("Player doubles")
                            doubles += 1
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
                        if 4 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            # print("Player doubles")
                            doubles += 1
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
                        if 4 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            # print("Player doubles")
                            doubles += 1
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
                        if 5 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            # print("Player doubles")
                            doubles += 1
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
                        if 5 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            # print("Player doubles")
                            doubles += 1
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
                        # print("Player stands")
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
                    elif player_total == 11 and len(player_hand) == 2:
                        # print("Player doubles")
                        doubles += 1
                        player_hand.append(deck.pop())
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 10 and 2 <= dealer_hand[0] <= 9 and len(player_hand) == 2:
                        # print("Player doubles")
                        doubles += 1
                        player_hand.append(deck.pop())
                        player_total = sum(player_hand)
                        player_hand = check_for_ace(player_hand, player_total)
                        player_total = sum(player_hand)
                        double = 1
                        break
                    elif player_total == 9 and 3 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                        # print("Player doubles")
                        doubles += 1
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
                        # print("Player hits. New Hand:", player_hand)
            if split == 1:
                while player_total2 < 21:
                    if 11 in player_hand2:
                        if player_total2 == 20:
                            # print("Player stands")
                            break
                        elif player_total2 == 19:
                            if dealer_hand[0] == 6 and len(player_hand2) == 2:
                                # print("Player doubles")
                                doubles += 1
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1

                                break
                            else:
                                # print("Player stands")
                                break
                        elif player_total2 == 18:
                            if 2 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                # print("Player doubles")
                                doubles += 1
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            elif 9 <= dealer_hand[0] <= 11:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                            else:
                                # print("Player stands")
                                break
                        elif player_total2 == 17:
                            if 3 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                # print("Player doubles")
                                doubles += 1
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 16:
                            if 4 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                # print("Player doubles")
                                doubles += 1
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 15:
                            if 4 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                # print("Player doubles")
                                doubles += 1
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 14:
                            if 5 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                # print("Player doubles")
                                doubles += 1
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 13:
                            if 5 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                # print("Player doubles")
                                doubles += 1
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                    else:
                        if player_total2 >= 17:
                            # print("Player stands")
                            break
                        elif player_total2 == 16 and 2 <= dealer_hand[0] <= 6:
                            # print("Player stands")
                            break
                        elif player_total2 == 15 and 2 <= dealer_hand[0] <= 6:
                            # print("Player stands")
                            break
                        elif player_total2 == 14 and 2 <= dealer_hand[0] <= 6:
                            # print("Player stands")
                            break
                        elif player_total2 == 13 and 2 <= dealer_hand[0] <= 6:
                            # print("Player stands")
                            break
                        elif player_total2 == 12 and 4 <= dealer_hand[0] <= 6:
                            # print("Player stands")
                            break
                        elif player_total2 == 11 and len(player_hand2) == 2:
                            # print("Player doubles")
                            doubles += 1
                            player_hand2.append(deck.pop())
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 10 and 2 <= dealer_hand[0] <= 9 and len(player_hand2) == 2:
                            # print("Player doubles")
                            doubles += 1
                            player_hand2.append(deck.pop())
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 9 and 3 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                            # print("Player doubles")
                            doubles += 1
                            player_hand2.append(deck.pop())
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        else:
                            player_hand2.append(deck.pop())
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            # print("Player hits. New Hand:", player_hand)
            # print("Player's Hand:", player_hand)
            # if split==1:
            # print("Player's Hand 2: ", player_hand2)
            dealer_total = sum(dealer_hand)
            dealer_hand = check_for_ace(dealer_hand, dealer_total)
            dealer_total = sum(dealer_hand)
            if player_total <= 21 or (player_total2 <= 21 and split == 1):
                while dealer_total < 17:
                    dealer_hand.append(deck.pop())
                    dealer_total = sum(dealer_hand)
                    if dealer_total > 21 and 11 in dealer_hand:
                        dealer_hand = check_for_ace(dealer_hand, dealer_total)
                        dealer_total = sum(dealer_hand)

            # print("Dealer's Hand:", dealer_hand)

            actual_sims += 1

            if player_total > 21 or (21 >= dealer_total > player_total):
                # print("Player loses")

                losses += 1
                if double == 1:
                    money -= 10
                else:
                    money -= 5
            elif check_for_push(player_total, dealer_total):
                # print("Push (Tie)")
                pushes += 1
            else:
                # print("Player wins")
                wins += 1
                if double == 1:
                    money += 10
                else:
                    money += 5
            if split == 1:
                if player_total2 > 21 or (21 >= dealer_total > player_total2):
                    # print("Player loses")
                    losses += 1
                    if split_double == 1:
                        money -= 10
                    else:
                        money -= 5
                elif check_for_push(player_total2, dealer_total):
                    # print("Push (Tie)")
                    pushes += 1
                else:
                    # print("Player wins")
                    wins += 1
                    if split_double == 1:
                        money += 10
                    else:
                        money += 5
            if dealer_total > 21:
                dealer_busts += 1
            if player_total > 21:
                player_busts += 1
            if player_total2 > 21:
                player_busts += 1
            if len(deck) <= cutting_card:
                cutting_card, deck = reshuffle(deck, deck_count)
            win_probabilities.append(wins / actual_sims)
            moneyrecord.append(money)
            pbar.update(1)

        pbar.update(num_simulations - pbar.n)

    return win_probabilities, wins, losses, pushes, money, moneyrecord, doubles, splits, dealer_busts, player_busts


def simulate_blackjack2(deck_count, num_simulations):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * (4 * deck_count)
    cutting_card = random.randrange(int(0.45 * len(deck)), int(0.55 * len(deck)))
    random.shuffle(deck)
    moneyrecord2 = []
    win_probabilities = []
    bet_sizes=[]
    wins = 0
    losses = 0
    pushes = 0
    doubles2 = 0
    splits2 = 0
    actual_sims = 0
    dealer_busts = 0
    player_busts = 0
    player_busts_record=[]
    dealer_busts_record=[]
    bad_good_insurance = []
    money = 5000
    count = 0
    all_true_counts = []

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
            player_total = sum(player_hand)
            double = 0
            split_double = 0
            split = 0
            player_total2 = 0
            player_hand2 = []
            dealer_hand = [deck.pop(), deck.pop()]
            # print("Dealer hand: ", dealer_hand)
            if dealer_hand[0] < 7:
                count += 1
            elif dealer_hand[0] > 9:
                count -= 1
            dealer_total = sum(dealer_hand)
            true_count = round(count / round(len(deck) / 52))

            bet_unit = 5

            bet_size = (true_count - 1) * bet_unit
            if true_count <= 1:
                bet_size = 5

            if money > 4:
                if bet_size >= money / 4:
                    bet_size = money / 4
            if bet_size < 5:
                bet_size = 5
            '''
            if true_count<=0:
                bet_size=5
            elif true_count>=6:
                bet_size=60
            else:
                bet_size=true_count*10
            '''

            print("-----")
            print("Player's Hand:", player_hand)
            print("Dealer's Hand:", [dealer_hand[0], "?"])
            print("Bet size:", bet_size)

            if dealer_hand[0] == 11 and check_for_blackjack(player_hand, player_total) == 0:
                if true_count >= 3:
                    insurance = 1
                    bet_size += bet_size / 2

            if check_for_blackjack(dealer_hand, dealer_total) and dealer_hand[0] == 11:

                if check_for_blackjack(player_hand, player_total):
                    print("Dealer's hand : [11, 10] \nBoth the player and the dealer have blackjack. Push(tie)")
                    pushes += 1
                    count -= 1
                    if len(deck) <= cutting_card:
                        cutting_card, deck = reshuffle(deck, deck_count)
                        count = 0
                    continue

                elif insurance == 1:
                    print("INSURANCE WORKED!!!")
                    bad_good_insurance.append(1)
                    pushes += 1
                    count -= 1

                    if len(deck) <= cutting_card:
                        cutting_card, deck = reshuffle(deck, deck_count)
                        count = 0
                    continue
                else:
                    print("Dealer's hand : [11, 10] \nDealer has blackjack. Player loses")
                    losses += 1
                    count -= 1
                    money -= bet_size
                    if len(deck) <= cutting_card:
                        cutting_card, deck = reshuffle(deck, deck_count)
                        count = 0
                    continue

            if check_for_blackjack(player_hand, player_total):
                print("Player has blackjack. Player wins")
                wins += 1
                if dealer_hand[1] < 7:
                    count += 1
                elif dealer_hand[1] > 9:
                    count -= 1
                money += bet_size * 1.5
                if len(deck) <= cutting_card:
                    cutting_card, deck = reshuffle(deck, deck_count)
                    count = 0
                continue
            if player_total == 12 and (player_hand[0] == 1 or player_hand[1] == 1):
                print("split aces")
                splits2 += 1
                split = 1
                player_hand = [11, deck.pop()]
                player_hand2 = [11, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 10 and true_count > 3 and dealer_hand[0] == 6:
                print("split tens")
                splits2 += 1
                split = 1
                player_hand = [10, deck.pop()]
                player_hand2 = [10, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 10 and true_count > 4 and dealer_hand[0] == 5:
                print("split tens")
                splits2 += 1
                split = 1
                player_hand = [10, deck.pop()]
                player_hand2 = [10, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 10 and true_count > 5 and dealer_hand[0] == 4:
                print("split tens")
                splits2 += 1
                split = 1
                player_hand = [10, deck.pop()]
                player_hand2 = [10, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 9 and (2 <= dealer_hand[0] <= 6 or 8 <= dealer_hand[0] <= 9):
                print("split nines")
                splits2 += 1
                split = 1
                player_hand = [9, deck.pop()]
                player_hand2 = [9, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 8:
                print("split eights")
                splits2 += 1
                split = 1
                player_hand = [8, deck.pop()]
                player_hand2 = [8, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 7 and dealer_hand[0] <= 7:
                print("split sevens")
                splits2 += 1
                split = 1
                player_hand = [7, deck.pop()]
                player_hand2 = [7, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 6 and dealer_hand[0] <= 6:
                print("split sixs")
                splits2 += 1
                split = 1
                player_hand = [6, deck.pop()]
                player_hand2 = [6, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 4 and (dealer_hand[0] == 5 or dealer_hand[0] == 6):
                print("split fours")
                splits2 += 1
                split = 1
                player_hand = [4, deck.pop()]
                player_hand2 = [4, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 3 and dealer_hand[0] <= 7:
                print("split threes")
                splits2 += 1
                split = 1
                player_hand = [3, deck.pop()]
                player_hand2 = [3, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            if player_hand[0] == player_hand[1] == 2 and dealer_hand[0] <= 7:
                print("split twos")
                splits2 += 1
                split = 1
                player_hand = [2, deck.pop()]
                player_hand2 = [2, deck.pop()]
                if player_hand[1] < 7:
                    count += 1
                elif player_hand[1] > 9:
                    count -= 1
                if player_hand2[1] < 7:
                    count += 1
                elif player_hand2[1] > 9:
                    count += 1
                player_total = sum(player_hand)
                player_total2 = sum(player_hand2)
            while player_total < 21:
                print("Player hand: ", player_hand)
                print("Dealer hand: ", dealer_hand)
                print("True count: ", true_count)

                if 11 in player_hand:
                    if player_total == 20:
                        print("Player stands")
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

                        elif dealer_hand[0] == 6 and len(player_hand) == 2:
                            print("Player doubles")
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
                            print("Player stands")
                            break
                    elif player_total == 18:
                        if 2 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            print("Player doubles")
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
                            print("Player stands")
                            break
                    elif player_total == 17:
                        if true_count > 0 and dealer_hand[0] == 2:
                            break
                        elif 3 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            print("Player doubles")
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
                        if 4 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            print("Player doubles")
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

                    elif player_total == 15:
                        if 4 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            print("Player doubles")
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
                        if 5 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            print("Player doubles")
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
                        if 5 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                            print("Player doubles")
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
                        print("Player stands")
                        break
                    elif player_total == 16 and true_count > 0 and dealer_hand[0] == 10:
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
                    elif player_total == 11 and true_count > 0 and dealer_hand[0] == 11 and len(player_hand) == 2:
                        print("Player doubles")
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
                    elif player_total == 10 and true_count > 3 and (dealer_hand == 11 or dealer_hand == 10) and len(
                            player_hand) == 2:
                        print("Player doubles")
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
                    elif player_total == 9 and true_count > 0 and dealer_hand == 2 and len(player_hand) == 2:
                        print("Player doubles")
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
                    elif player_total == 9 and true_count > 2 and dealer_hand == 7 and len(player_hand) == 2:
                        print("Player doubles")
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
                    elif player_total == 8 and true_count > 1 and dealer_hand == 6 and len(player_hand) == 2:
                        print("Player doubles")
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
                        print("Player stands")
                        break
                    elif player_total == 15 and 2 <= dealer_hand[0] <= 6:
                        print("Player stands")
                        break
                    elif player_total == 14 and 2 <= dealer_hand[0] <= 6:
                        print("Player stands")
                        break
                    elif player_total == 13 and 2 <= dealer_hand[0] <= 6:
                        print("Player stands")
                        break
                    elif player_total == 12 and 4 <= dealer_hand[0] <= 6:
                        print("Player stands")
                        break
                    elif player_total == 11 and len(player_hand) == 2:
                        print("Player doubles")
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
                    elif player_total == 10 and 2 <= dealer_hand[0] <= 9 and len(player_hand) == 2:
                        print("Player doubles")
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
                    elif player_total == 9 and 3 <= dealer_hand[0] <= 6 and len(player_hand) == 2:
                        print("Player doubles")
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
                        print("Player hits. New Hand:", player_hand)
            if split == 1:
                while player_total2 < 21:
                    print("Player hand: ", player_hand)
                    print("Dealer hand: ", dealer_hand)
                    print("True count: ", true_count)

                    if 11 in player_hand2:
                        if player_total2 == 20:
                            print("Player stands")
                            break
                        elif player_total2 == 19:
                            if true_count > 2 and dealer_hand[0] == 4:
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                            elif true_count > 0 and (dealer_hand[0] == 5 or dealer_hand[0] == 6):
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)

                            elif dealer_hand[0] == 6 and len(player_hand) == 2:
                                print("Player doubles")
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                print("Player stands")
                                break
                        elif player_total2 == 18:
                            if 2 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                print("Player doubles")
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            elif 9 <= dealer_hand[0] <= 11:
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                            else:
                                print("Player stands")
                                break
                        elif player_total2 == 17:
                            if true_count > 0 and dealer_hand[0] == 2:
                                break
                            elif 3 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                print("Player doubles")
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 16:
                            if 4 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                print("Player doubles")
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)

                        elif player_total2 == 15:
                            if 4 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                print("Player doubles")
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)

                        elif player_total2 == 14:
                            if 5 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                print("Player doubles")
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                        elif player_total2 == 13:
                            if 5 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                                print("Player doubles")
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)
                                split_double = 1
                                break
                            else:
                                player_hand2.append(deck.pop())
                                if (player_hand2[len(player_hand2) - 1]) < 7:
                                    count += 1
                                elif (player_hand2[len(player_hand2) - 1]) > 9:
                                    count -= 1
                                player_total2 = sum(player_hand2)
                                player_hand2 = check_for_ace(player_hand2, player_total2)
                                player_total2 = sum(player_hand2)

                    else:
                        if player_total2 >= 17:
                            print("Player stands")
                            break
                        elif player_total2 == 16 and true_count > -1 and dealer_hand[0] == 10:
                            break
                        elif player_total2 == 16 and true_count > 3 and dealer_hand[0] == 9:
                            break
                        elif player_total2 == 15 and true_count > 3 and dealer_hand[0] == 10:
                            break
                        elif player_total2 == 13 and true_count < 0 and dealer_hand[0] == 2:
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                        elif player_total2 == 12 and true_count > 2 and dealer_hand[0] == 2:
                            break
                        elif player_total2 == 12 and true_count > 1 and dealer_hand[0] == 3:
                            break
                        elif player_total2 == 12 and true_count < 0 and dealer_hand[0] == 4:
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                        elif player_total2 == 11 and true_count > 0 and dealer_hand[0] == 11 and len(player_hand2) == 2:
                            print("Player doubles")
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 10 and true_count > 3 and (
                                dealer_hand == 11 or dealer_hand == 10) and len(
                            player_hand2) == 2:
                            print("Player doubles")
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 9 and true_count > 0 and dealer_hand == 2 and len(player_hand2) == 2:
                            print("Player doubles")
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 9 and true_count > 2 and dealer_hand == 7 and len(player_hand2) == 2:
                            print("Player doubles")
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 8 and true_count > 1 and dealer_hand == 6 and len(player_hand2) == 2:
                            print("Player doubles")
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 16 and 2 <= dealer_hand[0] <= 6:
                            print("Player stands")
                            break
                        elif player_total2 == 15 and 2 <= dealer_hand[0] <= 6:
                            print("Player stands")
                            break
                        elif player_total2 == 14 and 2 <= dealer_hand[0] <= 6:
                            print("Player stands")
                            break
                        elif player_total2 == 13 and 2 <= dealer_hand[0] <= 6:
                            print("Player stands")
                            break
                        elif player_total2 == 12 and 4 <= dealer_hand[0] <= 6:
                            print("Player stands")
                            break
                        elif player_total2 == 11 and len(player_hand) == 2:
                            print("Player doubles")
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 10 and 9 >= dealer_hand[0] >= 2 == len(player_hand2):
                            print("Player doubles")
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        elif player_total2 == 9 and 3 <= dealer_hand[0] <= 6 and len(player_hand2) == 2:
                            print("Player doubles")
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            split_double = 1
                            break
                        else:
                            player_hand2.append(deck.pop())
                            if (player_hand2[len(player_hand2) - 1]) < 7:
                                count += 1
                            elif (player_hand2[len(player_hand2) - 1]) > 9:
                                count -= 1
                            player_total2 = sum(player_hand2)
                            player_hand2 = check_for_ace(player_hand2, player_total2)
                            player_total2 = sum(player_hand2)
                            print("Player hits. New Hand:", player_hand)
            print("Player's Hand:", player_hand)
            dealer_total = sum(dealer_hand)
            dealer_hand = check_for_ace(dealer_hand, dealer_total)
            dealer_total = sum(dealer_hand)
            if player_total <= 21 or (player_total2 <= 21 and split == 1):
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

            print("Dealer's Hand:", dealer_hand)

            actual_sims += 1
            if dealer_hand[1] < 7:
                count += 1
            elif dealer_hand[1] > 9:
                count -= 1

            if player_total > 21 or (21 >= dealer_total > player_total):
                print("Player loses")
                losses += 1
                if double == 1:
                    money -= bet_size * 2
                else:
                    money -= bet_size
            elif check_for_push(player_total, dealer_total):
                print("Push (Tie)")
                pushes += 1
            else:
                print("Player wins")
                wins += 1
                if double == 1:
                    money += bet_size * 2
                else:
                    money += bet_size
            if split == 1:
                if player_total2 > 21 or (21 >= dealer_total > player_total2):
                    print("Player loses")
                    losses += 1
                    if split_double == 1:
                        money -= bet_size * 2
                    else:
                        money -= bet_size
                elif check_for_push(player_total2, dealer_total):
                    print("Push (Tie)")
                    pushes += 1
                else:
                    print("Player wins")
                    wins += 1
                    if split_double == 1:
                        money += bet_size * 2
                    else:
                        money += bet_size

            if dealer_total > 21:
                dealer_busts += 1
            if player_total > 21:
                player_busts += 1
            if player_total2 > 21:
                player_busts += 1
            if len(deck) <= cutting_card:
                cutting_card, deck = reshuffle(deck, deck_count)
                count = 0
            win_probabilities.append(wins / actual_sims)
            moneyrecord2.append(money)
            all_true_counts.append(true_count)
            bet_sizes.append(bet_size)
            if player_total > 21 >= player_total2:
                player_busts_record.append(1)
            elif player_total2 > 21 >= player_total:
                player_busts_record.append(1)
            elif player_total<=21 and player_total2<=21:
                player_busts_record.append(0)
            else:
                player_busts_record.append(2)
            if dealer_total>21:
                dealer_busts_record.append(1)
            else:
                dealer_busts_record.append(0)
            if insurance==1 and check_for_blackjack(dealer_hand,dealer_total)==0:
                bad_good_insurance.append(0)
            if double==1:
                doubles2+=1
            if split_double==1:
                doubles2+=1
            pbar.update(1)

        pbar.update(num_simulations - pbar.n)

    return win_probabilities, wins, losses, pushes, money, moneyrecord2,doubles2,splits2, dealer_busts, player_busts, all_true_counts,bet_sizes,player_busts_record,dealer_busts_record,bad_good_insurance


decks = 6
sims = 100000
win_probabilities, wins, losses, pushes, money, moneyrecord, doubles, splits, dealer_bust, player_bust = simulate_blackjack1(
    decks, sims)
win_probabilities2, wins2, losses2, pushes2, money2, moneyrecord2,doubles_gen2,splits_gen2, dealer_bust2, player_bust2, final_true_count, all_bet_sizes,player_busts_record_gen2,dealer_busts_record_gen2,insurance_efficiency = simulate_blackjack2(
    decks, sims)
print("Win ratio 1st gen: ", wins / 1000)
print("Win ratio 2nd gen: ", wins2 / 1000)
print("Number of doubles for 1st gen: ", doubles)
print("Number of splits for 1st gen: ", splits)
print("Number of doubles for 2nd gen: ",doubles_gen2)
print("Number of splits for 2nd gen: ",splits_gen2)
print("Dealer busts: ", dealer_bust)
print("Player busts: ", player_bust)
print("Dealer busts 2nd gen: ", dealer_bust2)
print("Player busts 2nd gen: ", player_bust2)
print("Lose ratio gen 1:", losses / 1000)
print("Lose ratio gen 2:", losses2 / 1000)
print("Push ratio gen 1:", pushes / 1000)
print("Push ratio gen 2:", pushes2 / 1000)
print("Average money value through the game gen 1:", round(statistics.mean(moneyrecord), 2))
print("Average money value through the game gen 2:", round(statistics.mean(moneyrecord), 2))
print("Average true count through the game gen 2", round(statistics.mean(final_true_count), 2))
print("Average bet size value through gen 2:",round(statistics.mean(all_bet_sizes),2))
print("Variance money value through the game gen 1:", round(statistics.variance(moneyrecord), 2))
print("Variance money value through the game gen 2:", round(statistics.variance(moneyrecord2), 2))
print("Variance true count through the game gen 2:", round(statistics.variance(final_true_count), 2))
print("Variance bet size through gen 2:",round(statistics.variance(all_bet_sizes),2))
print(money)
print(int(money2))
# calculating correlation coefficients
r = scipy.stats.pearsonr(moneyrecord2, final_true_count)
rho = scipy.stats.spearmanr(moneyrecord2, final_true_count)
tau = scipy.stats.kendalltau(moneyrecord2, final_true_count)

r_bet_size=scipy.stats.pearsonr(all_bet_sizes,final_true_count)
r_busts_player=scipy.stats.pearsonr(player_busts_record_gen2,final_true_count)
r_busts_dealer=scipy.stats.pearsonr(dealer_busts_record_gen2,final_true_count)

r_winratio_truecount=scipy.stats.pearsonr(win_probabilities,final_true_count)
print("Pearson Correlation between true count and money record \n If r is > 0 we have a positive correlation", r)
print("Spearman Correlation between true count and money record", rho)
print("Kendall Correlation between true count and money record", tau)
print("Pearson Correlation between true count and bet size: ",r_bet_size)
print("Pearson Correlation between true count and player busts: ",r_busts_player)
print("Pearson Correlation between true count and dealer busts: ",r_busts_dealer)
print("Pearson Correlation between true count and win-ratio: ",r_winratio_truecount)
#Did insurance work?
plt.hist(insurance_efficiency,color='blue',edgecolor='black',bins=int(2))
plt.title('Histogram of insurance efficiency')
plt.xlabel('Did insurance work?')
plt.ylabel('games')
plt.grid(True)
plt.show()


#True count and bet size over time visualized
fig, axs = plt.subplots(2, 1, figsize=(10,6))

# Plot True count over time
axs[0].plot(range(sims), final_true_count)
axs[0].set_xlabel('Number of Simulations')
axs[0].set_ylabel('True count')
axs[0].set_title('True count over time')
axs[0].set_xlim(0, len(final_true_count))  # Set the x-axis limits
axs[0].grid(True)

# Plot Bet size fluctuation
axs[1].plot(range(sims), all_bet_sizes)
axs[1].set_xlabel('Number of Simulations')
axs[1].set_ylabel('Bet size')
axs[1].set_title('Bet size fluctuation')
axs[1].set_xlim(0, len(all_bet_sizes))  # Set the x-axis limits
axs[1].grid(True)

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
#regresion line
'''
slope, intercept, r_lin, p, stderr = scipy.stats.linregress(moneyrecord2, final_true_count)
print(int(slope))
line = f'Regression line: final_true_count={intercept:.2f}+{slope:.2f}moneyrecord2, r={r_lin:.2f}'
fig, ax = plt.subplots()
ax.plot(moneyrecord2, final_true_count, linewidth=0, marker='s', label='Data points')
ax.plot(moneyrecord2, intercept + slope*moneyrecord2, label=line)
ax.set_xlabel('Money record')
ax.set_ylabel('True Count')
ax.legend(facecolor='white')
plt.show()
'''
#heatmap of correlation
corr_matrix=np.corrcoef(moneyrecord2,final_true_count).round(decimals=2)
fig, ax = plt.subplots()
im = ax.imshow(corr_matrix)
im.set_clim(-1, 1)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1), ticklabels=('moni', 'true count'))
ax.yaxis.set(ticks=(0, 1), ticklabels=('moni', 'true count'))
ax.set_ylim(2.5, -0.5)
for i in range(2):
    for j in range(2):
        ax.text(j, i, corr_matrix[i, j], ha='center', va='center',
                color='r')
cbar = ax.figure.colorbar(im, ax=ax, format='% .2f')
plt.show()
#Histograms
plt.hist(moneyrecord,color='blue',edgecolor='black',bins=int(10))
plt.title('Histogram of money 1st gen')
plt.xlabel('moni')
plt.ylabel('games')
plt.hist(moneyrecord2,color='red',edgecolor='black',bins=int(10))
plt.grid(True)
plt.title('Histogram of money 2st gen')
plt.xlabel('moni2')
plt.ylabel('games2')
plt.grid(True)
plt.show()

#ECDF

data=moneyrecord
data2=moneyrecord2
sorted_data=np.sort(data)
sorted_data2=np.sort(data2)
edf=np.arange(1,len(sorted_data)+1)/len(sorted_data)
edf2=np.arange(1,len(sorted_data2)+1)/len(sorted_data2)
plt.step(sorted_data, edf,label='moni 1', where='post')
plt.step(sorted_data2, edf2, label='moni 2', where='post')
plt.xlabel('Data')
plt.ylabel('Empirical Distribution Function')
plt.title('Empirical Distribution Function')
plt.ylim(0, 1)  # Set y-axis limits
plt.legend()
plt.grid(True)
plt.show()


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
# Money fluctuations over time1
plt.figure(figsize=(10, 6))
plt.plot(range(sims), moneyrecord)
plt.xlabel('Number of Simulations')
plt.ylabel('Money in the Bank')
plt.title('Monetary Fluctuation')
plt.xlim(0, len(moneyrecord))  # Set the x-axis limits
plt.grid(True)
plt.show()

# Money fluctuations over time2 + true count
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

# Plot True count over time
axs[0].plot(range(sims), final_true_count)
axs[0].set_xlabel('Number of Simulations')
axs[0].set_ylabel('True count')
axs[0].set_title('True count over time')
axs[0].set_xlim(0, len(final_true_count))  # Set the x-axis limits
axs[0].grid(True)

# Plot Bet size fluctuation
axs[1].plot(range(sims), moneyrecord2)
axs[1].set_xlabel('Number of Simulations')
axs[1].set_ylabel('Money in the bank')
axs[1].set_title('Money fluctuation gen 2')
axs[1].set_xlim(0, len(moneyrecord2))  # Set the x-axis limits
axs[1].grid(True)

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
