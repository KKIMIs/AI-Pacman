import pygame
from pygame.math import Vector2 as vec
import numpy as np
from settings import *
from main_test import *
from ghost import *

vec = pygame.math.Vector2

class Player:
    def __init__(self, Game, pos, speed, genome):
        self.Game = Game
        self.pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.direction = RIGHT
        self.old_direction = None
        self.pix_pos = self.get_pix_pos()
        self.able_to_move = True
        self.image = openess_2_right
        self.cur_frame = 0
        self.next_frame = 0
        self.speed = speed
        self.lives = 3
        self.coin_sensor = np.zeros((4,5))
        self.ghost_sensor = np.zeros((4,5))

        self.genome = genome
        self.fitness = 0
        self.last_dist_coins = np.inf
        self.last_dist_ghosts = np.inf
        
    def reset(self):
        self.grid_pos = vec(self.pos)
        self.pix_pos = self.get_pix_pos()
        self.direction = RIGHT
        self.old_direction = None
        self.able_to_move = True

############################################# RUN ############################################

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed

        if self.time_to_adjust():
            self.step()

        if self.time_to_move():
            if self.old_direction != None:
                self.direction = self.old_direction
            self.able_to_move = self.wall_sensor()
            #print("코인: 상",self.coin_sensor[2,:],"/하",self.coin_sensor[3,:],"/좌",self.coin_sensor[1,:],"/우",self.coin_sensor[0,:])
            #print("유령: 상",self.ghost_sensor[2,:],"/하",self.ghost_sensor[3,:],"/좌",self.ghost_sensor[1,:],"/우",self.ghost_sensor[0,:])

        self.map_out_check()
        self.grid_pos_update()

        if self.on_coin():
            self.eat_coin()

        self.sense_coins()
        self.sense_ghosts()

########################################### HELPER FUCTIONS #############################################

    def move(self, direction):
        self.old_direction = direction

    def step(self):
        if self.direction == RIGHT or self.direction == LEFT:
            for i in range(1,PlAYER_SPEED):
                if int(self.pix_pos.x + self.direction.x*i + (SPACE * 2)) % (CELL) == 0 :
                    gap = i
            self.pix_pos += self.direction*gap

        elif self.direction == DOWN or self.direction == UP:
            for i in range(1,PlAYER_SPEED):
                if int(self.pix_pos.y + self.direction.y*i + (SPACE * 2)) % (CELL) == 0 :
                    gap = i
            self.pix_pos += self.direction*gap


    def get_pix_pos(self):
        return vec((self.grid_pos.x * CELL + SPACE + CELL // 2), (self.grid_pos.y * CELL + SPACE + CELL // 2))

    def grid_pos_update(self):
        self.grid_pos[0] = (self.pix_pos[0] - (SPACE * 2) + (CELL // 2)) // CELL
        self.grid_pos[1] = (self.pix_pos[1] - (SPACE * 2) + (CELL // 2)) // CELL

    def map_out_check(self):
        if self.pix_pos.x < SPACE and self.direction == LEFT:
            self.pix_pos.x = BG_WIDTH+SPACE

        elif self.pix_pos.x > BG_WIDTH+SPACE and self.direction == RIGHT:
            self.pix_pos.x = SPACE

    def time_to_move(self):
        if int(self.pix_pos.x + (SPACE * 2)) % (CELL) == 0:
            if self.direction == RIGHT or self.direction == LEFT or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + (SPACE * 2)) % (CELL) == 0:
            if self.direction == DOWN or self.direction == UP or self.direction == vec(0, 0):
                return True

    def time_to_adjust(self):
        if self.direction == RIGHT:
            if int(self.pix_pos.x + (SPACE * 2)) % (CELL) > CELL - PlAYER_SPEED:
                return True
        if self.direction == LEFT:
            if int(self.pix_pos.x + (SPACE * 2)) % (CELL) < PlAYER_SPEED and int(self.pix_pos.x + (SPACE * 2)) % (CELL) > 0:
                return True
        if self.direction == DOWN:
            if int(self.pix_pos.y + (SPACE * 2)) % (CELL) > CELL - PlAYER_SPEED:
                return True
        if self.direction == UP:
            if int(self.pix_pos.y + (SPACE * 2)) % (CELL) < PlAYER_SPEED and int(self.pix_pos.y + (SPACE * 2)) % (CELL) > 0 :
                return True

    def on_coin(self):
        if self.grid_pos in self.Game.coins:
            return True
        return False

    def eat_coin(self):
        self.Game.coins.remove(self.grid_pos)


########################################### SENSOR FUCTIONS #############################################

    def wall_sensor(self):
        next_pos = vec(self.grid_pos + self.direction)
        for wall in self.Game.walls:
            if next_pos == wall:
                return False
        return True

    def find_wall(self, pos):
        for wall in self.Game.walls:
            if pos == wall:
                return True
        return False

    # 4-방향 센서 :  2차원 배열 ( 1st 행: right / 2nd 행: left / 3rd 행: up / 4rd 행: down)
    def sense_coins(self):
        for h  in range(4):
            for i in range(5):
                next_pos = vec( self.grid_pos + direcs[h]*(i+1))
                if self.find_wall(next_pos):
                    for j in range(i, 5):
                        self.coin_sensor[h,j] = 2
                    break
                else:
                    if next_pos in self.Game.coins:
                        self.coin_sensor[h,i] = 1
                    else:
                        self.coin_sensor[h,i] = 0

    def sense_ghosts(self):
        for h  in range(4):
            for i in range(5):
                next_pos = vec( self.grid_pos + direcs[h]*(i+1))
                if self.find_wall(next_pos):
                    for j in range(i, 5):
                        self.ghost_sensor[h,j] = 2
                    break
                else:
                    if (next_pos == self.Game.green_ghost.grid_pos or next_pos== self.Game.red_ghost.grid_pos
                        or next_pos== self.Game.blue_ghost.grid_pos or next_pos == self.Game.pink_ghost.grid_pos):
                        self.ghost_sensor[h,i] = 1
                    else:
                        self.ghost_sensor[h,i] = 0
        # 상태 = (0: 없음, 1: 있음, 2: 모름)

########################################### ANIMATION FUCTIONS #############################################

    def draw(self):
        cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)

        # stop 후 다시 움직일 때
        if self.speed == 0:
            self.speed = PlAYER_SPEED

        # 원 위치로 돌아간 후 다시 움직일 때
        if self.direction == vec(0, 0):
            self.direction = RIGHT

        # 벽에 부딪히면 입을 움직이지 않음
        if self.wall_sensor() == False:
            if self.direction == UP:
                self.Game.screen.blit(openess_3_up, cur_pos)
            elif self.direction == DOWN:
                self.Game.screen.blit(openess_3_down, cur_pos)
            elif self.direction == LEFT:
                self.Game.screen.blit(openess_3_left, cur_pos)
            elif self.direction == RIGHT:
                self.Game.screen.blit(openess_3_right, cur_pos)
            return

        self.animate(cur_pos)

    def animate(self, position):
        right_frames = [openess_0, openess_1_right, openess_2_right, openess_3_right, openess_4_right]
        left_frames = [openess_0, openess_1_left, openess_2_left, openess_3_left, openess_4_left]
        up_frames = [openess_0, openess_1_up, openess_2_up, openess_3_up, openess_4_up]
        down_frames = [openess_0, openess_1_down, openess_2_down, openess_3_down, openess_4_down]

        clock = pygame.time.get_ticks()

        if clock > self.next_frame:
            self.cur_frame = (self.cur_frame + 1) % TOTAL_PACMAN_FRAMES
            self.next_frame = clock + 65
            if self.direction == UP:
                self.image = up_frames[self.cur_frame]
            elif self.direction == DOWN:
                self.image = down_frames[self.cur_frame]
            elif self.direction == LEFT:
                self.image = left_frames[self.cur_frame]
            elif self.direction == RIGHT:
                self.image = right_frames[self.cur_frame]

        self.Game.screen.blit(self.image, position)

    def stop(self):
        cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)
        self.speed = 0

        if self.direction == UP:
            self.image = openess_3_up
        elif self.direction == DOWN:
            self.image = openess_3_down
        elif self.direction == LEFT:
            self.image = openess_3_left
        elif self.direction == RIGHT:
            self.image = openess_3_right

        self.Game.screen.blit(self.image, cur_pos)
