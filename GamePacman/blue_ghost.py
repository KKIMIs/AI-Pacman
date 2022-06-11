import pygame
import math
import random
from pygame.math import Vector2 as vec
from settings import *
from main_test import *
from ghost import *

# Ghost 클래스 상속
class BlueGhost(Ghost):
        def __init__(self, Game, pos, speed):
                self.Game = Game
                self.grid_pos = pos
                self.pos = [pos.x, pos.y]
                self.pix_pos = self.get_pix_pos()
                self.speed = speed
                self.wait_area = []
                self.wait_pos = None
                self.wait_pos_arrived =  False
                self.color = "Blue"

        def move(self):
                #플레이어 센서 시 플레이어 추척
                if self.sense_player():
                    self.direction = self.get_path_direction(self.target)

                else:
                    old_wait_area = self.wait_area
                    self.search_coin_areas()

                    #if self.wait_pos == None:
                        #self.get_wait_pos()

                    #새로운 목적지가 설정될때마다 arrived 리셋:
                    if old_wait_area != self.wait_area:
                        self.get_wait_pos()

                    #목적지에 도착 - > 새 목적지 탐색
                    if self.grid_pos == self.wait_pos:
                        self.get_wait_pos()

                    else:
                        self.direction = self.get_path_direction(self.wait_pos)

        def sense_player(self):
            direcs = [ RIGHT, LEFT, UP, DOWN ]
            sensing_area = []
            #4-방향으로 6칸 센서
            for h  in range(4):
                for i in range(6):
                    next_search_pos = vec(self.grid_pos + direcs[h]*(i+1))
                    if self.find_wall(next_search_pos):
                        break
                    else:
                        sensing_area.append(next_search_pos)

            if self.Game.player.grid_pos in sensing_area:
                return True
            else:
                return False

        def search_coin_areas(self):
            #맵을 6분활
            #topleft, bottemright
            area_1 = ([0,0],[13,9])
            area_2 = ([14,0],[27,9])
            area_3 = ([0,10],[13,20])
            area_4 = ([14,10],[27,20])
            area_5 = ([0,21],[13,30])
            area_6 = ([14,21],[27,30])
            areas_list = [area_1,area_2,area_3,area_4,area_5,area_6]
            coins_list =[]

            for i in range(6):
                coins = self.count_coins(areas_list[i])
                coins_list.append(coins)
            #코인 최다 지역 탐색
            max = coins_list[0]
            self.wait_area = areas_list[0]
            num = 0
            for i in range(6):
                if max < coins_list[i]:
                    max = coins_list[i]
                    self.wait_area = areas_list[i]
                    num = i
            #print("제",str(num+1)+"영역")

        def get_wait_pos(self):
            #코인이 제일 많은 지역 내 랜덤 목표 위치 생성
            house_pos = [vec(12, 13), vec(13, 11), vec(13, 12), vec(13, 13), vec(14, 11), vec(14, 12), vec(14, 13), vec(15, 13)]
            way_out_pos = [vec(0,13),vec(1,13),vec(2,13),vec(25,13),vec(26,13),vec(27,13)]
            x_1 = self.wait_area[0][0]
            x_2 = self.wait_area[1][0]
            y_1 = self.wait_area[0][1]
            y_2 = self.wait_area[1][1]

            while True:
                x_num = random.randint(x_1,x_2)
                y_num = random.randint(y_1,y_2)
                self.wait_pos = vec(x_num, y_num)
                if (self.wait_pos not in self.Game.walls
                and self.wait_pos not in house_pos and self.wait_pos not in way_out_pos):
                    #print("랜덤위치 x: ",x_num,"y:",y_num)
                    break


        def count_coins(self,area):
            coins = 0
            for xidx in range(area[0][0],area[1][0]+1):
                for yidx in range(area[0][1],area[1][1]+1):
                    if vec(xidx,yidx) in self.Game.coins:
                        coins += 1
            return coins

        def draw_wait_pos(self):
            if self.wait_pos:
                pos_x = self.wait_pos[0]
                pos_y = self.wait_pos[1]
                pygame.draw.rect(self.Game.screen, BLUE, (pos_x* CELL + SPACE, pos_y * CELL + SPACE, CELL, CELL))

#####################################################################################
        def get_image(self):
            image = blue_up
            if self.direction == vec(0, 0):
                image = blue_right
            elif self.direction == UP:
                image = blue_up
            elif self.direction == DOWN:
                image = blue_down
            elif self.direction == RIGHT:
                image = blue_right
            elif self.direction == LEFT:
                image = blue_left

            return image

        def stop(self):
            cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)
            self.speed = 0

            self.Game.screen.blit(self.get_image(), cur_pos)

        def draw(self):
            cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)

            # stop 후 다시 움직이기 시작할 때
            if self.speed == 0:
                self.speed = BLUE_GHOST_SPEED

            #목적지 확인
            #self.draw_wait_pos()

            self.Game.screen.blit(self.get_image(), cur_pos)
