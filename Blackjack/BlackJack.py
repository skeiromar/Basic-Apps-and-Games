# Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

BACK_SIZE = (72, 96)
BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
score = 0
win_lost_status = 0  # 0 = no one won. 1 = player won. 2 = dealer won.

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


class Hand:
    def __init__(self):
        self.hand = []  # Stores cards in hand.

    def __str__(self):
        s = "Hand contains: "
        for i in self.hand:
            s += str(i) + " "
            s += " Value: " + str(VALUES[i.get_rank()]) + " "
        return s  # Returns ranks, suits and values of the cards in a hand

    def add_card(self, card):
        self.hand.append(card)  # Adds a card object to a hand

    def get_value(self):
        hand_value = 0
        count_of_ace = 0
        for i in self.hand:
            if i.get_rank() != 'A':
                hand_value += VALUES[i.get_rank()]
            else:
                if hand_value + 11 <= 21:
                    hand_value += 11
                else:
                    hand_value += 1
                count_of_ace += 1
        if count_of_ace > 1 and hand_value > 21:
            hand_value -= 10
        return hand_value

    def draw(self, canvas, pos):
        # The pos is the location of the leftmost card in a hand. So it need not change height, only width.
        for i in self.hand:
            i.draw(canvas, pos)
            pos[0] += 100
        if in_play:
            canvas.draw_image(card_back, BACK_CENTER,
                              BACK_SIZE, [71, 248], BACK_SIZE)  # Draw back of card image for dealer card.
            # Hard coded value is the addition of pos for dealer hand plus CARD_CENTER


class Deck:
    def __init__(self):
        self.deck = [Card(s, r) for s in SUITS for r in RANKS]  # Creates a 52 card deck.

    def shuffle(self):
        random.shuffle(self.deck)  # Shuffles the deck

    def deal_card(self):
        return random.choice(self.deck)  # Deals a card object from the deck

    def __str__(self):
        s = "Deck contains: "
        for i in self.deck:
            s += str(i) + " "
        return s  # Returns all the card objects from the deck in a string format.


def deal():
    global in_play, score, shuffled_deck, player_hand, dealer_hand, win_lost_status

    shuffled_deck = Deck()
    shuffled_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()

    for i in range(2):
        player_hand.add_card(shuffled_deck.deal_card())
        dealer_hand.add_card(shuffled_deck.deal_card())

    #if in_play:
     #   score -= 1

    in_play = True
    win_lost_status = 0


def hit():
    global score, in_play, win_lost_status

    if player_hand.get_value() <= 21 and win_lost_status == 0:
        player_hand.add_card(shuffled_deck.deal_card())

        if player_hand.get_value() > 21:
            in_play = False
            win_lost_status = 2
            score -= 1


def stand():
    global score, win_lost_status, in_play

    if player_hand.get_value() > 21 and win_lost_status == 0:
        win_lost_status = 2

    elif win_lost_status == 0:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(shuffled_deck.deal_card())

        if dealer_hand.get_value() > 21:
            win_lost_status = 1
            score += 1

        elif dealer_hand.get_value() == player_hand.get_value():
            win_lost_status = 2
            score -= 1

        elif dealer_hand.get_value() > player_hand.get_value():
            win_lost_status = 2
            score -= 1

        else:
            win_lost_status = 1
            score += 1

        in_play = False


def draw(canvas):
    global score, win_lost_status

    canvas.draw_text("Blackjack", [20, 60], 40, "purple")  # Draw Blackjack
    canvas.draw_text("Score: {}".format(score), [400, 60], 30, "red")  # Draw score
    canvas.draw_text("Dealer: ", [25, 190], 25, "violet")  # Draw Dealer
    canvas.draw_text("Player: ", [25, 390], 25, "violet")  # Draw Player

    if win_lost_status == 1:
        canvas.draw_text("Player won", [325, 190], 25, "Orange")
        canvas.draw_text("New deal?", [325, 390], 25, "Yellow")

    elif win_lost_status == 2:
        canvas.draw_text("Dealer won", [325, 190], 25, "Red")
        canvas.draw_text("New deal?", [325, 390], 25, "Yellow")

    else:
        canvas.draw_text("Hit or stand?", [325, 390], 25, "Yellow")

    dealer_hand.draw(canvas, [35, 200])
    player_hand.draw(canvas, [35, 400])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Light Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 75)
frame.add_button("Hit", hit, 75)
frame.add_button("Stand", stand, 75)
frame.set_draw_handler(draw)

deal()
frame.start()
