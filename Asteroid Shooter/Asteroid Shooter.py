
"""
This game is meant to be run in a browser preferably chrome. simplegui is the library used to build this game.
You can paste the code in codeskulptor.org and run.
For offline use, pip install SimpleGUICS2Pygame and it'll run but without sound.
The best place to run it is in the chrome browser.
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

# Animated asteroid info, horizontal tile sheet.
ROCK_DIM = 64  # quantity of rocks
ROCK_CENTER = [64, 64]
ROCK_SIZE = [128, 128]
ROCK_RADIUS = 54

# Realistic explosion info, 9x9 tile sheet.
EXPLOSION_CENTER = [50, 50]
EXPLOSION_SIZE = [100, 100]
EXPLOSION_DIM = [9, 9]
r_EXPLOSION_RADIUS = 40
r_explosion_lifespan = 73
"""
for explosion lifespan:

Age in sprite class updates at 0.9 t. There are 9x9=81 total frames to draw. 
By the time 0.9 t = 73, 1 t = 81. so all frames are drawn when 0.9 t thus explosion lifespan = 73
"""


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# All art assets credited to Kim Lathrop

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# animated rock image
rock_info = ImageInfo(ROCK_CENTER, ROCK_SIZE, ROCK_RADIUS, None, True)
rock_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/asteroid1.opengameart.warspawn.png")

# realistic explosion
r_explosion_info = ImageInfo(EXPLOSION_CENTER, EXPLOSION_SIZE, r_EXPLOSION_RADIUS, 73, True)
r_explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# sound assets were purchased from sounddogs.com except soundtrack
# soundtrack by Emiel Stophler. Ask here before using: http://www.filmcomposer.nl
soundtrack = simplegui.load_sound(
    "https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):  # calculates which way is forward
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):  # calculates the distance between two points on a canvas
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = angle_to_vector(self.angle)
        self.keys = {'left': -0.1,
                     'right': 0.1}

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def key_down(self, key):
        for i in self.keys:
            if key == simplegui.KEY_MAP[i]:
                self.angle_vel += self.keys[i]

    def key_up(self, key):
        for i in self.keys:
            if key == simplegui.KEY_MAP[i]:
                self.angle_vel -= self.keys[i]

    def is_thrust(self, is_on):
        self.thrust = is_on
        if self.thrust:
            ship_thrust_sound.play()
            self.image_center[0] += 90
        else:
            self.image_center[0] -= 90
            ship_thrust_sound.rewind()

    def update(self):

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel  # updates the rotation of the ship
        self.forward = angle_to_vector(self.angle)

        self.vel[0] *= (1 - 0.01)  # applies friction to velocity
        self.vel[1] *= (1 - 0.01)

        if self.thrust:
            self.vel[0] += self.forward[0] * 0.1  # moves toward the forward vector
            self.vel[1] += self.forward[1] * 0.1

        if self.pos[0] > WIDTH + 20:  # wraps ship around the canvas
            self.pos[0] = 0
        elif self.pos[0] < -20:
            self.pos[0] = WIDTH
        elif self.pos[1] > HEIGHT + 20:
            self.pos[1] = 0
        elif self.pos[1] < -20:
            self.pos[1] = HEIGHT

    def shoot(self):

        missile_vel = [self.vel[0] + self.forward[0] * 6, self.vel[1] + self.forward[1] * 4]  # missile velocity
        ship_cannon = [self.pos[0] + (44 * self.forward[0]),
                       self.pos[1] + (44 * self.forward[1])]  # position of the missile relative to the ship

        a_missile = Sprite(ship_cannon, missile_vel, 0, 0, missile_image, missile_info, missile_sound)

        missile_group.add(a_missile)

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.time_of_animation_asteroid = 0
        self.time_explosion = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):

        current_rock_index = (self.time_of_animation_asteroid % ROCK_DIM) // 1  # which rock to draw from the tile sheet
        current_rock_center = [ROCK_CENTER[0] + current_rock_index * ROCK_SIZE[0],
                               ROCK_CENTER[1]]  # the center of the rock to draw

        explosion_index = [self.time_explosion % EXPLOSION_DIM[0],
                           (self.time_explosion // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]  # which explosion sprite to draw

        current_explosion_center = [EXPLOSION_CENTER[0] + explosion_index[0] * EXPLOSION_SIZE[0],
                                    EXPLOSION_CENTER[1] + explosion_index[1] * EXPLOSION_SIZE[1]]  # the center of the explosion sprite to draw

        if self.animated and self.radius == ROCK_RADIUS:  # draw the rock
            canvas.draw_image(self.image, current_rock_center, self.image_size,
                              self.pos, self.image_size)

        elif self.animated and self.radius == r_EXPLOSION_RADIUS:  # draw the explosion
            canvas.draw_image(self.image, current_explosion_center,
                              self.image_size, self.pos, self.image_size)

        else:  # draw the missiles
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel

        if self.pos[0] > WIDTH + 20:  # wrap sprites around the canvas
            self.pos[0] = 0
        elif self.pos[0] < -20:
            self.pos[0] = WIDTH
        elif self.pos[1] > HEIGHT + 20:
            self.pos[1] = 0
        elif self.pos[1] < -20:
            self.pos[1] = HEIGHT

        self.time_explosion += 1  # going over explosion sprite sheet
        self.age += 0.9
        self.time_of_animation_asteroid += 0.2

        if self.age >= self.lifespan:  # if this returns true, the sprite will be deleted
            return True
        else:
            return False

    def collide(self, other_object):
        distance = dist(self.pos, other_object.get_position())
        if distance < (self.radius + other_object.get_radius()):  # calculate a collision between two objects
            return True
        return False

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius


def group_collide(set_group, other_object):  # calculate a collision between a group and an object
    is_collide = False
    for item in list(set_group):  # copy of the set so we can remove while iterating over
        if item.collide(other_object):
            set_group.remove(item)
            an_explosion = Sprite(item.get_position(), [0, 0], 0, 0,
                                  r_explosion_image, r_explosion_info, explosion_sound)
            explosion_group.add(an_explosion)  # creates a explosion object at collision location
            is_collide = True
    return is_collide


def group_group_collide(group_one, group_two):  # calculate a collision between two objects
    count_of_collide = 0
    for item in list(group_one):
        if group_collide(group_two, item):
            count_of_collide += 1
            group_one.remove(item)
    return count_of_collide


def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)

    if (not started) and inwidth and inheight:  # reset the game state
        started = True
        lives = 3
        score = 0
        timer.start()
        soundtrack.play()


def draw(canvas):
    global time, started, score, lives, animated_rock_group, explosion_group

    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw scores and lives
    canvas.draw_text("Score: " + str(score), [WIDTH - 150, 30], 30, 'white')
    canvas.draw_text("Lives: " + str(lives), [10, 30], 30, 'white')

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(animated_rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)

    # update ship and sprites
    my_ship.update()

    # ship, rock collision
    if group_collide(animated_rock_group, my_ship):  # returns true for any value other than 0
        explosion_group.add(Sprite(my_ship.get_position(), [0, 0], 0, 0,
                                   r_explosion_image, r_explosion_info, explosion_sound)) # create an explosion object
        lives -= 1

    # missile, rock collision
    if group_group_collide(animated_rock_group, missile_group):
        score += 10

    # splash screen
    if not started:
        timer.stop()  # stop spawning new rocks
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())
    # reset game
    if lives <= 0:
        animated_rock_group = set([])  # empty rocks
        started = False
        soundtrack.rewind()


def key_down(key):
    if key == simplegui.KEY_MAP['up']:
        my_ship.is_thrust(True)

    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

    my_ship.key_down(key)


def key_up(key):
    if key == simplegui.KEY_MAP['up']:
        my_ship.is_thrust(False)
    my_ship.key_up(key)


# timer handler that spawns a rock
def rock_spawner():
    global animated_rock_group
    velocity = [random.choice([random.random(), -random.random()]),
                random.choice([random.random(), -random.random()])]

    velocity[random.choice([0, 1])] += (score * 0.01)  # increases rock velocity with increasing of scores

    animated_rock = Sprite([random.randrange(1, WIDTH), random.randrange(1, HEIGHT)],
                           velocity, 0, 0, rock_image, rock_info)

    if len(animated_rock_group) <= 12 and dist(my_ship.get_position(), animated_rock.get_position()) > 90:
        animated_rock_group.add(animated_rock)  # draw rocks away from ship


def process_sprite_group(group_set, canvas):
    for item in list(group_set):
        item.draw(canvas)
        item.update()
        if item.update():  # if true, the item has exceeded its lifespan
            group_set.remove(item)


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and three sprite groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
missile_group = set([])
animated_rock_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)  # run handler every second

# Start game state
timer.start()
frame.start()
