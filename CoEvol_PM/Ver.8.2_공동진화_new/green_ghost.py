import pygame
import math
from pygame.math import Vector2 as vec
from settings import *
from main_test import *
from ghost import *

bottomLeft = vec(0,30)
topRight = vec(28,0)
one_move = 10

class Node():
        def __init__(self, pos_x, pos_y, parent=None, start=0, target= 0):
            self.pos = [pos_x, pos_y]
            self.parent = parent
            self.g = 0      #이동했던 거리
            self.h = 0      #목표까지 거리
            self.f = self.g + self.h

class GreenGhost(Ghost):
        def __init__(self, Game, pos, speed):
                self.Game = Game
                self.grid_pos = pos
                self.pos = [pos.x, pos.y]
                self.pix_pos = self.get_pix_pos()
                self.speed = speed
                self.pre_path = None
                self.open_list =[]
                self.closed_list =[]
                self.final_list =[]
                self.color = "Green"

        def move(self):
                # 게임 시작 후 5 초 뒤 출발
                #if self.Game.fps_after_start > 150:
                self.direction = self.Astar_get_path_direction(self.target)

        def Astar_get_path_direction(self, target):
                next_cell = self.Astar_find_next_cell(target)
                xdir = next_cell[0] - self.grid_pos[0]
                ydir = next_cell[1] - self.grid_pos[1]
                return vec(xdir, ydir)

        def Astar_find_next_cell(self, target):
                path = self.Astar_pathfinding([self.grid_pos.x, self.grid_pos.y], [target[0], target[1]])
                return vec(path[1].pos)

        def Astar_pathfinding(self, start, target):
                global cur_grid, target_grid
                self.open_list =[]
                self.closed_list =[]
                self.final_list =[]
                start_grid = Node(start[0],start[1])
                target_grid = Node(target[0],target[1])
                self.open_list.append(start_grid)

                while len(self.open_list)>0:
                    cur_grid = self.open_list[0]
                    #열린리스트 중 가장 F가 작고 F가 같다면
                    #H가 작은 걸 현재노드로 하고 열린리스트에서 닫힌리스트로 옮기기
                    for i in range(0,len(self.open_list)):
                        if (self.open_list[i].f < cur_grid.f and self.open_list[i].h < cur_grid.h):
                            cur_grid = self.open_list[i]

                    self.open_list.remove(cur_grid)
                    self.closed_list.append(cur_grid)

                    #target에 도착
                    if cur_grid.pos == target_grid.pos:
                        path_grid = cur_grid
                        while path_grid != start_grid:
                            self.final_list.append(path_grid)
                            path_grid = path_grid.parent

                        self.final_list.append(start_grid)
                        self.final_list.reverse()
                        return self.final_list

                    self.open_list_Add(cur_grid.pos[0], cur_grid.pos[1] - 1)       #상
                    self.open_list_Add(cur_grid.pos[0], cur_grid.pos[1] + 1)       #하
                    self.open_list_Add(cur_grid.pos[0] - 1, cur_grid.pos[1])       #좌
                    self.open_list_Add(cur_grid.pos[0] + 1, cur_grid.pos[1])       #우

        def open_list_Add(self, checkX,checkY):
                cur_grid ,target_grid

                #상하좌우 범위를 벗어나지 않고, 벽이 아니면서, 닫힌리스트에 없다면 탐색
                if (checkX < bottomLeft.x or checkX > topRight.x + 1 or checkY > bottomLeft.y or checkY < topRight.y + 1 ):
                    #print("범위 아웃")
                    return
                elif vec(checkX,checkY) in self.Game.walls:
                    #print("벽")
                    return
                for i in range(len(self.closed_list)):
                    if [checkX,checkY] == self.closed_list[i].pos:
                        #print("이미 검사")
                        return

                #코너를 가로질러 가지 않을시, 이동 중에 수직수평 장애물이 있으면 안됨
                if cur_grid in self.Game.walls or vec(checkX,checkY) in self.Game.walls:
                    return

                neighbor_grid = Node(checkX,checkY)
                move_cost = cur_grid.g + one_move

                #이동비용이 이웃노드G보다 작거나 또는 열린리스트에 이웃노드가 없다면
                #G, H, ParentNode를 설정 후 열린리스트에 추가
                if( move_cost < neighbor_grid.g or neighbor_grid not in self.open_list):
                    neighbor_grid.g = move_cost
                    neighbor_grid.h = int(math.sqrt(((target_grid.pos[0]-neighbor_grid.pos[0]) ** 2) + ((target_grid.pos[1]-neighbor_grid.pos[1]) ** 2))*10)
                    neighbor_grid.f = neighbor_grid.g + neighbor_grid.h
                    neighbor_grid.parent = cur_grid
                    self.open_list.append(neighbor_grid)

        def draw_Astar_path(self):
            for i in range(len(self.final_list)-1):
                start_point = self.final_list[i].pos
                end_point = self.final_list[i+1].pos

                start_x = start_point[0] * CELL + SPACE + CELL // 2
                start_y = start_point[1] * CELL + SPACE + CELL // 2
                end_x = end_point[0] * CELL + SPACE + CELL // 2
                end_y = end_point[1] * CELL + SPACE + CELL // 2

                pygame.draw.line(self.Game.screen, GREEN, (start_x, start_y), (end_x, end_y), 3)



#############################################################################

        def get_image(self):
            image = green_up
            if self.direction == vec(0, 0):
                image = green_right
            elif self.direction == UP:
                image = green_up
            elif self.direction == DOWN:
                image = green_down
            elif self.direction == RIGHT:
                image = green_right
            elif self.direction == LEFT:
                image = green_left

            return image

        def stop(self):
            cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)
            self.speed = 0

            self.Game.screen.blit(self.get_image(), cur_pos)

        def draw(self):
            cur_pos = (self.pix_pos.x - 15, self.pix_pos.y - 15)

            # stop 후 다시 움직이기 시작할 때
            if self.speed == 0:
                self.speed = GREEN_GHOST_SPEED

            self.Game.screen.blit(self.get_image(), cur_pos)

            # 경로확인
            # if self.Game.fps_after_start > 150:
            # self.draw_Astar_path()
