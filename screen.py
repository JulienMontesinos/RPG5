import pygame

class Screen:

    def __init__(self):
        self.width = 480
        self.height = 480
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Petit jeu en python')

    def update(self):
        pygame.display.flip()
        pygame.display.update()
        self.screen.fill((255,255,255))
    
    def get_size(self):
        return self.screen.get_size() 

    def get_display(self):
        return self.screen