import pygame
from pygame.math import Vector2 as vec
import random

# screen settings
BG_WIDTH, BG_HEIGHT = 560, 620
SPACE = 10
BOTTOM_SPACE = 40
SCREEN_WIDTH, SCREEN_HEIGHT = BG_WIDTH+(SPACE*2), BG_HEIGHT+(SPACE*2)+BOTTOM_SPACE
ROW, COLUMN = 28, 31
CELL = 20
FPS = 30

# live settings
LIVE_START_POS_X, LIVE_START_POS_Y = 450, 640
TOTAL_LIVES = 3

# define color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (173, 173, 173)
YELLOW = (250, 255, 165)
BROWN = (165, 42, 42)
GREEN = (0, 185, 25)
BLUE = (135, 206, 235)
PINK = (255,192,203)

# define direction
UP = vec(0, -1)
DOWN = vec(0, 1)
LEFT = vec(-1, 0)
RIGHT = vec(1, 0)
direcs = [ RIGHT, LEFT, UP, DOWN ]

# player settings
PLAYER_START_POS = vec(1,29)
def set_new_pos():
    ran_num = random.randint(0,1)
    START_POS_LIST = [vec(26,1), vec(1,29)]
    return START_POS_LIST[ran_num]
PLAYER_SPEED = 5

# player fitness
PLAYER_FIT_eatCoin = 5.
PLAYER_FIT_neartoCoin = 0.7
PLAYER_FIT_farfromCoin = -0.5
PLAYER_FIT_neartoGhost = -2.0
PLAYER_FIT_farfromGhost = 2.5
PLAYER_FIT_bump = -200
PLAYER_FIT_timeout = -150

# ghost fitness
#GHOST_FIT_indir_bump = 30.
GHOST_FIT_dir_bump = 200.
GHOST_FIT_move_to_wall = -20.
GHOST_FIT_move = 15.
GHOST_FIT_sense_player = 20.
GHOST_FIT_far_player = -10
GHOST_FIT_close_player = 5.5
GHOST_FIT_do_not_move = -10.
GHOST_FIT_180_move = -5


# player images
TOTAL_PACMAN_FRAMES = 5
openess_0 = pygame.image.load('images/openess_0.png')

openess_1_right = pygame.image.load('images/openess_1.png')
openess_2_right = pygame.image.load('images/openess_2.png')
openess_3_right = pygame.image.load('images/openess_3.png')
openess_4_right = pygame.image.load('images/openess_4.png')

openess_1_up = pygame.transform.rotate(openess_1_right, 90)
openess_2_up = pygame.transform.rotate(openess_2_right, 90)
openess_3_up = pygame.transform.rotate(openess_3_right, 90)
openess_4_up = pygame.transform.rotate(openess_4_right, 90)

openess_1_left = pygame.transform.rotate(openess_1_up, 90)
openess_2_left = pygame.transform.rotate(openess_2_up, 90)
openess_3_left = pygame.transform.rotate(openess_3_up, 90)
openess_4_left = pygame.transform.rotate(openess_4_up, 90)

openess_1_down = pygame.transform.rotate(openess_1_left, 90)
openess_2_down = pygame.transform.rotate(openess_2_left, 90)
openess_3_down = pygame.transform.rotate(openess_3_left, 90)
openess_4_down = pygame.transform.rotate(openess_4_left, 90)

# ghost settings
GREEN_GHOST_START_POS = vec(12,13)
RED_GHOST_START_POS = vec(13,13)
PINK_GHOST_START_POS = vec(14,13)
BLUE_GHOST_START_POS = vec(15,13)
GREEN_GHOST_SPEED = 2
RED_GHOST_SPEED = 3
PINK_GHOST_SPEED = 5
BLUE_GHOST_SPEED = 1

# ghost images
red_right = pygame.image.load('images/red_right.png')
red_left = pygame.image.load('images/red_left.png')
red_up = pygame.image.load('images/red_up.png')
red_down = pygame.image.load('images/red_down.png')

green_right = pygame.image.load('images/green_right.png')
green_left = pygame.image.load('images/green_left.png')
green_up = pygame.image.load('images/green_up.png')
green_down = pygame.image.load('images/green_down.png')

blue_right = pygame.image.load('images/blue_right.png')
blue_left = pygame.image.load('images/blue_left.png')
blue_up = pygame.image.load('images/blue_up.png')
blue_down = pygame.image.load('images/blue_down.png')

pink_right = pygame.image.load('images/pink_right.png')
pink_left = pygame.image.load('images/pink_left.png')
pink_up = pygame.image.load('images/pink_up.png')
pink_down = pygame.image.load('images/pink_down.png')
