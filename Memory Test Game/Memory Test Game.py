# implementation of card game - Memory

import simpleguitk as simplegui
import random

card_list = range(0, 8)
card_list.extend(range(0, 8))
random.shuffle(card_list)
exposed = [False] * 16
state = 0
check_cards = []
which_card = []
counter = 0


# helper function to initialize globals
def new_game():
    global card_list, counter, exposed, state, check_cards, which_card
    state = 0
    for i in range(len(exposed)):
        exposed[i] = False
    random.shuffle(card_list)
    counter = 0
    label.set_text("Turns: " + str(counter))
    check_cards = []
    which_card = []


# define event handlers
def mouseclick(pos):
    global state, check_cards, which_card, counter  # pos[0] < (50 * (x + 1)) and pos[0] > (50 * x)
    for x in range(0, 17):
        if (50 * (x + 1)) > pos[0] > (50 * x) and state != 3 and not exposed[x]:
            exposed[x] = True
            check_cards.append(card_list[x])
            which_card.append(x)
            state += 1
            if state == 2:
                counter += 1
                label.set_text("Turns: " + str(counter))
            
        if state == 3:
            if check_cards[0] == check_cards[1]:
                state = 1
                check_cards = [card_list[x]]
                which_card = [x]
                #check_cards.append(card_list[x])
                #which_card.append(x)

            elif check_cards[0] != check_cards[1]:
                exposed[which_card[0]] = False
                exposed[which_card[1]] = False  # check_cards.append(card_list[x])
                state = 1
                which_card = [x]
                check_cards = [card_list[x]]
                #which_card.append(x)


# cards are logically 50x100 pixels in size
def draw(canvas):
    y = 8
    x = 50
    op = 0
    for i in exposed:
        if not i:
            canvas.draw_polygon([(x - 50 + 2, 2), (x, 2), (x, 133), (x - 50 + 2, 133)], 1, 'white', 'green')
        elif i:
            canvas.draw_text(str(card_list[op]), [y, 105], 50, "white")
        x += 50
        op += 1
        y += 50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game, 100)
label = frame.add_label("Turns: " + str(counter))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
