import pygame
import math
from pygame.math import Vector2 as vec
from settings import *
import numpy as np
from main_test import *
from genome_ghost import *
from ghost import *

# Ghost 클래스 상속
class PinkGhost(Ghost):
    def __init__(self, Game, pos, speed, genome):
        self.Game = Game
        self.grid_pos = pos
        self.pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.speed = speed
        self.next_dir = vec(0,0)
        self.color = "Pink"
        self.old_direction = None
        self.direction = UP

        self.GhostGenome = genome
        self.fitness = 0

############################################# RUN ############################################

    def update(self):
        self.target = self.find_target()
        if self.target != self.grid_pos:
            if self.able_to_move:
                self.pix_pos += self.direction * self.speed

            if self.time_to_adjust():
                self.step()

            if self.time_to_move():
                self.learning_process()
                #self.move()
                if self.old_direction != None:
                    self.direction = self.old_direction
                self.able_to_move = self.wall_sensor()

        self.map_out_check()
        self.grid_pos_update()
        self.output_fitness_by_time()

########################################### HELPER FUCTIONS #############################################
    def move(self, direction):
        self.old_direction = direction

    def sense_player(self):
        sense_area = []
        # 4-방향으로 10칸 센서
        for i in range(4):
            for j in range(10):
                next_search_pos = vec(self.grid_pos + direcs[i] * (j + 1))
                if self.find_wall(next_search_pos):
                    break
                else:
                    sense_area.append(next_search_pos)
        if self.Game.player.grid_pos in sense_area:
            return True
        else:
            return False

    def step(self):
        if self.direction == RIGHT or self.direction == LEFT:
            for i in range(1,PINK_GHOST_SPEED):
                if int(self.pix_pos.x + self.direction.x*i + (SPACE * 2)) % (CELL) == 0 :
                    gap = i
            self.pix_pos += self.direction*gap

        elif self.direction == vec(0,1) or self.direction == UP:
            for i in range(1,PINK_GHOST_SPEED):
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
            if int(self.pix_pos.x + (SPACE * 2)) % (CELL) > CELL - PINK_GHOST_SPEED:
                return True
        if self.direction == LEFT:
            if int(self.pix_pos.x + (SPACE * 2)) % (CELL) < PINK_GHOST_SPEED and int(self.pix_pos.x + (SPACE * 2)) % (CELL) > 0:
                return True
        if self.direction == DOWN:
            if int(self.pix_pos.y + (SPACE * 2)) % (CELL) > CELL - PINK_GHOST_SPEED:
                return True
        if self.direction == UP:
            if int(self.pix_pos.y + (SPACE * 2)) % (CELL) < PINK_GHOST_SPEED and int(self.pix_pos.y + (SPACE * 2)) % (CELL) > 0 :
                return True

########################## AI Learning #############################
    def output_fitness_by_move(self):
        curr_pos = self.grid_pos
        next_pos = curr_pos + self.direction

        # 벽이면
        if next_pos in self.Game.walls or next_pos in self.Game.ghost_house:
            self.fitness += GHOST_FIT_move_to_wall
        # 좌표의 이동이 있다면
        elif curr_pos != next_pos:
            self.fitness += GHOST_FIT_move
        # 플레이어를 감지하면
        if self.sense_player():
            self.fitness += GHOST_FIT_sense_player
        #180도 이동하면
        if self.is_opposide(self.old_direction) == self.direction:
            self.fitness += GHOST_FIT_180_move

    def output_fitness_by_time(self):
        time = self.Game.fps_after_start
        if time % 20 != 0:
            self.before_pos = self.grid_pos
        else:
            before_pos = self.before_pos
            curr_pos = self.grid_pos
            target_pos = self.find_target()
            dist_before = math.sqrt(math.pow((before_pos.x - target_pos.x), 2) + math.pow((before_pos.y - target_pos.y), 2))
            dist_curr = math.sqrt(math.pow((curr_pos.x - target_pos.x), 2) + math.pow((curr_pos.y - target_pos.y), 2))

            # 움직이지 않으면
            if self.before_pos == self.grid_pos:
                self.fitness += GHOST_FIT_do_not_move
            else:
                # 플레이어에 가까워지면
                if dist_curr < dist_before:
                    self.fitness += GHOST_FIT_close_player
                    # print("close player: ", self.fitness)
                # 플레이어에 멀어지면
                else:
                    self.fitness += GHOST_FIT_far_player
                    # print("far player: ", self.fitness)

    def is_opposide(self, former_dir):
        if former_dir == UP:
            opposide = DOWN
        elif former_dir == DOWN:
            opposide = UP
        elif former_dir == LEFT:
            opposide = RIGHT
        elif former_dir == RIGHT:
            opposide = LEFT
        else:
            opposide = (0,0)
        return opposide

    def get_input(self):
        #genome_input = [빨강유령 이동방향, x좌표, y좌표, 파랑유령 이동방향, x좌표, y좌표, 초록유령 이동방향, x좌표, y좌표, 벽]
        self.genome_input = []

        dir_list = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]

        # 빨강유령 input
        for i,dir in enumerate(dir_list):
            if self.Game.red_ghost.direction == dir:
                self.genome_input.append(i)
                break
        self.genome_input.append(self.Game.red_ghost.grid_pos.x)
        self.genome_input.append(self.Game.red_ghost.grid_pos.y)

        # 파랑유령 input
        if self.Game.blue_ghost.sense_player():
            for i,dir in enumerate(dir_list):
                if self.Game.blue_ghost.direction == dir:
                    self.genome_input.append(i)
                    break
            self.genome_input.append(self.Game.blue_ghost.grid_pos.x)
            self.genome_input.append(self.Game.blue_ghost.grid_pos.y)
        else:
            self.genome_input.append(5.)
            self.genome_input.append(0.)
            self.genome_input.append(0.)

        # 초록유령 input
        # if self.Game.fps_after_start > 150:
        self.genome_input.append(5.)
        self.genome_input.append(0.)
        self.genome_input.append(0.)

        # 벽 input
        if not self.wall_sensor():
            # 벽이면 1
            self.genome_input.append(1.)
        else:
            # 벽 아니면 0
            self.genome_input.append(0.)

        return self.genome_input

    def learning_process(self):
        inputs = self.get_input()
        outputs = self.GhostGenome.forward(inputs)
        outputs = np.argmax(outputs)
        if outputs == 0:
            self.direction = UP
        elif outputs == 1:
            self.direction = DOWN
        elif outputs == 2:
            self.direction = LEFT
        elif outputs == 3:
            self.direction = RIGHT

        if self.grid_pos in self.Game.ghost_house:
            self.direction = UP

        self.output_fitness_by_move()

        #di = ["↑", "↓","←", "→", "ERROR"]
        #print("신경망 inputs: "+str(inputs)+" //outputs: "+str(outputs), di[outputs])
        #return self.next_dir

####################### DRAWING #######################

    def get_image(self):
        image = pink_up
        if self.direction == vec(0, 0):
            image = pink_right
        elif self.direction == UP:
            image = pink_up
        elif self.direction == DOWN:
            image = pink_down
        elif self.direction == RIGHT:
            image = pink_right
        elif self.direction == LEFT:
            image = pink_left
        return image

    def stop(self):
        cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)
        self.speed = 0
        self.Game.screen.blit(self.get_image(), cur_pos)

    def draw(self):
        cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)

        # stop 후 다시 움직이기 시작할 때
        if self.speed == 0:
            self.speed = PINK_GHOST_SPEED

        self.Game.screen.blit(self.get_image(), cur_pos)
