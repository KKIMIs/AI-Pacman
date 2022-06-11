import pygame
import sys
from settings import *
from pygame.math import Vector2 as vec
from class_player import *
from ghost import *
from red_ghost import *
from green_ghost import *
from blue_ghost import *
from pink_ghost import *

pygame.init()
vec = pygame.math.Vector2

icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Pac-Man")

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = 'intro'
        self.stage = 1
        self.walls = []
        self.aisle = []
        self.coins = []
        self.ghost_house = []
        self.player = Player(self, PLAYER_START_POS,PlAYER_SPEED, genome = None)
        self.green_ghost = GreenGhost(self, GREEN_GHOST_START_POS, GREEN_GHOST_SPEED)
        self.red_ghost = RedGhost(self, RED_GHOST_START_POS, RED_GHOST_SPEED)
        self.pink_ghost = PinkGhost(self, PINK_GHOST_START_POS, PINK_GHOST_SPEED)
        self.blue_ghost = BlueGhost(self, BLUE_GHOST_START_POS, BLUE_GHOST_SPEED)
        self.load()
        self.fps_after_start = 0

    def run(self):
        while self.running:
            self.fps_after_start += 1
            if self.scene == 'intro':
                self.get_intro_events()
                self.draw_intro_scene()
            elif self.scene == 'play':
                self.get_play_events()
                self.update_play_scene()
                self.draw_play_scene()
            elif self.scene == 'game over':
                self.get_game_over_events()
                self.draw_game_over_scene()
            else:
                self.running = False
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

############################ HELPER FUNCTIONS ##################################

    def load(self):
        self.background = pygame.image.load('images/map.png')
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (SPACE, SPACE))

        with open("structure.txt", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(x, y))
                    if char == "A":
                        self.aisle.append(vec(x, y))
                    if char == "x" or char=="-":
                        self.ghost_house.append(vec(x, y))

    def fill_up_coins(self):
        with open("structure.txt", 'r') as file:

            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "0":
                        self.coins.append(vec(x, y))

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, YELLOW,
                               (int((coin.x * CELL) + (SPACE * 2)), int((coin.y * CELL) + (SPACE * 2))), 3)

    def draw_text(self, sentence, pos):
        font = pygame.font.SysFont('broadway', 25)
        text = font.render(sentence, True, WHITE)
        self.screen.blit(text, pos)

    def clear_bottom(self):
        self.screen.fill(BLACK, rect=(0, BG_HEIGHT + SPACE, SCREEN_WIDTH, SCREEN_HEIGHT))

    def put_obj_back(self):
        self.player.reset()
        self.green_ghost.reset()
        self.red_ghost.reset()
        self.blue_ghost.reset()
        self.pink_ghost.reset()

    def freeze_obj(self):
        self.player.stop()
        self.pink_ghost.stop()
        self.green_ghost.stop()
        self.red_ghost.stop()
        self.blue_ghost.stop()

    def draw_grid(self):
        for x in range(ROW + 1):
            pygame.draw.line(self.screen, GREY, (x * CELL + SPACE, SPACE), (x * CELL + SPACE, BG_HEIGHT + SPACE))

        for y in range(COLUMN + 1):
            pygame.draw.line(self.screen, GREY, (SPACE, y * CELL + SPACE), (BG_WIDTH + SPACE, y * CELL + SPACE))

        for wall in self.walls:
            pygame.draw.rect(self.screen, GREY, (wall.x * CELL + SPACE, wall.y * CELL + SPACE, CELL, CELL))


########################### INTRO FUNCTIONS ####################################

    def get_intro_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.scene = 'play'
                self.fill_up_coins()

    def draw_intro_scene(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (SPACE,SPACE))
        self.draw_coins()
        self.freeze_obj()
        self.draw_text('Press the space bar to start!', (105, 640))
        pygame.display.update()

########################### PLAYING FUNCTIONS ##################################

    def get_play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(LEFT)
                if event.key == pygame.K_RIGHT:
                    self.player.move(RIGHT)
                if event.key == pygame.K_UP:
                    self.player.move(UP)
                if event.key == pygame.K_DOWN:
                    self.player.move(DOWN)

    def update_play_scene(self):
        if self.door_is_closed() == False and self.ghost_in_house() == False:
            self.close_the_door()

        if self.bump() == True:
            self.lose_life()

        if self.clear_stage() == True:
            self.reset()

        self.player.update()
        self.green_ghost.update()
        self.red_ghost.update()
        self.blue_ghost.update()
        self.pink_ghost.update()

    def ghost_in_house(self):
        house_pos = [vec(12, 13), vec(13, 11), vec(13, 12), vec(13, 13), vec(14, 11), vec(14, 12), vec(14, 13), vec(15, 13)]
        ghosts_pos = [self.blue_ghost.grid_pos, self.red_ghost.grid_pos, self.green_ghost.grid_pos, self.pink_ghost.grid_pos]

        for ghost in ghosts_pos:
            if ghost in house_pos:
                return True
        return False

    def door_is_closed(self):
        door_pos = [vec(13, 11), vec(14, 11)]
        for door in door_pos:
            if door in self.walls:
                return True
        return False

    def close_the_door(self):
        door_pos = [vec(13, 11), vec(14, 11)]

        for door in door_pos:
            self.walls.append(door)

    def open_the_door(self):
        door_pos = [vec(13, 11), vec(14, 11)]
        for door in door_pos:
            self.walls.remove(door)

    def bump(self):
        ghosts_pos = [self.blue_ghost.grid_pos, self.red_ghost.grid_pos, self.green_ghost.grid_pos, self.pink_ghost.grid_pos]

        if self.player.grid_pos in ghosts_pos:
            return True
        return False

    def lose_life(self):
        self.freeze_obj()
        self.player.lives -= 1

        if self.player.lives == 0:
            self.scene = 'game over'
            return

        pygame.time.delay(1000)
        self.erase_live()
        self.put_obj_back()
        if self.door_is_closed() == True:
            self.open_the_door()
        self.fps_after_start = 0

    def clear_stage(self):
        if len(self.coins) <= 0:
            return True
        return False

    def reset(self):
        self.fill_up_coins()
        self.put_obj_back()
        if self.door_is_closed() == True:
            self.open_the_door()
        self.stage += 1
        pygame.time.delay(1000)
        self.fps_after_start = 0

    def draw_play_scene(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (SPACE, SPACE))
        #self.draw_grid()
        self.draw_coins()
        self.player.draw()
        self.green_ghost.draw()
        self.blue_ghost.draw()
        self.red_ghost.draw()
        self.pink_ghost.draw()
        self.clear_bottom()
        self.draw_stage()
        self.draw_lives()
        pygame.display.update()

    def draw_stage(self):
        self.draw_text('stage ' + str(self.stage), (30, 640))

    def draw_lives(self):
        live = pygame.image.load('images/live.png')
        live = pygame.transform.scale(live, (25, 25))
        for i in range(self.player.lives):
            self.screen.blit(live, (LIVE_START_POS_X + (i * 37), LIVE_START_POS_Y))

    def erase_live(self):
        gap = TOTAL_LIVES - self.player.lives
        self.screen.fill(BLACK, rect=(LIVE_START_POS_X + (37 * gap), LIVE_START_POS_Y + 25, LIVE_START_POS_X + (37 * gap) + 25, LIVE_START_POS_Y + 25))

########################### GAME OVER FUNCTIONS ################################

    def get_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.restart()

    def draw_game_over_scene(self):
        self.clear_bottom()
        self.draw_text('Game over! Your record : ' + 'stage ' + str(self.stage), (70, 640))
        pygame.display.update()

    def restart(self):
        self.stage = 1
        self.player.lives = 3
        self.coins = []
        self.fill_up_coins()
        self.put_obj_back()
        self.scene = 'play'
        self.fps_after_start = 0

if __name__ == '__main__':
    game = Game()
    game.run()
