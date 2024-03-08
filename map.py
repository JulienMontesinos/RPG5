import pygame
import pytmx
import pyscroll
from screen import Screen

class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.switch_map("map0")
    
    def switch_map(self, map:str):
        #chargement de la carte
        self.tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data,self.screen.get_size())
        
        #dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)
    
    def add_player(self,player):
        self.group.add(player)

    def update(self):
        self.group.update()
        self.group.draw(self.screen.get_display())
    
    def remove_player(self, player):
        if player in self.group:  # 假设玩家对象存储在某个pygame.sprite.Group中
            self.group.remove(player)