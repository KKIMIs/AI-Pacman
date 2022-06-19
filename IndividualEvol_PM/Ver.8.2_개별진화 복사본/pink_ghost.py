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
        self.direction = vec(0,0)
        self.former_dir = vec(0,0)
        self.centroid = None
        self.color = "Pink"

####################### MOVING #######################

    # 현위치와 무게중심 거리 차이 계산
    def calculate_centroid(self):
        red_pos = self.Game.red_ghost.grid_pos
        blue_pos = self.Game.blue_ghost.grid_pos
        green_pos = self.Game.green_ghost.grid_pos
        centroid_x = int((red_pos.x + blue_pos.x + green_pos.x) // 3)
        centroid_x = int(centroid_x * CELL + SPACE)
        centroid_y = int((red_pos.y + blue_pos.y + green_pos.y) // 3)
        centroid_y = int(centroid_y * CELL + SPACE)
        self.centroid = vec(centroid_x, centroid_y)

        if self.centroid in self.Game.ghost_house:
            self.calculate_centroid()

    def calculate_distance(self, pos1, pos2):
        distance = math.sqrt(math.pow((pos1.x - pos2.x), 2) + math.pow((pos1.y - pos2.y), 2))
        return distance

    # 반대방향 전달
    def is_opposide(self, former_dir):
        if former_dir == UP:
            opposide = DOWN
        elif former_dir == DOWN:
            opposide = UP
        elif former_dir == LEFT:
            opposide = RIGHT
        elif former_dir == RIGHT:
            opposide = LEFT
        return opposide

    def is_unable_togo(self):
        able_dir = [UP, DOWN, LEFT, RIGHT]
        x, y = self.grid_pos.x, self.grid_pos.y
        up, down, left, right = vec(x, y - 1), vec(x, y + 1), vec(x - 1, y), vec(x + 1, y)
        if up in self.Game.walls or up in self.Game.ghost_house:
            able_dir.remove(UP)
        if down in self.Game.walls or down in self.Game.ghost_house:
            able_dir.remove(DOWN)
        if left in self.Game.walls or left in self.Game.ghost_house:
            able_dir.remove(LEFT)
        if right in self.Game.walls or right in self.Game.ghost_house:
            able_dir.remove(RIGHT)

        return able_dir

    def get_direction(self):
        # 고스트 하우스에서 나오기
        if self.grid_pos in self.Game.ghost_house:
            return UP

        # 이동 가능한 방향이 1개 일때
        able_dir_list = self.is_unable_togo()
        if len(able_dir_list) == 1:
            return able_dir_list[0]

        # 이동방향 유지(180회전 금지)
        opposite_dir = self.is_opposide(self.former_dir)
        if opposite_dir in able_dir_list:
            able_dir_list.remove(opposite_dir)

        # 최단거리 이동방향 계산
        self.calculate_centroid()
        min_dist = float('inf')
        min_dir = None
        for dir in able_dir_list:
            next_dir = self.grid_pos + dir
            dist = self.calculate_distance(next_dir, self.centroid)
            if dist < min_dist:
                min_dist = dist
                min_dir = dir
        return min_dir

    def move(self):
        # 5초 뒤 행동 시작
        if self.Game.fps_after_start > 300:
            self.direction = self.get_direction()
            self.former_dir = self.direction


###################### TESTING ######################

    def show_distance(self):
        red_pos = self.Game.red_ghost.grid_pos
        blue_pos = self.Game.blue_ghost.grid_pos
        green_pos = self.Game.green_ghost.grid_pos

        pygame.draw.line(self.Game.screen, DARK_GREY, (red_pos.x * CELL + SPACE, red_pos.y * CELL + SPACE), (blue_pos.x * CELL + SPACE, blue_pos.y * CELL + SPACE), 2)
        pygame.draw.line(self.Game.screen, DARK_GREY, (blue_pos.x * CELL + SPACE, blue_pos.y * CELL + SPACE), (green_pos.x * CELL + SPACE, green_pos.y * CELL + SPACE), 2)
        pygame.draw.line(self.Game.screen, DARK_GREY, (green_pos.x * CELL + SPACE, green_pos.y * CELL + SPACE), (red_pos.x * CELL + SPACE, red_pos.y * CELL + SPACE), 2)

        mid_1_x, mid_1_y = (red_pos.x + green_pos.x) / 2, (red_pos.y + green_pos.y) / 2
        mid_2_x, mid_2_y = (green_pos.x + blue_pos.x) / 2, (green_pos.y + blue_pos.y) / 2
        mid_3_x, mid_3_y = (blue_pos.x + red_pos.x) / 2, (blue_pos.y + red_pos.y) / 2

        pygame.draw.line(self.Game.screen, DARK_GREY, (mid_1_x * CELL + SPACE, mid_1_y * CELL + SPACE), (blue_pos.x * CELL + SPACE, blue_pos.y * CELL + SPACE), 2)
        pygame.draw.line(self.Game.screen, DARK_GREY, (mid_2_x * CELL + SPACE, mid_2_y * CELL + SPACE), (red_pos.x * CELL + SPACE, red_pos.y * CELL + SPACE), 2)
        pygame.draw.line(self.Game.screen, DARK_GREY, (mid_3_x * CELL + SPACE, mid_3_y * CELL + SPACE), (green_pos.x * CELL + SPACE, green_pos.y * CELL + SPACE), 2)

    def show_direction(self):
        if self.centroid:
            pos_x = self.centroid[0]
            pos_y = self.centroid[1]
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

        # 분홍 유령 동작 확인
        # self.show_distance()
        # self.show_direction()

        self.Game.screen.blit(self.get_image(), cur_pos)
