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
        self.screen = Screen()
        self.map = Map(self.screen)

        self.player = Player(p_id=None,
                             x = randint(35,310),
                             y = randint(300,430),
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
            #"player": self.player
            "position": self.player.position
        }
        self.sock.send(pickle.dumps(data))
        return self.sock.recv(2048)
        

    def update_other_players_data(self, data):
        #for player in data.values():
            #player.draw(self.screen, self.sprite_sheet)
            #self.map.add_player(player)
        for player_id, position in data.items():
            if player_id in self.other_players:
            # 更新现有玩家的位置
               existing_player = self.other_players[player_id]
               existing_player.x, existing_player.y = position
               existing_player.rect.topleft = position  # 确保也更新rect属性，以便正确渲染
            else:
            # 创建新的玩家对象并添加到字典和地图中
              new_player = Player(p_id=player_id, x=position[0], y=position[1], frame_width=32, frame_height=32)
              self.other_players[player_id] = new_player
              self.map.add_player(new_player)

    def update_screen(self): #Appeler en continuer depuis le jeu lancé
        #self.screen.fill((255, 255, 255))
        
        self.map.update()
        #self.map.add_player(self.player)
        
        #self.screen.upadate()

        self.player.move()
        #self.player.draw(self.screen, self.sprite_sheet)

        other_players_data = pickle.loads(self.send_player_data())
        self.update_other_players_data(other_players_data)
        #pygame.display.update()
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
