# snake game
import sys, pygame, random, time

check_errors  = pygame.init()

if check_errors[1] > 0:
    print("Had {0} initializing errors...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("Pygame successfully initialized.")


# play surface

fps = 10
play_surface = pygame.display.set_mode((700, 460))
pygame.display.set_caption("Snake Game")

# colors

red = pygame.Color(255, 0, 0) # game over
blue = pygame.Color(0, 255, 0) # snake
green = pygame.Color(0, 0, 255)
black = pygame.Color(0, 0, 0) # score
white = pygame.Color(255, 255, 255) # background
brown = pygame.Color(165, 42, 42) # food


# FPS Controller

fps_controller = pygame.time.Clock()


# important variables

snakePos = [100, 50]

snakeBody = [[100, 50], [90, 50], [80, 50]]

foodPos = [random.randrange(1, 71)*10, random.randrange(1, 45)*10]

foodSpawn = True

direction = 'RIGHT'

changeTo = direction

score = 0

# Game Over Function

def gameover():
    myFont = pygame.font.SysFont('Sans Serif', 72)
    GOsurf = myFont.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 120)
    play_surface.blit(GOsurf, GOrect)
    showscore(2)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit() # window exit
    sys.exit() # console exit

def showscore(choice=1):
    sFont = pygame.font.SysFont('Monaco', 24)
    Ssurf = sFont.render("Score : " + str(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (50, 10)
    else:
        Srect.midtop = (360, 220)
    play_surface.blit(Ssurf, Srect)


# Game Logic

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                changeTo = "RIGHT"
            elif event.key == pygame.K_LEFT or event.key == ord("a"):
                changeTo = "LEFT"
            elif event.key == pygame.K_UP or event.key == ord("w"):
                changeTo = "UP"
            elif event.key == pygame.K_DOWN or event.key == ord("s"):
                changeTo = "DOWN"
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # validation of direction
    if changeTo == "RIGHT" and not direction == "LEFT":
        direction = "RIGHT"
    elif changeTo == "LEFT" and not direction == "RIGHT":
        direction = "LEFT"
    elif changeTo == "DOWN" and not direction == "UP":
        direction = "DOWN"
    elif changeTo == "UP" and not direction == "DOWN":
        direction = "UP"

    if direction == "RIGHT":
        snakePos[0] += 10
    if direction == "LEFT":
        snakePos[0] -= 10
    if direction == "UP":
        snakePos[1] -= 10
    if direction == "DOWN":
        snakePos[1] += 10

    # snake body mechanism

    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 5
        fps += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    if foodSpawn == False:
        foodPos = [random.randrange(1, 70) * 10, random.randrange(1, 46) * 10]
    foodSpawn = True

    play_surface.fill(white)
    for position in snakeBody:
        pygame.draw.rect(play_surface, green,
        pygame.Rect(position[0], position[1], 10, 10))

    pygame.draw.rect(play_surface, brown,
                     pygame.Rect(foodPos[0], foodPos[1], 10, 10))


    if snakePos[0] > 710 or snakePos[0] < 0:
        gameover()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameover()

    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameover()

    showscore()
    pygame.display.flip()
    fps_controller.tick(fps)


