import pygame
import random

from bibloteca.settings import *

class Food(pygame.sprite.Sprite):

    def __init__(self, position = (0,0), image = None):
        pygame.sprite.Sprite.__init__(self)

        self.surface = pygame.image.load(image).convert_alpha()
        self.image = self.surface
        self.rect = self.image.get_rect(center=position)

class FoodFactory():
    def __init__(self, window_width, window_height):
        self.group = pygame.sprite.Group()
        self.window_width = window_width
        self.window_height = window_height


    def create(self):
        self.group.add(Food(position=(random.randint(0+70, self.window_width-70),random.randint(0+70, self.window_height-70)), image=self.image_path))
        
    def update(self):
        self.group.update()        
        pass

    def draw(self, surface):
        self.group.draw(surface)
        pass
        
    def activeFood(self):
        return len(self.group.sprites())

    def setImage(self, image_path):
        self.image_path = image_path
    
    def reset(self):
        self.group.empty()
