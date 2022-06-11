import pygame
import math
from pygame.math import Vector2 as vec
from settings import *
from main_test import *
from ghost import *

# Ghost 클래스 상속
class PinkGhost(Ghost):
    def __init__(self, Game, pos, speed):
        self.Game = Game
        self.grid_pos = pos
        self.pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.speed = speed
        self.centroid_pos = None
        self.next_dir = UP
        self.color = "Pink"


####################### MOVING #######################

    # 현위치와 무게중심 거리 차이 계산
    def calculate_distance(self, pos):
        red_pos = self.Game.red_ghost.grid_pos
        blue_pos = self.Game.blue_ghost.grid_pos
        green_pos = self.Game.green_ghost.grid_pos
        centroid_x = int((red_pos.x + blue_pos.x + green_pos.x) // 3)
        centroid_y = int((red_pos.y + blue_pos.y + green_pos.y) // 3)
        self.centroid_pos = vec(centroid_x, centroid_y)
        cx, cy = self.centroid_pos.x, self.centroid_pos.y
        x, y = pos.x, pos.y
        dist = round(math.sqrt((cx - x)**2 + (cy - y)**2), 2)
        return dist

    def get_direction(self):
        # 고스트 하우스에서 나오기
        if self.grid_pos in self.Game.ghost_house:
            return UP

        x, y = self.grid_pos.x, self.grid_pos.y
        up, down, left, right = vec(x, y - 1), vec(x, y + 1), vec(x - 1, y), vec(x + 1, y)
        next_dir_list= [up, down, right, left]
        able_to_go = [False, False, False, False]
        index_true = []

        for i, next in enumerate(next_dir_list):
            if next not in self.Game.walls:
                able_to_go[i] = True
                index_true.append(i)
            else:
                able_to_go[i] = False
                if i in index_true:
                    index_true.remove(i)
        index_true.sort()

        if len(index_true) <= 1 and index_true[0]:
            return vec(next_dir_list[index_true[0]] - vec(x, y))

        min_dist = float('inf')
        for i, able in enumerate(able_to_go):
            if able:
                dist = self.calculate_distance(next_dir_list[i])
                if dist < min_dist:
                    min_dist = dist
                    self.next_dir = i

        # 위
        if self.next_dir == 0:
            self.next_dir = UP
        # 아래
        elif self.next_dir == 1:
            self.next_dir = DOWN
        # 오른쪽
        elif self.next_dir == 2:
            self.next_dir = RIGHT
        # 왼쪽
        elif self.next_dir == 3:
            self.next_dir = LEFT

        return self.next_dir

    def move(self):
        # 5초 뒤 행동 시작
        if self.Game.fps_after_start > 300:
            self.direction = self.get_direction()

###################### TESTING ######################

    def show_direction(self):
        if self.centroid_pos:
            pos_x = self.centroid_pos[0]
            pos_y = self.centroid_pos[1]
            pygame.draw.rect(self.Game.screen, PINK, (pos_x * CELL + SPACE, pos_y * CELL + SPACE, CELL, CELL))

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

        # 빨강 유령 동작 확인
        #self.show_direction()

        self.Game.screen.blit(self.get_image(), cur_pos)
