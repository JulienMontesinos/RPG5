from typing import SupportsIndex
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, p_id, x, y, frame_width, frame_height):
        super().__init__()
        self.id = p_id
        self.sprite_sheet = pygame.image.load("player.png")
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])
        #self.rect = self.image.get_rect()
        self.speed = 3
        self.x = x
        self.y = y
        self.position = [self.x, self.y]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.frame_width = frame_width 
        self.frame_height = frame_height 
        self.frame_num = 0
        self.frame_rect = (self.frame_num * self.frame_width, 0 * self.frame_height,
                           self.frame_width, self.frame_height)

        self.current_dir = "down"
        self.last_dir = self.current_dir

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def move_right(self):
        self.position[0] += self.speed
        self.rect.x = self.position[0]
        self.update_rect()
    
    def move_left(self):
        self.position[0] -= self.speed
        self.update_rect()

    def move_up(self):
        self.position[1] -= self.speed
        self.update_rect()

    def move_down(self):
        self.position[1] += self.speed
        self.update_rect()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.move_left()
            self.current_dir = "left"
            self.set_frame_rect(1)

        elif keys[pygame.K_RIGHT]:
            self.move_right()
            self.current_dir = "right"
            self.set_frame_rect(2)

        elif keys[pygame.K_UP]:
            self.move_up()
            self.current_dir = "up"
            self.set_frame_rect(3)

        elif keys[pygame.K_DOWN]:
            self.move_down()
            self.current_dir = "down"
            self.set_frame_rect(0)

        self.last_dir = self.current_dir
    
    def get_image(self, x, y):
        image = pygame.Surface([32,32])
        image.blit(self.sprite_sheet, (0,0), (x,y,32,32))
        return image

    def set_frame_rect(self, pic_row):
        self.frame_num += 1
        if self.current_dir != self.last_dir or self.frame_num > 2:
            self.frame_num = 0

        self.frame_rect = (self.frame_num * self.frame_width, pic_row * self.frame_height,
                           self.frame_width, self.frame_height)
    
    def draw(self, win, pic):
        win.blit(pic, self.position, self.frame_rect)