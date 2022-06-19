import pygame
from pygame.math import Vector2 as vec
import numpy as np
from settings import *
from main_test import *
from ghost import *
from genome_player import *

vec = pygame.math.Vector2

class Player:
    def __init__(self, Game, pos, speed, genome):
        self.Game = Game
        self.pos = pos
        self.grid_pos = pos
        self.direction = RIGHT
        self.old_direction = None
        self.pix_pos = self.get_pix_pos()
        self.able_to_move = False
        self.image = openess_2_right
        self.cur_frame = 0
        self.next_frame = 0
        self.speed = speed
        self.lives = 3

        self.num_sensor = 10
        self.coin_sensor = np.zeros((4,self.num_sensor))
        self.ghost_sensor = np.zeros((4,self.num_sensor))

        #유전자 정보와 적합도 추가
        self.p_genome = genome
        self.fitness = 0
        self.last_dist_coins = np.inf
        self.last_dist_ghosts = [0,0,0,0]
        self.genome_input = [1.,1.,1.,1.,1.,1.,1.,1.,0]
        self.time_out_counter = 0

    def reset(self):
        self.grid_pos = vec(self.pos)
        self.pix_pos = self.get_pix_pos()
        self.direction = RIGHT
        self.old_direction = None
        self.able_to_move = False
        self.coin_sensor = np.zeros((4,self.num_sensor))
        self.ghost_sensor = np.zeros((4,self.num_sensor))
        self.last_dist_coins = np.inf
        self.last_dist_ghosts = [0,0,0,0]
        self.genome_input = [1.,1.,1.,1.,1.,1.,1.,1.,0]
        self.time_out_counter = 0

############################################# RUN ############################################

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed

        if self.time_to_adjust():
            self.step()

        if self.time_to_move():
            self.p_learning_process()
            if self.old_direction != None:
                self.direction = self.old_direction
            self.able_to_move = self.wall_sensor()

        self.map_out_check()
        self.grid_pos_update()

        if self.on_coin():
            if self.time_to_move():
                self.eat_coin()

        self.sense_coins()
        self.compute_coin_dist()
        self.sense_ghosts()
        self.compute_ghost_dist()

########################################### HELPER FUCTIONS #############################################

    def move(self, direction):
        self.old_direction = direction

    def step(self):
        if self.direction == RIGHT or self.direction == LEFT:
            for i in range(1,PlAYER_SPEED):
                if int(self.pix_pos.x + self.direction.x*i + (SPACE * 2)) % (CELL) == 0 :
                    gap = i
            self.pix_pos += self.direction*gap

        elif self.direction == vec(0,1) or self.direction == UP:
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

################################FITNESS#################################

    def eat_coin(self):
        # 코인을 먹으면 fitness +3
        # if self.time_to_move():
        self.fitness += PLAYER_FIT_eatCoin
        # print("++++eat coin+++++" ,self.fitness)
        self.Game.coins.remove(self.grid_pos)
        self.time_out_counter = 0

    def draw_nearest(self):
        if nearest_c:
            pos_x = nearest_c[0]
            pos_y = nearest_c[1]
            pygame.draw.rect(self.Game.screen, YELLOW, (pos_x* CELL + SPACE, pos_y * CELL + SPACE, CELL, CELL))
        if nearest_g:
            pos_x = nearest_g[0]
            pos_y = nearest_g[1]
            pygame.draw.rect(self.Game.screen, GREY, (pos_x* CELL + SPACE, pos_y * CELL + SPACE, 35, 35))

    def compute_coin_dist(self):
        found = False
        nearest_c = None
        #제일 가까운 코인 찾기
        for i in range(self.num_sensor):
            for h in range(4):
                if self.coin_sensor[h][i] == 1:
                    nearest_c = vec(self.grid_pos + direcs[h]*(i+1))
                    found = True
            if found:
                break
        if nearest_c not in self.Game.coins:
            nearest_c = None
            found = False
        #코인과의 거리 계산
        # 코인과 가까워지면 fitness +0.5 멀어지면 -0.5
        if nearest_c:
            curr_dist_coins = np.linalg.norm(self.grid_pos - nearest_c)
            if self.last_dist_coins > curr_dist_coins:
                # print("++++near to coin+++++" ,self.fitness)
                self.fitness += PLAYER_FIT_neartoCoin
            elif self.last_dist_coins < curr_dist_coins:
                # print("++++far from coin+++++" ,self.fitness)
                self.fitness += PLAYER_FIT_farfromCoin
            self.last_dist_coins = curr_dist_coins

    def compute_ghost_dist(self):
        # 플레이어 상, 하, 좌, 우 5칸 정사각형 내에서 유령 거리 계산
        # 범위 설정
        area = []
        num_sensor = self.num_sensor
        for xidx in range(int(self.grid_pos[0])-num_sensor,int(self.grid_pos[0])+num_sensor+1,1):
            for yidx in range(int(self.grid_pos[1])-num_sensor,int(self.grid_pos[1])+num_sensor+1,1):
                area.append(vec(xidx,yidx))
        near_ghost=[self.Game.green_ghost.grid_pos, self.Game.red_ghost.grid_pos,
        self.Game.blue_ghost.grid_pos, self.Game.pink_ghost.grid_pos]
        curr_dist_ghosts = [0,0,0,0]

        if self.time_to_move():
            for i in range(4):
                if near_ghost[i] in area:
                    curr_dist_ghosts[i] = np.linalg.norm(self.grid_pos - near_ghost[i])
                else:
                    curr_dist_ghosts[i] = 0
            # if self.Game.fps_after_start % 90 == 0:
            #     print("last_dist_ghosts:",self.last_dist_ghosts)
            #     print("curr_dist_ghosts:",curr_dist_ghosts)

            for i in range(4):
                if curr_dist_ghosts[i] != 0 and self.last_dist_ghosts[i] != 0:
                    if self.last_dist_ghosts[i] > curr_dist_ghosts[i]:
                        self.fitness += PLAYER_FIT_neartoGhost
                        # print("++++near to GHOST+++++" ,self.fitness)

                    elif self.last_dist_ghosts[i] < curr_dist_ghosts[i]:
                        self.fitness += PLAYER_FIT_farfromGhost
                        # print("++++far from GHOST+++++" ,self.fitness)
                self.last_dist_ghosts[i] = curr_dist_ghosts[i]

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
        for h in range(4):
            for i in range(self.num_sensor):
                next_pos = vec(self.grid_pos + direcs[h]*(i+1))
                if self.find_wall(next_pos):
                    for j in range(i, self.num_sensor):
                        self.coin_sensor[h,j] = 2
                    break
                else:
                    if next_pos in self.Game.coins:
                        self.coin_sensor[h,i] = 1
                    else:
                        self.coin_sensor[h,i] = 0

    def sense_ghosts(self):
        for h  in range(4):
            for i in range(self.num_sensor):
                next_pos = vec( self.grid_pos + direcs[h]*(i+1))
                if self.find_wall(next_pos):
                    for j in range(i, self.num_sensor):
                        self.ghost_sensor[h,j] = 2
                    break
                else:
                    if (next_pos == self.Game.green_ghost.grid_pos or next_pos== self.Game.red_ghost.grid_pos
                        or next_pos== self.Game.blue_ghost.grid_pos or next_pos == self.Game.pink_ghost.grid_pos):
                        self.ghost_sensor[h,i] = 1
                    else:
                        self.ghost_sensor[h,i] = 0
        # 상태 = (0: 없음, 1: 있음, 2: 모름)


    def get_p_genome_input(self):
        #genome_input = [코인-우, 코인-좌, 코인-상, 코인-하, 유령-우, 유령-좌, 유령-상, 유령-하
                #+ 다음 벽 True/False]
        # 0 - 0.2 - 0.4 - 0.6 - 0.8 - 1 (near.........far)
        for i in range(4):
            for j in range(self.num_sensor):
                if self.coin_sensor[i,j] == 1:
                    self.genome_input[i] = 0.2 * j
                    break
                else:
                    self.genome_input[i] = 1.
            for h in range(self.num_sensor):
                if self.ghost_sensor[i,h] == 1:
                    self.genome_input[i+4] = 0.2 * j
                    break
                else:
                    self.genome_input[i+4] = 1.
            next_pos = vec( self.grid_pos + direcs[i]*(1))
        if not self.wall_sensor():
            #벽이면 1
            self.genome_input[8] = 1.
        else:
            #벽 아니면 0
            self.genome_input[8] = 0.

        return self.genome_input

    def p_learning_process(self):
        inputs = self.get_p_genome_input()
        outputs = self.p_genome.forward(inputs)
        outputs = np.argmax(outputs)

        if outputs == 0:
            self.direction = RIGHT
        elif outputs == 1:
            self.direction = LEFT
        elif outputs == 2:
            self.direction = UP
        elif outputs == 3:
            self.direction = DOWN

        # di = [ "→", "←", "↑",  "↓" ]
        # if self.Game.fps_after_start % 90 == 0:
        #      print("신경망 inputs: "+str(inputs)+" //outputs: "+str(outputs), di[outputs],"fitness",self.fitness)

########################################### ANIMATION FUCTIONS #############################################

    def draw(self):
        #if self.Game.fps_after_start % 90 == 0:
            #print("Fitness: %s" % self.fitness)
        #self.draw_nearest()
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
