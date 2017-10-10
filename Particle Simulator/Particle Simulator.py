import simpleguitk as simplegui
import random

# global values
WIDTH = 600
HEIGHT = 400
particle_list = []
direction_list = [[1, 0], [0, 1], [-1, 0], [0, -1]]
color_list = ["red", "blue", "green", "yellow", "orange", "purple", "violet", "white", "black"]



class Particle:

    def __init__(self, position, color):
        self.position = position
        self.color = color

    def move(self, offset):

        self.position[0] += offset[0]
        self.position[1] += offset[1]


    def draw(self, canvas):

        canvas.draw_circle(self.position, 8, 1, self.color, random.choice(color_list))

    def __str__(self):
        return "Position: " + str(self.position) + " Color: " + self.color

def draw(canvas):
    for i in particle_list:
        i.move(random.choice(direction_list))
        i.draw(canvas)
    #for i in particle_list:
     #   i.draw(canvas)

for i in range(100):
    j = Particle([WIDTH / 2, HEIGHT / 2], random.choice(color_list))
    particle_list.append(j)

frame = simplegui.create_frame("Particle Simulator", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

frame.start()