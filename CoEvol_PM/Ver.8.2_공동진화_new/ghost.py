import pygame
from pygame.math import Vector2 as vec
from settings import *
from main_test import *
import math

vec = pygame.math.Vector2

class Ghost:
        target = None
        able_to_move = True
        direction = vec(0, 0)

#####################################################################
        def update(self):
                self.target = self.find_target()
                if self.target != self.grid_pos:
                        if self.able_to_move:
                                self.pix_pos += self.direction * self.speed
                        if self.time_to_adjust():
                                self.step()
                        if self.time_to_move():
                                self.move()
                                self.able_to_move = self.wall_sensor()
                self.grid_pos_update()


        def reset(self):
                self.grid_pos = vec(self.pos)
                self.pix_pos = self.get_pix_pos()
                self.direction = vec(0, 0)
                self.able_to_move = True
                if self.color == "Blue":
                    self.wait_pos = None

#####################################################################################
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
            for aisle in self.Game.aisle:
                if pos == aisle:
                    return True
            return False

        def get_pix_pos(self):
                return vec((self.grid_pos.x * CELL + SPACE + CELL // 2), (self.grid_pos.y * CELL + SPACE + CELL // 2))

        def grid_pos_update(self):
                self.grid_pos[0] = (self.pix_pos[0] - (SPACE * 2) + (CELL // 2)) // CELL
                self.grid_pos[1] = (self.pix_pos[1] - (SPACE * 2) + (CELL // 2)) // CELL

        def time_to_move(self):
                if int(self.pix_pos.x + (SPACE * 2)) % (CELL) == 0:
                        if self.direction == RIGHT or self.direction == LEFT or self.direction == vec(0, 0):
                                return True
                if int(self.pix_pos.y + (SPACE * 2)) % (CELL) == 0:
                        if self.direction == DOWN or self.direction == UP or self.direction == vec(0, 0):
                                return True
                return False

        def get_speed(self):
                if self.color == "Red":
                    return RED_GHOST_SPEED
                elif self.color == "Blue":
                    return BLUE_GHOST_SPEED
                elif self.color == "Green":
                    return GREEN_GHOST_SPEED
                elif self.color == "Pink":
                    return PINK_GHOST_SPEED

        def time_to_adjust(self):
                SPEED = self.get_speed()
                if self.direction == RIGHT:
                    if int(self.pix_pos.x + (SPACE * 2)) % (CELL) > CELL - SPEED:
                        return True
                if self.direction == LEFT:
                    if int(self.pix_pos.x + (SPACE * 2)) % (CELL) < SPEED and int(self.pix_pos.x + (SPACE * 2)) % (CELL) > 0:
                        return True
                if self.direction == DOWN:
                    if int(self.pix_pos.y + (SPACE * 2)) % (CELL) > CELL - SPEED:
                        return True
                if self.direction == UP:
                    if int(self.pix_pos.y + (SPACE * 2)) % (CELL) < SPEED and int(self.pix_pos.y + (SPACE * 2)) % (CELL) > 0 :
                        return True

        def step(self):
                SPEED = self.get_speed()
                if self.direction == RIGHT or self.direction == LEFT:
                    for i in range(1,SPEED):
                        if int(self.pix_pos.x + self.direction.x*i + (SPACE * 2)) % (CELL) == 0 :
                            gap = i
                    self.pix_pos += self.direction*gap
                    #print("--- RIGHT/LEFT steping ---")

                elif self.direction == DOWN or self.direction == UP:
                    for i in range(1,SPEED):
                        if int(self.pix_pos.y + self.direction.y*i + (SPACE * 2)) % (CELL) == 0 :
                            gap = i
                    self.pix_pos += self.direction*gap
                    #print("--- UP/DOWN steping ---")


        def find_target(self):
                return self.Game.player.grid_pos

########################## BASIC MOVING ###############################

        def get_path_direction(self, target):
                next_cell = self.search_next_position(target)
                x = next_cell[0] - self.grid_pos[0]
                y = next_cell[1] - self.grid_pos[1]
                return vec(x, y)

        def search_next_position(self, target):
                curr_pos = [int(self.grid_pos.x), int(self.grid_pos.y)]
                target_pos = [int(target[0]), int(target[1])]
                position = self.BFS(curr_pos, target_pos)
                return position[1]

        def BFS(self, start, target):

                grid = [[0 for x in range(28)] for x in range(31)]
                for cell in self.Game.walls:
                        if cell.x < 28 and cell.y < 31:
                                grid[int(cell.y)][int(cell.x)] = 1
                queue = [start]
                path = []
                visited = []
                while queue:
                        current = queue[0]
                        queue.remove(queue[0])
                        visited.append(current)
                        if current == target:
                                break
                        else:
                                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                                for neighbour in neighbours:
                                        if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                                                if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                                                        next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                                                        if next_cell not in visited:
                                                                if grid[next_cell[1]][next_cell[0]] != 1:
                                                                        queue.append(next_cell)
                                                                        path.append({"Current": current, "Next": next_cell})
                shortest = [target]

                while target != start:
                    for step in path:
                            if step["Next"] == target:
                                    target = step["Current"]
                                    shortest.insert(0, step["Current"])

                return shortest
