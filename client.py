import pygame, pickle, socket
from settings import *
from game import Player, Room, PlayerInfo, Fruit

class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.name = name
        self.addr = (self.host, self.port)
        self.player_info = None
        self.conn()

    def get_player_info(self):
        return self.player_info

    def conn(self):
        try:
            self.client.connect(self.addr)
            self.client.send(pickle.dumps(self.name))
            self.player_info = pickle.loads(self.client.recv(1024))
            print(self.player_info)
            print('连接成功！')
        except socket.error as e:
            print('连接出错:', str(e))

    def send(self, data):
        try:
            pkl_data = pickle.dumps(data)
            self.client.send(pkl_data)
            msg = pickle.loads(self.client.recv(1024))
            return msg
        except socket.error as e:
            print('网络出错：', str(e))


class App:
    def __init__(self):
        pygame.init()
        self.name = input('请输入用户名 > ')
        self.window = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(self.name)
        self.player2 = Player('enemy')
        self.client = Network(self.name)
        self.player_info = self.client.get_player_info()
        self.fruits = []
        self.player.update_by_info(self.player_info)
        self.my_room = None
        self.running = True
        self.USEREVENT = pygame.event.Event(pygame.USEREVENT)
        pygame.time.set_timer(self.USEREVENT, 100)

    def update(self):
        self.player.input()
        self.my_room = self.client.send(self.player.body)
        self.fruits = []
        for fruit_info in self.my_room.fruits:
            fruit = Fruit(fruit_info.pos, fruit_info.type)
            self.fruits.append(fruit)
        for info in self.my_room.players:
            if info.pos != self.player_info.pos:
                self.player2.update_by_info(info)
                break
    def draw_screen(self):
        self.window.fill(bg_color)
        for row in range(TILE_NUMBER):
            for col in range(TILE_NUMBER):
                if (row % 2 and col % 2) or (row % 2 == 0 and col % 2 == 0):
                    rect = col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE
                    pygame.draw.rect(self.window, grass_color, rect)

    def draw_players(self):
        self.player.draw(self.window)
        if self.player2.online:
            self.player2.draw(self.window)
        for fruit in self.fruits:
            fruit.draw(self.window)
    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.USEREVENT:
                    self.player.update()
            self.update()
            self.draw_screen()
            self.draw_players()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    app = App()
    app.run()
