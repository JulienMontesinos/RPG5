import sys
import pygame
import pickle
import socket
from player import Player
from random import randint
from screen import Screen
from map import Map

class Game:
    def __init__(self):
        pygame.init()
        self.screen = Screen()
        self.map = Map(self.screen)
        self.player = Player(p_id=None,
                             x=randint(35, 310),
                             y=randint(300, 430),
                             frame_width=32,
                             frame_height=32)
        self.map.add_player(self.player)
        self.port = 5555
        self.host = "10.0.94.50"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.other_players = {}

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.player.id = self.sock.recv(2048).decode("utf-8")

    def send_player_data(self):
        data = {
            "id": self.player.id,
            "position": (self.player.x, self.player.y)
        }
        self.sock.send(pickle.dumps(data))
        response = self.sock.recv(2048)
        return response

    def update_other_players_data(self, data):
        received_data = pickle.loads(data)
        current_active_ids = set(received_data.keys())

    # 移除已断开连接的玩家
        for player_id in list(self.other_players.keys()):
            if player_id not in current_active_ids and player_id != self.player.id:
               self.map.remove_player(self.other_players[player_id])  # 假设Map类有remove_player方法
               del self.other_players[player_id]

    # 更新或添加其他玩家
        for player_id, position in received_data.items():
            if player_id == self.player.id:
                continue  # 跳过自己
            if player_id in self.other_players:
               existing_player = self.other_players[player_id]
               existing_player.x, existing_player.y = position
               existing_player.rect.topleft = position
            else:
               new_player = Player(p_id=player_id, x=position[0], y=position[1], frame_width=32, frame_height=32)
               self.other_players[player_id] = new_player
               self.map.add_player(new_player)


    def update_screen(self):
        self.map.update()
        self.player.move()
        other_players_data = self.send_player_data()
        self.update_other_players_data(other_players_data)
        self.screen.update()

    def start(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_screen()

if __name__ == "__main__":
    game = Game()
    game.start()
