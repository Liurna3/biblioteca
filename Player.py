import pygame
from bibloteca.Control import Control

class Hitbox():
    def __init__(self, rect):
        self.rect = pygame.Rect.copy(rect)
        self.rect.width = 70
        self.rect.height = 70

    def set_position(self, x, y):
        self.rect.x = x - self.rect.width/2
        self.rect.y = y - self.rect.height/2


        
class Player(pygame.sprite.Sprite):
    
    def __init__(self, position = (0,0), control_id = -1):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # self.surface = pygame.transform.smoothscxale(
        #     pygame.image.load(image).convert(), (100, 100))

        self.pos = position
        self.speed = 255
        self.rotation_speed = 150
        self.direction = pygame.math.Vector2(0, -1)
        self.angle = 0
        self.clock = pygame.time.Clock()
        self.control = Control(
            control_id=control_id,
            key_down=pygame.K_s,
            key_up=pygame.K_w,
            key_left=pygame.K_a,
            key_right=pygame.K_d
        )

    def set_position(self, position = (0,0)):
        self.rect = self.image.get_rect(center=position)
        self.hitbox = Hitbox(self.rect)

        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255,0,0), self.hitbox.rect,2)
    
    def acelerar(self, dt):
        self.rect.move_ip(self.direction * self.speed * dt)
        self.hitbox.set_position(self.rect.centerx,self.rect.centery)

    def rotate(self, delta_angle):    
        self.image = pygame.transform.rotate(self.surface, self.angle)
        self.direction.rotate_ip(-delta_angle)
        self.angle = (self.angle + delta_angle) % 360
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def setImagen(self, imagen):
        self.surface = pygame.image.load(imagen).convert_alpha()
        self.image = self.surface
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = Hitbox(self.rect)
    
    def setSpeed(self, speed):
        self.speed = speed

    def setControl(self, control_id,key_down,key_up,key_left,key_right,key_fire):
        self.control = Control(control_id=control_id,key_down=key_down,key_up=key_up,key_left=key_left,key_right=key_right,key_fire = pygame.K_b)

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.hitbox.set_position(self.rect.centerx,self.rect.centery)
    
    def update(self):
        dt = self.clock.tick(60) / 1000
        self.control.update()

        if self.control.get(Control.LEFT):
            self.rotate(self.rotation_speed * dt)

        if self.control.get(Control.RIGHT):
            self.rotate(-self.rotation_speed * dt)

        if self.control.get(Control.UP):
            self.acelerar(dt)
