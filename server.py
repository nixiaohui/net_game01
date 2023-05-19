import socket, pickle
from threading import Thread

import pygame

from game import Room, PlayerInfo, Timer, FruitInfo


class Server:
    def __init__(self):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.bind(('127.0.0.1', 5555))
        self.skt.listen(5)
        self.index = 0
        self.rooms = []
        pygame.init()

    def handle_conn(self, conn:socket.socket, idx: int):
        name = pickle.loads(conn.recv(1024))
        print(name, '上线')
        my_room = None
        for room in self.rooms:
            if not room.ready:
                my_room = room
        if my_room:
            # 加入房间，成为普通玩家
            player = PlayerInfo(name, pos='B', color='red')
            my_room.add_player(player)
            print('加入房间')
        else:
            # 建房，成为房主
            player = PlayerInfo(name)
            my_room = Room(player)
            self.rooms.append(my_room)
            print('房间创建成功')
        conn.send(pickle.dumps(player))
        while True:
            if my_room.ready:
                my_room.update()
                print(my_room.fruits)
            try:
                body = pickle.loads(conn.recv(1024))
                if body:
                    player.body = body
                else:
                    my_room.remove_player(player)
                    if my_room.empty() and my_room in self.rooms:
                        self.rooms.remove(my_room)
                    print(name, '断开了连接')
                conn.send(pickle.dumps(my_room))
            except socket.error as e:
                my_room.remove_player(player)
                if my_room.empty() and my_room in self.rooms:
                    self.rooms.remove(my_room)
                print('连接出错：', str(e))

    def run(self):
        while True:
            conn, addr = self.skt.accept()
            Thread(target=self.handle_conn, args=(conn, self.index)).start()
            self.index += 1

if __name__ == '__main__':
    server = Server()
    server.run()
