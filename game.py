import random

import pygame
from settings import *


class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.start_timer = 0
        self.active = False

    def activate(self):
        self.start_timer = pygame.time.get_ticks()
        self.active = True

    def deactivate(self):
        self.start_timer = 0
        self.active = False

    def update(self):
        current = pygame.time.get_ticks()
        if current - self.start_timer >= self.duration:
            if self.func:
                self.func()
            self.deactivate()


class FruitInfo:
    def __init__(self, pos, tp):
        self.type = tp
        self.pos = pos
        self.enable = True
        self.timer = Timer(3000, self.disable)
        self.timer.activate()

    def disable(self):
        self.enable = False

    def update(self):
        self.timer.update()


class Fruit:
    def __init__(self, pos, tp):
        self.type = tp
        self.image = pygame.image.load(f'./images/fruit/{fruit_types[tp]}.png')
        self.x, self.y = pos
        self.rect = self.image.get_rect(topleft=(self.x*TILE_SIZE, self.y*TILE_SIZE))
        self.enable = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update_by_info(self, fruit_info: FruitInfo):
        self.enable = fruit_info.enable
        self.type = fruit_info.type
        self.x, self.y = fruit_info.pos

class PlayerInfo:
    def __init__(self, name, pos='A', color='blue'):
        self.name = name
        self.pos = pos
        self.body = []
        self.color = color
        self.score = 0
        self.online = True
        self.init_body()

    def init_body(self):
        if self.pos == 'A':
            self.body = position_A
        else:
            self.body = position_B


class Player:
    def __init__(self, name, color='blue'):
        self.body = position_A
        self.name = name
        self.pos = 'A'
        if color not in ['blue', 'red']:
            color = 'blue'
        self.image_path = f'./images/snake/{color}'
        self.load_images()
        self.online = True

        # movement
        self.direction = pygame.Vector2(0, 0)
        self.speed = 3

    def update_by_info(self, player_info: PlayerInfo):
        self.name = player_info.name
        self.body = player_info.body
        self.pos = player_info.pos
        self.color = player_info.color
        if self.color not in ['blue', 'red']:
            color = 'blue'
        self.image_path = f'./images/snake/{self.color}'
        self.load_images()
        self.online = player_info.online

    def load_images(self):
        self.head_down = pygame.image.load(f'{self.image_path}/head_down.png')
        self.head_up = pygame.image.load(f'{self.image_path}/head_up.png')
        self.head_left = pygame.image.load(f'{self.image_path}/head_left.png')
        self.head_right = pygame.image.load(f'{self.image_path}/head_right.png')

        self.body_v = pygame.image.load(f'{self.image_path}/body_vertical.png')
        self.body_h = pygame.image.load(f'{self.image_path}/body_horizontal.png')
        self.body_bl = pygame.image.load(f'{self.image_path}/body_bl.png')
        self.body_br = pygame.image.load(f'{self.image_path}/body_br.png')
        self.body_tl = pygame.image.load(f'{self.image_path}/body_tl.png')
        self.body_tr = pygame.image.load(f'{self.image_path}/body_tr.png')

        self.tail_down = pygame.image.load(f'{self.image_path}/tail_down.png')
        self.tail_up = pygame.image.load(f'{self.image_path}/tail_up.png')
        self.tail_left = pygame.image.load(f'{self.image_path}/tail_left.png')
        self.tail_right = pygame.image.load(f'{self.image_path}/tail_right.png')

    def update_head_graphic(self):
        dx = self.body[1][0] - self.body[0][0] # 0 同列, 1 头在左, -1 头在右
        dy = self.body[1][1] - self.body[0][1] # 0 同行, 1 头在上, -1 头在下
        if dx == 1:
            self.head = self.head_left
        elif dx == -1:
            self.head = self.head_right
        elif dy == 1:
            self.head = self.head_up
        else:
            self.head = self.head_down

    def update_tail_graphic(self):
        dx = self.body[-2][0] - self.body[-1][0]  # 0 同列, 1 尾在左, -1 尾在右
        dy = self.body[-2][1] - self.body[-1][1]  # 0 同行, 1 尾在上, -1 尾在下
        if dx == 1:
            self.tail = self.tail_left
        elif dx == -1:
            self.tail = self.tail_right
        elif dy == 1:
            self.tail = self.tail_up
        else:
            self.tail = self.tail_down

    def draw(self, display_surface):
        if not self.online:
            return
        self.update_head_graphic()
        self.update_tail_graphic()
        for i in range(len(self.body)):
            if i == 0:
                display_surface.blit(self.head, (self.body[0][0] * TILE_SIZE, self.body[0][1] * TILE_SIZE))
            elif i+1 == len(self.body):
                display_surface.blit(self.tail, (self.body[-1][0] * TILE_SIZE, self.body[-1][1] * TILE_SIZE))
            else:
                prex = self.body[i-1][0] - self.body[i][0]  # 0 同列, 1 前在右, -1 前在左
                prey = self.body[i-1][1] - self.body[i][1]  # 0 同行, 1 前在下, -1 前在上
                nxtx = self.body[i+1][0] - self.body[i][0]  # 0 同列, 1 后在右, -1 后在左
                nxty = self.body[i+1][1] - self.body[i][1]  # 0 同行, 1 后在下, -1 后在上
                if prex == 0 and nxtx == 0:
                    self.body_image = self.body_v
                elif prey == 0 and nxty == 0:
                    self.body_image = self.body_h
                elif prex == 1 and nxty == 1 or prey == 1 and nxtx == 1:
                    self.body_image = self.body_br
                elif prex == 1 and nxty == -1 or prey == -1 and nxtx == 1:
                    self.body_image = self.body_tr
                elif prex == -1 and nxty == 1 or prey == 1 and nxtx == -1:
                    self.body_image = self.body_bl
                else:
                    self.body_image = self.body_tl
                display_surface.blit(self.body_image, (self.body[i][0] * TILE_SIZE, self.body[i][1] * TILE_SIZE))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.direction.y != 1:
                self.direction = pygame.Vector2(0, -1)
        elif keys[pygame.K_DOWN]:
            if self.direction.y != -1:
                self.direction = pygame.Vector2(0, 1)
        elif keys[pygame.K_LEFT]:
            if self.direction.x != 1:
                self.direction = pygame.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            if self.direction.x != -1:
                self.direction = pygame.Vector2(1, 0)

    def move(self):
        head = tuple(self.body[0] + self.direction)
        self.body.pop()
        self.body.insert(0, head)

    def update(self):
          self.input()
          if self.direction != (0, 0):
              self.move()


class Room:
    def __init__(self, player: PlayerInfo):
        self.players = []
        self.amount = 0
        self.capacity = 2
        self.ready = False
        self.add_player(player)
        self.fruits = []
        self.timer = Timer(2000, self.gen_fruit)

    def gen_fruit(self):
        x = random.randint(0, TILE_NUMBER-1)
        y = random.randint(0, TILE_NUMBER-1)
        tp = random.randint(0, 2)
        fruit_info = FruitInfo((x, y), tp)
        self.fruits.append(fruit_info)

    def empty(self):
        return self.amount > 0

    def add_player(self, player: PlayerInfo):
        if self.amount >= self.capacity:
            return False
        self.players.append(player)
        self.amount += 1
        if self.amount == 2:
            self.ready = True
        return True

    def remove_player(self, player):
        if player in self.players:
            # self.players.remove(player)
            player.online = False
            self.amount -= 1
            self.ready = False
            return True
        return False

    def update(self):
        if not self.timer.active:
            self.timer.activate()
        self.timer.update()
        exp_fruits = []
        for fruit in self.fruits:
            fruit.update()
            if not fruit.enable:
                exp_fruits.append(fruit)
        for fruit in exp_fruits:
            self.fruits.remove(fruit)