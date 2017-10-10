# Implementation of classic arcade game Pong

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



import random
#import simpleguitk as simplegui
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80

ball_pos = [600 / 2, 400 / 2]

ball_vel = [0, 0]

LEFT = False
RIGHT = True

paddle1_pos = 100
paddle2_pos = 100

paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists

    if direction == RIGHT:
        ball_vel = [random.randrange(2, 4), random.randrange(-3, -1)]
        ball_pos = [300, 200]
    elif direction == LEFT:
        ball_vel = [random.randrange(-4, -2), random.randrange(-3, -1)]
        ball_pos = [300, 200]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'Green', "white")
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    # draw paddles
    if paddle1_pos <= 36:
        paddle1_pos = 36
    elif paddle1_pos >= HEIGHT - 36:
        paddle1_pos = HEIGHT - 36
    if paddle2_pos <= 36:
        paddle2_pos = 36
    elif paddle2_pos >= HEIGHT - 36:
        paddle2_pos = HEIGHT - 36

    canvas.draw_line([0, paddle1_pos], [PAD_WIDTH, paddle1_pos], PAD_HEIGHT, 'Red')
    canvas.draw_line([WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH, paddle2_pos], PAD_HEIGHT, 'Green')
    # determine whether paddle and ball collide
    if ball_pos[1] >= (paddle1_pos - 60) and ball_pos[1] <= (paddle1_pos + 40) and ball_pos[0] <= PAD_WIDTH + 20:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] += (0.10 * (ball_vel[0]))
        ball_vel[1] += (0.10 * (ball_vel[1]))

    elif ball_pos[1] >= (paddle2_pos - 60) and ball_pos[1] <= (paddle2_pos + 40) and ball_pos[0] >= (
        WIDTH - PAD_WIDTH) - 20:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] += (0.10 * (ball_vel[0]))
        ball_vel[1] += (0.10 * (ball_vel[1]))
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[0] <= PAD_WIDTH + 16:
        spawn_ball(RIGHT)
        score2 += 1
    elif ball_pos[0] >= (WIDTH - PAD_WIDTH) - 16:
        spawn_ball(LEFT)
        score1 += 1

    # draw scores
    canvas.draw_text(str(score1), [200, 100], 60, "gold")
    canvas.draw_text(str(score2), [400, 100], 60, "orange")


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 6
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 6
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 6
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 6


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += 6
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= 6
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel += 6
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= 6

        # create frame


frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', new_game)

# start frame
new_game()
frame.start()
