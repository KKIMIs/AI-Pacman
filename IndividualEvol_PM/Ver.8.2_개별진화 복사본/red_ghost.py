import pygame
import math
from pygame.math import Vector2 as vec
from settings import *
from main_test import *
from ghost import *

# Ghost 클래스 상속
class RedGhost(Ghost):
        def __init__(self, Game, pos, speed):
                self.Game = Game
                self.grid_pos = pos
                self.pos = [pos.x, pos.y]
                self.pix_pos = self.get_pix_pos()
                self.speed = speed
                self.next_dir = UP
                self.color = "Red"

        ####################### MOVING #######################

        def calculate_distance(self, pos):
            self.target = self.find_target()
            distance =  math.sqrt(math.pow((pos[0]-self.target[0]), 2) + math.pow((pos[1]-self.target[1]), 2))

            return round(distance, 1)

        def is_wall(self, pos):
            if pos in self.Game.walls:
                return True
            return False

        # 가는 방향에서 정반대 방향인 180도 방향인지 판단
        def is_opposide(self, former_dir, next_grid_pos):
            x = self.grid_pos.x
            y = self.grid_pos.y
            up, down, left, right = vec(x, y-1), vec(x, y+1), vec(x-1, y), vec(x+1, y)

            if former_dir == UP:
                opposide = down
            elif former_dir == DOWN:
                opposide = up
            elif former_dir == LEFT:
                opposide = right
            elif former_dir == RIGHT:
                opposide = left

            if opposide == next_grid_pos:
                return True
            return False

        def in_house(self):
            house_pos = [vec(13, 13), vec(13, 12), vec(13, 11)]

            if self.grid_pos in house_pos:
                return True
            return False

        # 팩맨과 빨강 유령의 상/하/좌/우 좌표로 직선 거리를 계산했을 때 가장 짧은 거리를 가지는 좌표 구하기
        def get_min_grid_pos(self):
        	x = self.grid_pos.x
        	y = self.grid_pos.y

        	# 빨강 유령 상/하/좌/우 grid 좌표
        	up, down, left, right = vec(x, y-1), vec(x, y+1), vec(x-1, y), vec(x+1, y)
        	directions = [up, down, right, left]

        	min_dis = float('inf')
        	min_grid_pos = self.grid_pos
        	former_dir = self.next_dir

        	for next_grid_pos in directions:
        		# 벽이나 현재 방향에서 반대 방향이 아닌 좌표로부터의 거리만 체크
        		if (self.is_wall(next_grid_pos) == False) and (self.is_opposide(former_dir, next_grid_pos) == False):
        			distance = self.calculate_distance(next_grid_pos)
        			if min_dis > distance:
        				min_dis = distance
        				min_grid_pos = next_grid_pos
        			# 거리가 같은 경우 '위 > 왼쪽 > 아래 > 오른쪽' 순 우선순위를 고려하여 결정
        			elif distance == min_dis:
        				if (next_grid_pos == up) or (min_grid_pos == up):
        					min_grid_pos = up
        				elif (next_grid_pos == left) or (min_grid_pos == left):
        					min_grid_pos = left
        				elif (next_grid_pos == down) or (min_grid_pos == down):
        					min_grid_pos = down
        				else:
        					min_grid_pos = down

        	return min_grid_pos

        # 다음에 나아갈 방향 구하기
        def get_direction(self):
        	x = self.grid_pos.x
        	y = self.grid_pos.y
        	up, down, left, right = vec(x, y-1), vec(x, y+1), vec(x-1, y), vec(x+1, y)

        	min_grid_pos = self.get_min_grid_pos()
        	former_dir = self.next_dir

        	# ghost house에 있을 경우 나오게 하기
        	if self.in_house() == True:
        		self.next_dir = UP
        		return self.next_dir

        	if min_grid_pos == up:
        		self.next_dir = UP
        	elif min_grid_pos == down:
        		self.next_dir = DOWN
        	elif min_grid_pos == right:
        		self.next_dir = RIGHT
        	elif min_grid_pos == left:
        		self.next_dir = LEFT

        	# 빨강 유령 동작 확인
        	#self.print_direction(min_grid_pos, former_dir)

        	return self.next_dir

        def move(self):
            self.direction = self.get_direction()

        ###################### TESTING ######################

        def print_direction(self, next_grid_pos, former_dir):
            x = self.grid_pos.x
            y = self.grid_pos.y

            directions = {'상': vec(x, y-1), '하': vec(x, y+1), '좌': vec(x-1, y), '우': vec(x+1, y)}

            if self.next_dir == UP:
                movement = 'UP'
            elif self.next_dir == DOWN:
                movement = 'DOWN'
            elif self.next_dir == RIGHT:
                movement = 'RIGHT'
            elif self.next_dir == LEFT:
                movement = 'LEFT'

            print('현재 좌표: {}'.format(self.grid_pos))

            for direction, pos in directions.items():
                print('{}: {} / 벽={} / 반대쪽={} / 거리={}'.format(direction, pos, self.is_wall(pos), self.is_opposide(former_dir, pos), self.calculate_distance(pos)))

            print('결과: 최소 거리={} / 다음 방향={} / 다음 좌표={}'.format(self.calculate_distance(next_grid_pos), movement, next_grid_pos), end='\n\n')

        def draw_direction(self):
        	x = self.grid_pos.x
        	y = self.grid_pos.y
        	target = self.find_target()

        	up, down, left, right = vec(x, y-1), vec(x, y+1), vec(x-1, y), vec(x+1, y)
        	directions = [up, down, right, left]
        	former_dir = self.next_dir

        	for pos in directions:
        		# 벽이나 반대쪽 좌표면 갈색 네모
        		if self.is_wall(pos) == True or self.is_opposide(former_dir, pos) == True:
        			pygame.draw.rect(self.Game.screen, BROWN, (pos.x * CELL + SPACE, pos.y * CELL + SPACE, CELL, CELL))
        		# 가장 짧은 거리로 향하는 좌표면 하얀 네모
        		elif pos == self.get_min_grid_pos():
        			pygame.draw.rect(self.Game.screen, WHITE, (pos.x * CELL + SPACE, pos.y * CELL + SPACE, CELL, CELL))
        			pygame.draw.line(self.Game.screen, WHITE, (target.x * CELL + SPACE, target.y * CELL + SPACE), (pos.x * CELL + SPACE, pos.y * CELL + SPACE), 2)
        		# 벽이나 반대방향은 아니지만 가장 짧은 거리로 향하는 좌표가 아니면 회색 네모
        		else:
        			pygame.draw.rect(self.Game.screen, GREEN, (pos.x * CELL + SPACE, pos.y * CELL + SPACE, CELL, CELL))
        			pygame.draw.line(self.Game.screen, GREEN, (target.x * CELL + SPACE, target.y * CELL + SPACE), (pos.x * CELL + SPACE, pos.y * CELL + SPACE), 2)

        ####################### DRAWING #######################

        def get_image(self):
            image = red_up
            if self.direction == vec(0, 0):
                image = red_right
            elif self.direction == UP:
                image = red_up
            elif self.direction == DOWN:
                image = red_down
            elif self.direction == RIGHT:
                image = red_right
            elif self.direction == LEFT:
                image = red_left

            return image

        def stop(self):
            cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)
            self.speed = 0

            self.Game.screen.blit(self.get_image(), cur_pos)

        def draw(self):
            cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)

            # stop 후 다시 움직이기 시작할 때
            if self.speed == 0:
                self.speed = RED_GHOST_SPEED

            # 빨강 유령 동작 확인
            # self.draw_direction()

            self.Game.screen.blit(self.get_image(), cur_pos)