# template for "Stopwatch: The Game"
import simpleguitk as simplegui

# define global variables
interval = 100
counter = 0
position = [80, 130]
timer_text = "0:00.0"
reflex_counter1 = "X"
reflex_counter2 = "Y"
y_increment = 0
x_increment = 0
is_running = False


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

def format(t):
    a = t / 600
    d = t % 10
    bc = (t / 10) % 60
    b = bc / 10
    c = bc % 10

    return str(a) + ":" + str(b) + str(c) + "." + str(d)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_running
    timer.start()
    if timer.is_running() == True:
        is_running = True


def stop():
    global reflex_counter1
    global reflex_counter2
    global counter
    global is_running
    global x_increment
    global y_increment

    d = counter % 10
    c = ((counter / 10) % 60) % 10

    if is_running == True:
        if c < 10 and d == 0:
            x_increment += 1
            reflex_counter1 = str(x_increment)

        y_increment += 1
        reflex_counter2 = str(y_increment)

    timer.stop()

    if timer.is_running() == False:
        is_running = False


def reset():
    global x_increment
    global y_increment
    global reflex_counter1
    global reflex_counter2
    global counter
    global timer_text
    global is_running
    timer.stop()
    x_increment = 0
    y_increment = 0
    reflex_counter1 = "X"
    reflex_counter2 = "Y"
    counter = 0
    timer_text = str(counter)
    is_running = False


# define event handler for timer with 0.1 sec interval
def create_timer():
    global counter
    counter += 1


# define draw handler
def draw_handler(canvas):
    timer_text = format(counter)
    canvas.draw_text(timer_text, position, 40, 'white')
    canvas.draw_text(reflex_counter1 + "/" + reflex_counter2, [240, 50], 26, 'red')


# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)

# register event handlers
timer = simplegui.create_timer(interval, create_timer)
frame.set_draw_handler(draw_handler)
button1 = frame.add_button('Start timer', start)
button2 = frame.add_button('Stop timer', stop)
button3 = frame.add_button('Reset', reset)

# start frame
frame.start()


# Please remember to review the grading rubric
